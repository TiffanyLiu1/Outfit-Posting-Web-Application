import json
from DBHandle import DBHandle

db_post = DBHandle(table='post')
db_user = DBHandle(table='user')
db_hist = DBHandle(table='history')


def lambda_handler(event, context):
    # TODO implement

    print(event)

    response = post_like(event['account'], event['imgId'])


def post_like(user_id, photo_id):
    print(user_id, photo_id)

    like_sign = True
    # query in 'user' database
    mylike_records = db_user.lookup(key=[{
        'user_id': user_id
    }
    ])

    post_records = db_post.lookup(key=[{
        'photo_id': photo_id
    }
    ])

    try:
        mylike = mylike_records[0]['mylike']
        if not mylike:
            mylike = [photo_id]
        elif photo_id in mylike:
            like_sign = False
            mylike.remove(photo_id)
        else:
            mylike.append(photo_id)
    except:
        mylike = [photo_id]

    try:
        db_user.update_item(
            key={
                'user_id': user_id
            },
            feature={
                'mylike': mylike
            },
            sign=False
        )
    except:
        print('user table update error')

    # query in 'post' database
    try:
        # current like the photo
        if like_sign:
            db_post.update_item(
                key={
                    'photo_id': photo_id
                },
                feature={
                    'like_id_group': [user_id]
                }
            )
        # used to like, but now dislike
        else:
            like_id_group = post_records[0]['like_id_group']
            like_id_group.remove(user_id)

            db_post.update_item(
                key={
                    'photo_id': photo_id
                },
                feature={
                    'like_id_group': like_id_group
                },
                sign=False
            )
    except:
        print('post table updated error')

    try:
        # user like current photo
        if like_sign:
            db_hist.update_item(
                key={
                    'user_id': user_id
                },
                feature={
                    'like_photo_id': [photo_id]
                }
            )

            db_hist.update_item(
                key={
                    'user_id': user_id
                },
                feature={
                    'like_labels': [post_records[0]['labels']]
                }
            )
        # user used to like, now dislike
        else:
            like_records = db_hist.lookup(key=[{
                'user_id': user_id
            }])

            like_photo_id = like_records[0]['like_photo_id']
            like_labels = like_records[0]['like_labels']

            index = like_photo_id.index(photo_id)

            del like_photo_id[index]
            del like_labels[index]

            print(like_photo_id, like_labels)
            db_hist.update_item(
                key={
                    'user_id': user_id
                },
                feature={
                    'like_photo_id': like_photo_id
                },
                sign=False
            )

            db_hist.update_item(
                key={
                    'user_id': user_id
                },
                feature={
                    'like_labels': like_labels
                },
                sign=False
            )

    except:
        print('history table update error')

    return