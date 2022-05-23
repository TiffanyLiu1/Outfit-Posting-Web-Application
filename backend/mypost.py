import json
from DBHandle import DBHandle

db_post = DBHandle(table='post')
db_user = DBHandle(table='user')
db_hist = DBHandle(table='history')

http_header = 'https://'
subfix = '.s3.amazonaws.com/'
bucket_name = 'post-s3-bucket'


def lambda_handler(event, context):
    # TODO implement

    # db_hist.update_item(key={
    #     'user_id': 'qq2'
    # },
    # feature={
    #     'hist_label': 'my'
    # })

    request = event['account']
    print('request from user {}'.format(request))

    response = get_post(request)

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


def get_post(user_id):
    user_record = db_user.lookup(key=[{
        'user_id': user_id,
    }])

    print(user_record)

    result = []
    if not user_record or not user_record[0]['mypost']:
        return result
    else:
        for post_id in user_record[0]['mypost']:
            records = db_post.lookup(key=[{
                'photo_id': post_id
            }])

            if user_id in records[0]['like_id_group']:
                sign = True
            else:
                sign = False

            Idx = {
                'imgId': post_id,
                'src': http_header + bucket_name + subfix + post_id,
                'likeAmount': len(records[0]['like_id_group']),
                # 'liked': sign,
                'account': user_id
            }

            result.append(Idx)

    print(result)
    return result