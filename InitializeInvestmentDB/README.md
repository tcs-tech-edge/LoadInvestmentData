

Setup Instructions:
1 - Create a new lambda function with a security role that have access to Dynamodb
2 - Zip this folder and upload it to the lamda function
3 - Create a new DynamoDB table called TickerTimeSeries
4 - Expose this lamda function as a service so we can trigger it before the application startup


Order of running this setup:

1 - First upload the csv file into the s3 bucket
2 - LoadCSVData Lambda will get triggered
3 - Run InitializeInvestmentDB function
4 - Run CalculateNetWorth function

