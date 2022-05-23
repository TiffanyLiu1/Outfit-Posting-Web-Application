import boto3
from botocore.exceptions import ClientError

# the database we define to use
user_table = '6998user_table'
photo_table = '6998photo_table'

# how many search history to keep
LSTM = 10


class DBHandle:
    """
        enable database insert, update, lookup and delete
        with initialized table name, provided primary key
        and other relevant information.
    """

    def __init__(self, table=""):
        self.db = boto3.resource('dynamodb')
        self.table_name = table
        self.table = self.db.Table(self.table_name)

    def insert_data(self, data_list):
        """
        :param data_list: (list) with inner json format
            [
                {
                    'primary key': ...,
                    'attribute1': ...,
                    'attribute2': ...,
                    ...
                },...
            ]
        :return: insert operation response
        """

        # overwrite if the same index is provided
        for data in data_list:
            response = self.table.put_item(Item=data)
        print('insert_data: response', response)

        return response

    def update_item(self, key, feature):
        """
            :param key: (list) format as following
                {
                    'primary key': value
                }
            :param feature: (json) format of the updated attribute and the value
                {
                    'attribute': new_value
                }
            :return: modified item information
        """

        # -----------------------------------
        # if we allow user to change its user_name,
        # we need to update every db we operate on
        # -----------------------------------
        avail_list = ['mypost', 'mylike', 'like_id_group', 'like_photo_id', 'like_labels',
        'detail_photo_id', 'detail_labels', 'search_photo_id', 'search_labels']
        # global check variable
        # primary_key = list(key.keys())[0]
        expression = "set #feature =:f"

        # variables to be updated
        attribute = list(feature.keys())[0]
        value = list(feature.values())[0]

        # append information from search database
        if attribute in avail_list:
            expression = "set #feature = list_append(#feature,:f)"
        #     try:
        #         search_history = response[0]['search_history']
        #         # check if stored history records are more than LSTM, remove and add
        #         if len(search_history) >= LSTM:
        #             # only keep the last LSTM-1 records
        #             search_history = search_history[-LSTM+1:]
        #         search_history.append(value)
        #         value = search_history
        #     except:
        #         value = [value]
        # # append information from photo database if click like button
        # elif attribute == 'like_id':
        #     response = self.lookup(key=key)
        #     like_list = response[0]['like_id']

        #     # remove information from photo database if double click like button
        #     if value in like_list:
        #         like_list.remove(value)
        #     else:
        #         like_list.append(value)
        #     value = like_list
            # expression="set #feature=list_append(#feature,:f)"

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
            ReturnValues="ALL_NEW"          # return whole information of the item
        )
        print(response)
        
        return response

    def delete_item(self, key):
        """
            :param key: json format of primary key-value
                {
                    'primary key': value
                }

            :return: delete response if exists, else no 
            return
        """

        try:
            response = self.table.delete_item(Key=key)
        except ClientError as e:
            print('Error', e.response['Error']['Message'])
        else:
            print(response)
            return response

    def lookup(self, key):
        """
            :param key: json format of primary key-value
                {
                    'primary key': value
                }
            # -------------------------- details ----------------------------
            look up data in dynamoDB with key-value set by format (multi-search)
            [
                {
                    'primary key': value
                },
                {
                    'primary key': value
                },
                ... ...
            ]
            if only search one item, format as below
            {
                'primary key': value
            }

            :return: modified item information
            # -------------------------- details ----------------------------
            if nothing found in database, return an empty list, else return
            the found record by json format below:
            [
                {
                    'primary key': value1,
                    'attribute1': value2,
                    ... ...
                },
                {
                    ... ...
                }
            ]
        """

        result = []
        if not key:
            return None
        # elif len(key) == 1:
        #     key = [key]

        for val in key:
            try:
                response = self.table.get_item(Key=val)
            except ClientError as e:
                continue
            try:
                response['Item']
                result.append(response['Item'])
            except:
                continue

        return result
