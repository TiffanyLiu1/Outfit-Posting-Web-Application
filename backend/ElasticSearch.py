import json
import requests


class ElasticSearch:
    def __init__(self, endpoint, index, auth):
        self.endpoint = endpoint
        self.index = index
        self.search_url = self.endpoint + '/' + self.index + '/_search'
        self.headers = {'Content-type': 'application/json'}
        self.auth = auth
        self.post_url = self.endpoint + '/' + self.index + '/0'


    def search_photos(self, labels):
        # find the hit photos of each keyword
        resp = []
        for label in labels:
            if label != '' and label is not None:
                query = {
                    "query": {
                        "match": {
                            "labels": label
                        }

                    }
                }
                r = requests.get(self.search_url, auth=self.auth, headers=self.headers, data=json.dumps(query))
                # print('temp data: ', json.loads(r.text))
                resp.append(json.loads(r.text))

        key_list = []
        for r in resp:
            if 'hits' in r:
                for hit in r['hits']['hits']:
                    image_name = hit['_source']['photo_id']
                    if image_name not in key_list:
                        key_list.append(image_name)
        print('image key output: ', key_list)
        return key_list


    def post_photo(self, data):
        resp = requests.post(self.post_url, auth=self.auth, headers=self.headers, data=json.dumps(data).encode("utf-8"))
        return resp


    def delete_es_part(self, key):
        # region = 'us-east-1'
        # service = 'es'
        # credentials = boto3.Session().get_credentials()
        # awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)

        # Get environment variable
        # es_endpoint = os.environ['ES_ENDPOINT']

        # es_endpoint = 'https://search-photos-bxigr5a2lhirygbext2ru46tui.us-east-1.es.amazonaws.com'
        # print('es_endpoint is', es_endpoint)

        # index = 'photos'
        url = self.endpoint + '/' + self.index + '/_delete_by_query'

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
        r = requests.post(url, auth=self.auth, headers=headers, data=json.dumps(query))
        print(r)
        return

    def delete_es_all(self):
        # region = 'us-east-1'
        # service = 'es'
        # credentials = boto3.Session().get_credentials()
        # awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)

        # Get environment variable
        # es_endpoint = os.environ['ES_ENDPOINT']

        # es_endpoint = 'https://search-photos-bxigr5a2lhirygbext2ru46tui.us-east-1.es.amazonaws.com'
        # print('es_endpoint is', es_endpoint)

        # index = 'photos'
        url = self.endpoint + '/' + self.index

        # Make the signed HTTP request
        r = requests.delete(url, auth=self.auth)
        print(r)
        return