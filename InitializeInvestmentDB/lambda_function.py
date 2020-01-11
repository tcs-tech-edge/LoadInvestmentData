
import json
from urllib.parse import unquote_plus
import boto3
import csv
import sys
import uuid
import requests
import time
from botocore.exceptions import ClientError

print('Loading function')

def lambda_handler(event, context):
    region='us-east-2'
    
    try:
        dyndb = boto3.client('dynamodb', region_name=region)
        dyndbResource = boto3.resource('dynamodb')
        
        investmentPortfolioTable = dyndbResource.Table('investment_portfolio')
        response = investmentPortfolioTable.scan()
        items = response['Items']
       
        uniqueTickers = [];
        for i in items:
            if(i["ticker"] not in uniqueTickers):
                 uniqueTickers.append(i["ticker"]);
        counter = 1
        for item in uniqueTickers:
            print(item)
            res = requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol='+item+'&apikey=W03G1YF4WE1KCNQ5')
            resJson = res.json()
            
            for dt in resJson["Time Series (Daily)"]:
                #print(resJson["Time Series (Daily)"][dt]["4. close"]);
                response = dyndb.put_item(
                    TableName='historical_ticker_data',
                    Item={
                    'tickerName': {'S': resJson["Meta Data"]["2. Symbol"]},
                    'tickerPrice' : {'N':resJson["Time Series (Daily)"][dt]["4. close"]},
                    'tickerDate' : {'S':dt}
                    }
                )
            if counter == 5:
                counter = 1
                time.sleep(60)
            else:
                counter = counter + 1;    
            print('Put succeeded:')
        # TODO implement
        return {
            'statusCode': 200,
            'body': json.dumps('Historical Stock Data is Successfully loaded in the DynamoDB!')
            }
    
    except ClientError as err:
       print("Unexpected error:", str(err))
       return {
            'statusCode': 500,
            'body': json.dumps('Historical Stock Data load Failed!')
            }


