import json
from DBHandle import DBHandle

db = DBHandle(table='user')


def lambda_handler(event, context):
    # TODO implement

    # user = '1@qq.com'
    # password = 'adwadwad'

    response = log_in(event['account'], event['password'])

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


def log_in(user, password):
    '''
        when logging in, check if user and password matches in 'user' table

        # param:
            user: (str) unique email address provided by user
            password: (str) password to match the specific user

        # return:
            integer:
                1: username not found
                2: correct username but wrong password
                3: correct match
    '''

    record = db.lookup(key=[{'user_id': user}])
    print('look up result: {}'.format(record))

    if not record:
        print('provided username not exists!')
        return 1
        # return {
        #         'sign': False,
        #         'msg': 'There is no account associated with the email address provided!'
        #     }

    if record[0]['password'] == password:
        print('log in success!')
        return 3
    else:
        print('password error!')
        return 2


def modify(user, password, new_password=''):
    '''
        when a user modifies his/her password, check old password and enable news

        # param:
            user: (str) unique email address provided by user
            password: (str) password to match the specific user
            new_password: (str) new password to modify

        # return:
            sign:
                True: if password matches
                False: if password does not match
            message:
                specific error caused by modifying
    '''

    record = db.lookup({'user_id': user})

    if record[0]['password'] == password:
        db.update_item(key={'user_id': user}, feature={'password': new_password})
        return {
            'sign': True,
            'msg': 'new password modified!'
        }
    else:
        return {
            'sign': False,
            'msg': 'password not matches'
        }