import json
import requests
from DynamoDB import DynamoDB
from ElasticSearch import ElasticSearch

db_user = DynamoDB(table='user')
db_post = DynamoDB(table='post')
db_history = DynamoDB(table='history')

endpoint = 'https://search-photos-bxigr5a2lhirygbext2ru46tui.us-east-1.es.amazonaws.com'
index = 'photos'
auth = ('master', 'Cc12345678!')
es = ElasticSearch(endpoint=endpoint, index=index, auth=auth)


def lambda_handler(event, context):
    try:
        request = event
        # # ---------- test case ----------
        # request = {'account': 'lxtlxt2'}
        # # ---------- test case ----------
        user_id = request['account']

        history_data = db_history.lookup_data(key={'user_id': user_id})
        print('history data', history_data)
        like_labels = history_data['like_labels']  # list of lists
        search_labels = history_data['search_labels']  # list
        detail_labels = history_data['detail_labels']  # list
        like_photo_id = history_data['like_photo_id']  # list

        # print('like_labels: ', like_labels)
        # print('search_labels', search_labels)
        # print('detail_labels', detail_labels)
        # print('like_photo_id', like_photo_id)

        # flatten list of lists
        like_labels = [item for sublist in like_labels for item in sublist]
        # print('like_labels after remove outer list: ', like_labels)
        # detail_labels = [item for sublist in detail_labels for item in sublist]
        # like_photo_id = [item for sublist in like_photo_id for item in sublist]

        # search matched photos from elastic search
        es_labels = []
        es_labels.extend(like_labels)
        es_labels.extend(search_labels)
        es_labels.extend(detail_labels)

        es_labels = list(set(es_labels))

        print('recommendation es labels ---> ', es_labels)
        match_photo_es = es.search_photos(labels=es_labels[:10])
        # match_photo_like = es.search_photos(labels=like_labels)    # search matched photos in like_labels
        # match_photo_search = es.search_photos(labels=search_labels)  # search matched photos in search_labels
        # match_photo_detail = es.search_photos(labels=detail_labels)  # search matched photos in detail_labels

        # # search for other photos of the liked author  1
        # liked_author = []
        # for photo_id in like_photo_id:
        #     post_data = db_post.lookup_data(key={'photo_id': photo_id})
        #     post_user = post_data['user_id']
        #     if post_user not in liked_author:
        #         liked_author.append(post_user)
        # match_photo_liked_author = []
        # for author in liked_author:
        #     user_data = db_user.lookup_data(key={'user_id': author})
        #     match_photo_liked_author.extend(user_data['mypost'])

        # combine all the matched photo
        # match_photo = list(set(match_photo_like + match_photo_search + match_photo_detail + match_photo_liked_author))
        # match_photo = list(set(match_photo_es + match_photo_liked_author))    # also recommand photo of liked author  1
        match_photo = list(set(match_photo_es))
        print('matched photos: ', match_photo)

        # To process the condition if there is no matched photo (always happend for the first-time user)
        if len(match_photo) == 0:
            print('recommendation is empty')
            random_photos = db_post.scan_table(value='yz3917')
            random_photos = random_photos['Items']
            for random_photo in random_photos:
                match_photo.append(random_photo['photo_id']['S'])
            print('The random recommended photos: ', match_photo)
            # print('DB temp: ', temp['Items'][0]['photo_id'])
            # for item in db_post.scan_table():
            #     return_data.append(item)
            # print('return data: ', return_data)

        # return all matched photos to the frontend
        return_data = []
        for photo_id in match_photo:
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
                return_data.append(data)

        print('return data: ', return_data)

        response = {
            "statusCode": 200,
            "headers": {"Access-Control-Allow-Origin": "*", "Content-Type": "application/json"},
            "body": return_data,
            "isBase64Encoded": False
        }

    except:
        print('---> Error: recommendation access deny')
        response = {
            "statusCode": 200,
            "headers": {"Access-Control-Allow-Origin": "*", "Content-Type": "application/json"},
            "body": [],
            "isBase64Encoded": False
        }
    print('response -->', response)
    return response