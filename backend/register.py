import json
from DBHandle import DBHandle

db = DBHandle(table='user')


# db_hist = DBHandle(table='history')

def lambda_handler(event, context):
    # TODO implement

    print(event)
    request = event
    # ---- test case ----
    # request = {
    #     'account': 'wqs',
    #     'password': 'e21e131231231'
    # }

    # db_hist.update_item(key={
    #     'user_id': 'qq2'
    # },
    # feature={
    #     'hist_label': [['pig','rabbit']]    # update for list of list
    #     'hist_label': ['pig','cat']         # update for list
    #     # 'mypost': ['1.png']
    # })

    response = register(request['account'], request['password'])

    return {
        "isBase64Encoded": 'false',
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Headers': 'Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With,x-api-key',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,PUT,GET',
        },
        'body': str(response)
    }


def register(user, password):
    '''
        when a new user registers, record in all database with the email address
        provided.

        # param:
            user: (str) unique email address provided by user
            password: (str) password to match the specific user

        # return:
            None
    '''

    DATABASE = ['user', 'history']

    try:
        record = db.lookup(key=[{'user_id': user}])
        print('look up result: \n {}'.format(record))

        if record:
            # return {
            #         'sign': False,
            #         'msg': 'email address already registered!'
            #     }
            print('current username already exists')
            return 2

        for database in DATABASE:
            if database == 'user':
                response = db.insert_data([
                    {
                        'user_id': user,
                        'password': password,
                        'mylike': [],
                        'mypost': []
                    }
                ]
                )
                print('insert into user table response: {}'.format(response))
            else:
                re_db = DBHandle(table=database)
                response = re_db.insert_data([
                    {
                        'user_id': user,
                        'like_photo_id': [],
                        'like_labels': [],
                        'detail_photo_id': [],
                        'detail_labels': [],
                        'search_photo_id': [],
                        'search_labels': []
                    }
                ]
                )
                print('insert into history table response: {}'.format(response))
        # return {
        #             'sign': True,
        #             'msg': 'register success!'
        #     }
        return 1
    except:
        return 3