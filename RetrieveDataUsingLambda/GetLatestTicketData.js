'use strict';
const AWS = require('aws-sdk');

exports.handler = async (event, context) => {
  const documentClient = new AWS.DynamoDB.DocumentClient();

  let responseBody = "";
  let statusCode = 0;
  
  const {  tickerDate } = event.queryStringParameters;

  const params = {
    TableName: "historical_ticker_data",
     KeyConditionExpression: "#tickerDate = :tickerDate",
            ExpressionAttributeNames:{
                "#tickerDate": "tickerDate"
            },
            ExpressionAttributeValues: {
                ":tickerDate": tickerDate
            }
  };

  try {
    const data = await documentClient.query(params).promise();
    responseBody = JSON.stringify(data.Items);
    statusCode = 200;
  } catch(err) {
    responseBody = `Unable to get historical_ticker_data: ${err}`;
    statusCode = 403;
  }

  const response = {
    statusCode: statusCode,
    headers: {
      "Content-Type": "application/json"
    },
    body: responseBody
  };

  return response;
};