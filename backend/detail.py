import json
from DBHandle import DBHandle

db_user = DBHandle(table='user')
db_post = DBHandle(table='post')
db_hist = DBHandle(table='history')


def lambda_handler(event, context):
    # TODO implement

    response = query_detail(event['imgId'], event['account'])

    return {
        "isBase64Encoded": 'false',
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Headers': 'Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With,x-api-key',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,PUT,GET',
        },
        'body': response
    }


def query_detail(photo_id, user_id):
    post_records = db_post.lookup(key=[{
        'photo_id': photo_id
    }])

    response = dict()

    if not post_records:
        print('no records of the photo_id')
        return response

    http_header = 'https://'
    subfix = '.s3.amazonaws.com/'
    bucket_name = 'post-s3-bucket'

    response['img'] = http_header + bucket_name + subfix + photo_id
    response['detailUserName'] = post_records[0]['user_id']
    response['title'] = post_records[0]['title']

    like_record = db_user.lookup(key=[{
        'user_id': user_id
    }])

    if photo_id in like_record[0]['mylike']:
        response['liked'] = True
    else:
        response['liked'] = False

    response['imgId'] = photo_id
    response['content'] = post_records[0]['description']

    db_hist.update_item(key={
        'user_id': user_id
    },
        feature={
            'detailed_photo_id': [photo_id]
        })

    db_hist.update_item(key={
        'user_id': user_id
    },
        feature={
            'detailed_labels': post_records[0]['labels']
        })

    return response