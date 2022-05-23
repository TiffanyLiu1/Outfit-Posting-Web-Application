import boto3
from botocore.exceptions import ClientError


class DynamoDB:
    def __init__(self, table=''):
        self.client = boto3.resource('dynamodb')
        self.table = self.client.Table(table)
        self.table_name = table


    def insert_data(self, data_list):
        # overwrite if the same index is provided
        for data in data_list:
            response = self.table.put_item(Item=data)
        # print('@insert_data: response', response)
        return response


    def lookup_data(self, key):
        try:
            response = self.table.get_item(Key=key)
        except ClientError as e:
            print('Error', e.response['Error']['Message'])
        else:
            print('Search post response from DynamoDB: ', response['Item'])
            return response['Item']


    def update_item(self, key, feature):
        avail_list = ['mypost', 'mylike', 'like_id_group', 'like_photo_id',
                      'search_photo_id', 'search_labels', 'detail_photo_id', 'detail_labels']
        expression = "set #feature=:f"

        # variables to be updated
        attribute = list(feature.keys())[0]
        value = list(feature.values())[0]

        if attribute in avail_list:
            expression = "set #feature =list_append(#feature,:f)"

        response = self.table.update_item(
            Key=key,
            UpdateExpression=expression,
            ExpressionAttributeValues={
                ':f': value
            },
            ExpressionAttributeNames={
                "#feature": attribute
            },
            # ReturnValues="UPDATED_NEW"    # return only modified part
            ReturnValues="ALL_NEW"  # return whole information of the item
        )
        print('return from update database: ', response)
        return response


    def delete_item(self, key):
        try:
            response = self.table.delete_item(Key=key)
        except ClientError as e:
            print('Error', e.response['Error']['Message'])
        else:
            print(response)
            return response



    def query_table(self):
        dynamodb_client = boto3.client('dynamodb')
        response = dynamodb_client.query(
            TableName=self.table_name,
            Select='ALL_ATTRIBUTES',
            # AttributesToGet=['photo_id'],
            KeyConditionExpression='photo_id=:id',
            ExpressionAttributeValues={
                ':id': {'S': 'images.jpg'}
            },
            # Limit=10,
            # ReturnConsumedCapacity="TOTAL"
        )
        return response


    def scan_table(self, value):
        dynamodb_client = boto3.client('dynamodb')
        response = dynamodb_client.scan(
            TableName=self.table_name,
            Select='ALL_ATTRIBUTES',
            # AttributesToGet=['photo_id'],
            FilterExpression='user_id=:id',
            ExpressionAttributeValues={
                ':id': {'S': value}
            },
            Limit=20,
            # ReturnConsumedCapacity="TOTAL"
        )
        return response




