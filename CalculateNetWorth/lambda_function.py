
import json
import boto3
import csv
import sys
import uuid
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError

print('Loading function')

def lambda_handler(event, context):
    region='us-east-1'
    recList=[]
    
    try:
        dyndb = boto3.client('dynamodb', region_name=region)
        dyndbResource = boto3.resource('dynamodb')
        
        investmentPortfolioTable = dyndbResource.Table('InvestmentPortfolio')
        tickerTimeSeriesTable = dyndbResource.Table('TickerTimeSeries')
        
        ipResponseAll = investmentPortfolioTable.scan()
        uniqueCustomers = [];
        for i in ipResponseAll['Items']:
            if(i["customerID"] not in uniqueCustomers):
                 uniqueCustomers.append(i["customerID"] );
        
        for customerID in uniqueCustomers:
            ipResponse = investmentPortfolioTable.scan(FilterExpression=Attr("customerID").eq(customerID))
            nwDict = {}
            for i in ipResponse['Items']:
                #print(i['ticker'], ":", i['number_of_shares'])
                ttResponse = tickerTimeSeriesTable.scan(FilterExpression=Attr("tickerName").eq(i['ticker']))
                for t in ttResponse['Items']:
                    # print(t['tickerDate'], ":", t['tickerPrice'])
                    if t['tickerDate'] in nwDict:
                        nwDict[t['tickerDate']] = nwDict[t['tickerDate']] + (t['tickerPrice'] * i['number_of_shares'])
                    else:
                        nwDict[t['tickerDate']] = (t['tickerPrice'] * i['number_of_shares'])
            
            for x, y in nwDict.items():
                dyndb.put_item(
                        TableName='NetWorth',
                        Item={
                        'customerID': {'S': customerID},
                        'insertDate' : {'S': x},
                        'totalAmount' : {'S': str(y)}
                        }
                    )    
      
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


