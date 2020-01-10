import json
from urllib.parse import unquote_plus
import boto3
import csv
import sys
import uuid

from botocore.exceptions import ClientError

print('Loading function')

s3 = boto3.client('s3')


def lambda_handler(event, context):
    #print("Received event: " + json.dumps(event, indent=2))

    # Get the object from the event and show its content type
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    
    region='us-east-1'
    recList=[]
    
    try:
       
        dyndb = boto3.client('dynamodb', region_name=region)
        csvData = s3.get_object(Bucket=bucket, Key=key)
        recList = csvData['Body'].read().decode("utf-8").split('\n')
        firstrecord=True
        csv_reader = csv.reader(recList, delimiter=',', quotechar='"')
        for row in csv_reader:
            if (firstrecord):
                firstrecord=False
                continue
            print(str(row))
            
            accountName = row[0]
            accountID = row[1]
            customerID = row[2]
            ticker = row[3]
            investment_type = row[4]
            purchase_price = row[5]
            number_of_shares = row[6]
            purchase_date = row[7]
            response = dyndb.put_item(
                TableName='InvestmentPortfolio',
                Item={
                'transactionID': {'S': str(uuid.uuid1())},
                'customerID' : {'S':customerID},
                'accountID' : {'S':accountID},
                'accountName' : {'S':accountName},
                'ticker': {'S':ticker},
                'investment_type': {'S':investment_type},
                'purchase_price': {'N':purchase_price},
                'number_of_shares': {'N':number_of_shares},
                'purchase_date': {'S':purchase_date},
                }
            )
        print('Put succeeded:')
        
    except ClientError as err:
       print("Unexpected error:", str(err))
    
