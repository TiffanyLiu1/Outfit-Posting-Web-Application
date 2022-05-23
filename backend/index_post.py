import json
import boto3
import requests
from DynamoDB import DynamoDB
from ElasticSearch import ElasticSearch

db_user = DynamoDB(table='user')
db_post = DynamoDB(table='post')
db_history = DynamoDB(table='history')

# endpoint = "sms-spam-classifier-mxnet-2022-04-20-01-07-32-116"    # ------------> NLP model endpoint
endpoint = 'https://search-photos-bxigr5a2lhirygbext2ru46tui.us-east-1.es.amazonaws.com'
index = 'photos'
auth = ('master', 'code')
es = ElasticSearch(endpoint=endpoint, index=index, auth=auth)

s3_client = boto3.client('s3')
rekog_client = boto3.client('rekognition')


# sagemaker_client = boto3.Session().client(service_name='sagemaker-runtime', region_name='us-east-1')
# db_client = boto3.resource('dynamodb')


def lambda_handler(event, context):
    print('event -->', event)
    # get 'objectKey' and 'bucket'
    s3 = event['Records'][0]['s3']
    bucket_name = s3['bucket']['name']  # 'post-s3-bucket'
    image_name = s3['object']['key']  # e.g. 'test.jpg'

    # get customlabels (metadata)
    labels = []
    s3_response = s3_client.head_object(
        Bucket=bucket_name,
        Key=image_name
    )
    metaData = s3_response['Metadata']
    print('metaData is: ', metaData)
    if len(metaData) != 0:
        custum_labels = metaData['customlabels'].split(',')
        labels.extend(custum_labels)

    # get rekognition 'labels'
    image_in = {'S3Object': {'Bucket': bucket_name, 'Name': image_name}}
    detect_out = rekog_client.detect_labels(Image=image_in,
                                            MaxLabels=10,
                                            MinConfidence=60)
    for label in detect_out['Labels']:
        labels.append(label['Name'])
    print('labels of image: ', labels)

    # get title and post description
    if len(metaData) != 0:
        post_title = metaData['title']
        post_description = metaData['postcontent']
        user_id = metaData['account']

    # # ----- test case -------------
    # request = {'title': 'Fashion Dress', 'postcontent': 'This is a fashionable dress', 'account': 'lxtlxt2'}
    # post_title = request['title']
    # post_description = request['postcontent']
    # user_id = request['account']
    # # ----- test case -------------

    # get NLP labels by using post description
    # --------------- endpoint with trained mode ---------------

    # create a JSON format
    es_data = {
        'photo_id': image_name,
        'labels': labels
    }

    # Insert data into ElasticSearch
    resp = es.post_photo(data=es_data)
    print('resp store in elastic', resp.text)

    # Insert data into DynamoDB
    db_data = [
        {
            "photo_id": image_name,
            "user_id": user_id,
            "labels": labels,
            "like_id_group": [],
            "description": post_description,
            "title": post_title
        }
    ]
    db_post.insert_data(data_list=db_data)
    db_user.update_item(key={'user_id': user_id}, feature={'mypost': [image_name]})

    to_frontend = {
        "imgId": image_name
    }
    print('to_frontend: ', to_frontend)
    return {
        'statusCode': 200,
        'body': image_name
    }