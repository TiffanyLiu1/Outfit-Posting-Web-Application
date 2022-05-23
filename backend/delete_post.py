import json
import boto3
import requests
from DBHandle import DBHandle

db_post = DBHandle(table='post')
db_user = DBHandle(table='user')
bucket_name = 'post-s3-bucket'
s3 = boto3.client('s3')
auth = ('master', 'Cc12345678!')


def lambda_handler(event, context):
    # TODO implement

    print(event)
    # delete all relevant records from database and s3
    delete_db(event['account'], event['imgId'])

    # delete corresponding photo from  es
    try:
        delete_es(request['imgId'])
    except:
        print('elastic search delete error')

    return
    # get_all()


def get_all():
    dynamodb_client = boto3.client('dynamodb')
    record = dynamodb_client.query(
        TableName='post',
        Select='ALL_ATTRIBUTES',
        # AttributesToGet=['photo_id'],
        KeyConditionExpression='photo_id=:id',
        ExpressionAttributeValues={
            ':id': {'S': 'images.jpg'}
        },
        Limit=10,
        # ReturnConsumedCapacity="TOTAL"
    )

    print(record)


def delete_db(user_id, photo_id):
    post_records = db_post.lookup(key=[{
        'photo_id': photo_id
    }])

    try:
        like_id_group = post_records[0]['like_id_group']

        # delete records from users who liked this photo
        if like_id_group:
            delete_cor(like_id_group, photo_id)
    except:
        print('no like user yet!')

    # delete record from post table
    response = db_post.delete_item(key={
        'photo_id': photo_id,
    })

    user_record = db_user.lookup(key=[{
        'user_id': user_id
    }])

    # delete record from user mypost schema
    try:
        mypost = user_record[0]['mypost']
        mypost.remove(photo_id)
        db_user.update_item(key={
            'user_id': user_id
        },
            feature={
                'mypost': mypost
            })
    except:
        print('no photo_id to be removed')

    # delete photo in s3
    try:
        s3.delete_object(Bucket=bucket_name, Key=photo_id)
    except:
        print('error when deleting from s3')

    return


def delete_cor(group, photo_id):
    for user in group:
        records = db_user.lookup(key=[{
            'user_id': user
        }])

        try:
            mylike = records[0]['mylike']
            mylike.remove(photo_id)
            db_user.update_item(key={
                'user_id': user
            },
                feature={
                    'mylike': mylike
                })
        except:
            print('error while recursion user: {}'.format(user))

    return


def delete_es(key):
    region = 'us-east-1'
    service = 'es'
    # credentials = boto3.Session().get_credentials()
    # awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)

    # Get environment variable
    # es_endpoint = os.environ['ES_ENDPOINT']

    es_endpoint = 'https://search-photos-bxigr5a2lhirygbext2ru46tui.us-east-1.es.amazonaws.com'
    print('es_endpoint is', es_endpoint)

    index = 'photos'
    url = es_endpoint + '/' + index + '/_delete_by_query'

    # Elasticsearch 6.x requires an explicit Content-Type header
    headers = {"Content-Type": "application/json"}

    query = {
        "query": {
            "match": {
                "photo_id": key
            }
        }
    }

    # Make the signed HTTP request
    r = requests.post(url, auth=auth, headers=headers, data=json.dumps(query))
    # r = requests.delete(url, auth=auth)

    print(r)
    return


def delete_es_all():
    region = 'us-east-1'
    service = 'es'
    # credentials = boto3.Session().get_credentials()
    # awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)

    # Get environment variable
    # es_endpoint = os.environ['ES_ENDPOINT']

    es_endpoint = 'https://search-photos-bxigr5a2lhirygbext2ru46tui.us-east-1.es.amazonaws.com'
    print('es_endpoint is', es_endpoint)

    index = 'photos'
    # url = es_endpoint + '/' + index + '/_delete_by_query'
    url = es_endpoint + '/' + index

    # Make the signed HTTP request
    # r = requests.post(url, auth=auth, headers=headers, data=json.dumps(query))
    r = requests.delete(url, auth=auth)

    print(r)
    return