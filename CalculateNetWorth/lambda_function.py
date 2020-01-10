
import json
import boto3
import csv
import sys
import uuid
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
from datetime import datetime as dt
from dateutil import parser
from decimal import Decimal

print('Loading function')

def lambda_handler(event, context):
    region='us-east-2'
    recList=[]
    
    try:
        dyndb = boto3.client('dynamodb', region_name=region)
        dyndbResource = boto3.resource('dynamodb')
        
        investmentPortfolioTable = dyndbResource.Table('investment_portfolio')
        tickerTimeSeriesTable = dyndbResource.Table('historical_ticker_data')
        
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
                    if i['sale_date'] == 'N/A':
                        i['sale_date'] = '12/12/2100'
                    if (parser.parse(i['purchase_date']) < parser.parse(t['tickerDate'])) & (parser.parse(i['sale_date']) > parser.parse(t['tickerDate'])):
                        if t['tickerDate'] in nwDict:
                            if i['investment_type'] in nwDict[t['tickerDate']]:
                                nwDict[t['tickerDate']][i['investment_type']] = nwDict[t['tickerDate']][i['investment_type']] + (t['tickerPrice'] * i['number_of_shares'])
                            else:
                                nwDict[t['tickerDate']][i['investment_type']] = (t['tickerPrice'] * i['number_of_shares'])
                        else:
                            nwDict[t['tickerDate']] = {}
                            nwDict[t['tickerDate']][i['investment_type']] = (t['tickerPrice'] * i['number_of_shares'])
            
            for x, y in nwDict.items():
                consolidatedTypeNetWorth = {}
                for k, v in y.items():
                    consolidatedTypeNetWorth.update({k : {"S": str(v)}})
                dyndb.put_item(
                        TableName='customer_net_worth',
                        Item={
                        'customerID': {'S': customerID},
                        'insertDate' : {'S': x},
                        'totalAmount' : {"M": consolidatedTypeNetWorth}
                        }
                    )    
      
      
        # TODO implement
        return {
            'statusCode': 200,
            'body': json.dumps('Net worth Data is Successfully loaded in the DynamoDB!')
            }
    
    except ClientError as err:
       print("Unexpected error:", str(err))
       return {
            'statusCode': 500,
            'body': json.dumps('Net worth Data load Failed!')
            }


