import logging
import boto3
from datetime import datetime


class DynamoDBFormatter(logging.Formatter):
    def format(self, record):
        data = record.__dict__.copy()
        return data['msg']


class DynamoDBHandler(logging.StreamHandler):
    
    def __init__(self, level=logging.WARNING):
        logging.StreamHandler.__init__(self, level)
        self.level = level
        self.client = boto3.client(
            'dynamodb', 
            region_name='eu-west-1'
        )
        self.table_name = 'AutomationLogging'
        self.formatter = DynamoDBFormatter()
        try:
            self.client.create_table(
                AttributeDefinitions=[
                    {
                        'AttributeName': 'Time',
                        'AttributeType': 'S',
                    }
                ],
                KeySchema=[
                    {
                        'AttributeName': 'Time',
                        'KeyType': 'HASH',
                    }
                ],
                BillingMode='PAY_PER_REQUEST',
                TableName=self.table_name,
            )
        except self.client.exceptions.ResourceInUseException:
            pass
        
    def emit(self, record):
        formatted_record = self.format(record)
        self.client.put_item(
                    TableName=self.table_name,
                    Item={
                        'Time': {
                            'S': str(datetime.utcnow())
                        },
                        'Record': {
                            'S': str(formatted_record)
                        }
                    }
                )    