import json
import boto3
import requests
import inflect
from botocore.exceptions import ClientError
from DynamoDB import DynamoDB
from ElasticSearch import ElasticSearch

db_user = DynamoDB(table='user')
db_post = DynamoDB(table='post')
db_history = DynamoDB(table='history')

endpoint = 'https://search-photos-bxigr5a2lhirygbext2ru46tui.us-east-1.es.amazonaws.com'
index = 'photos'
auth = ('master', 'code')
es = ElasticSearch(endpoint=endpoint, index=index, auth=auth)

lex_client = boto3.client('lex-runtime')


# db_client = boto3.resource('dynamodb')


def lambda_handler(event, context):
    try:
        print('event: ', event)
        try:
            # request = event['queryStringParameters']['q']
            request = event
            # # ----------- test case ---------------
            # request = {'input': 'Show me nike', 'account': 'lxtlxt'}
            # # ----------- test case ---------------
        except:
            print('We have not detected any post searching query.')
            return

        input_query = request['input']
        user_id = request['account']

        # lex
        response_lex = lex_client.post_text(
            botName='PostBot',
            botAlias="post_botbot",
            userId="testuser",
            inputText=input_query)
        print('response from lex: ', response_lex)

        if 'slots' in response_lex:
            keys = [response_lex['slots']['KeyOne'], response_lex['slots']['KeyTwo']]
            print('keyword is: ', keys)

            # change plural to singular
            for i in range(len(keys)):
                if keys[i] is not None:
                    keys[i] = get_singular(keys[i])
            print('keyword is: ', keys)

            # get photos_id from elastic search
            images_key = es.search_photos(labels=keys)  # get photo id from elastic search labels
            print('the matched photo: ', images_key)

            # update history table
            db_history.update_item(key={'user_id': user_id}, feature={'search_photo_id': images_key})
            # history_data = db_history.lookup_data(key={'user_id': user_id})
            # print('history data is: ', history_data)
            # search_photo_id = history_data['search_photo_id']
            # search_labels = history_data['search_labels']
            # search_photo_id.extend(images_key)

            # get post data from DynamoDB, and format returned posts data
            posts_data = []
            for photo_id in images_key:
                try:
                    post_data = db_post.lookup_data(key={'photo_id': photo_id})
                except:
                    continue
                else:
                    user_data = db_user.lookup_data(key={'user_id': user_id})
                    data = dict()
                    data['imgId'] = photo_id
                    data['src'] = 'https://post-s3-bucket.s3.amazonaws.com/' + photo_id
                    data['likeAmount'] = len(post_data['like_id_group'])
                    if photo_id in user_data['mylike']:
                        data['liked'] = True
                    else:
                        data['liked'] = False
                    posts_data.append(data)

                    # update history table
                    try:
                        # print('len of labels --->', len(post_data['labels']))
                        db_history.update_item(key={'user_id': user_id}, feature={'search_labels': post_data['labels']})
                    except:
                        # print('Error !!!')
                        # print('len of labels --->', len(post_data['labels']))
                        continue
                    # search_labels.extend(post_data['labels'])
                    # db_history.update_item(key={'user_id': user_id}, feature={'search_photo_id': photo_id})
                    # db_history.update_item(key={'user_id': user_id}, feature={'search_labels': post_data['labels']})

            print('posts data: ', posts_data)

            # update history table
            # db_history.update_item(key={'user_id': user_id}, feature={'search_photo_id': search_photo_id})
            # db_history.update_item(key={'user_id': user_id}, feature={'search_labels': search_labels})

            # format the response return to frontend
            response = {
                "statusCode": 200,
                "headers": {"Access-Control-Allow-Origin": "*", "Content-Type": "application/json"},
                "body": posts_data,
                "isBase64Encoded": False
            }
        else:
            response = {
                "statusCode": 200,
                "headers": {"Access-Control-Allow-Origin": "*", "Content-Type": "application/json"},
                "body": [],
                "isBase64Encoded": False
            }
        print('res -->', response)

    except:
        print('---> Error: search access deny')
        response = {
            "statusCode": 200,
            "headers": {"Access-Control-Allow-Origin": "*", "Content-Type": "application/json"},
            "body": [],
            "isBase64Encoded": False
        }

    return response


def get_singular(noun):
    s = inflect.engine()
    singular = s.singular_noun(noun)
    if singular:
        return singular
    else:
        return noun

# # search photo_id from elastic search
# def search_photos(labels):
#     endpoint = 'https://search-photos-3m4sdle7y6dognxadyonvkdkeq.us-east-1.es.amazonaws.com'
#     index = 'photos'
#     elastic_url = endpoint + '/' + index + '/_search'
#     headers = {'Content-type': 'application/json'}
#
#     # find the hit photos of each keyword
#     resp = []
#     for label in labels:
#         if label != '' and label is not None:
#             query = {
#                 "query": {
#                     "match": {
#                         "labels": label
#                     }
#
#                 }
#             }
#             r = requests.get(elastic_url, auth=('master', 'code'), headers=headers, data=json.dumps(query))
#             print('temp data: ', json.loads(r.text))
#             resp.append(json.loads(r.text))
#
#     key_list = []
#     for r in resp:
#         if 'hits' in r:
#             for hit in r['hits']['hits']:
#                 image_name = hit['_source']['photo_id']
#                 if image_name not in key_list:
#                     key_list.append(image_name)
#     print('image key output: ', key_list)
#     return key_list


# # search data from DynamoDB
# def lookup_data(key, db=db_client, table=''):
#     if not db:
#         db = boto3.resource('dynamodb')
#     table = db.Table(table)
#     try:
#         response = table.get_item(Key=key)
#     except ClientError as e:
#         print('Error', e.response['Error']['Message'])
#     else:
#         print('Search post response from DynamoDB: ', response['Item'])
#         return response['Item']


# def update_item(key, feature, db=db_client, table=''):
#     if not db:
#         db = boto3.resource('dynamodb')
#     table = db.Table(table)
#     expression = "set #feature=:f"
#
#     # variables to be updated
#     attribute = list(feature.keys())[0]
#     value = list(feature.values())[0]
#
#     response = table.update_item(
#         Key=key,
#         UpdateExpression=expression,
#         ExpressionAttributeValues={
#             ':f': value
#         },
#         ExpressionAttributeNames={
#             "#feature": attribute
#         },
#         # ReturnValues="UPDATED_NEW"    # return only modified part
#         ReturnValues="ALL_NEW"  # return whole information of the item
#     )
#     print('return from update database: ', response)
#     return response