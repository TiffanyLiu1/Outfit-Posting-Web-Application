import json
from DBHandle import DBHandle

db_post = DBHandle(table='post')
db_user = DBHandle(table='user')


def lambda_handler(event, context):
    # TODO implement

    # user = '1@qq.com'

    print(event)
    response = query_favorite(event['account'])

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


def query_favorite(user_id):
    user_record = db_user.lookup(key=[{
        'user_id': user_id
    }])

    http_header = 'https://'
    subfix = '.s3.amazonaws.com/'
    bucket_name = 'post-s3-bucket'
    # bucket_name = os.environ['BUCKET']

    result = []
    try:
        like_record = user_record[0]['mylike']
        if not like_record:
            return result

        for like in like_record:
            post_record = db_post.lookup(key=[{
                'photo_id': like
            }])

            Idx = {
                'imgId': like,
                'src': http_header + bucket_name + subfix + like,
                'likeAmount': len(post_record[0]['like_id_group']),
                'liked': True,
                'account': post_record[0]['user_id']
            }

            result.append(Idx)
    except:
        return result

    return result