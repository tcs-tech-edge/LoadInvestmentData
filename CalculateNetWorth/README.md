Intro:
This lambda function creates a consolidated networth for each user for 100 days and persist it in the NetWorth DynamoDb table
100 days data is comming from the API. I did not want to get the past 20 years data ... 

Todo:
I should check the purchase date and if it is on purchase date or after I should calculate the networth.
I should calculate the return percentage for each date by looking at the purchase price

Setup Instructions:
1 - Create a new lambda function with a security role that have access to Dynamodb
2 - Zip this folder and upload it to the lamda function
3 - Create a new DynamoDB table called NetWorth
4 - Expose this lamda function as a service so we can trigger it before the application startup



Order of running this setup:

1 - First upload the csv file into the s3 bucket
2 - LoadCSVData Lambda will get triggered
3 - Run InitializeInvestmentDB function
4 - Run CalculateNetWorth function

