# Data Load into DynamoDB

## Steps to Load Data using Lambda Function & S3

1. [ ] Create a s3 bucket
2. [ ] Create a lambda function
3. [ ] Assign a role that have access to dynamodb and s3
4. [ ] Create S3 Lambda trigger
5. [ ] Create s3 bucket policy with this role arn

```javascript
{
    "Version": "2012-10-17",
    "Id": "Policy",
    "Statement": [
        {
            "Sid": "statement",
            "Effect": "Allow",
            "Principal": {
                "AWS": "arn:aws:iam::<Enter Role Here>"
            },
            "Action": "s3:*",
            "Resource": [
                "arn:aws:s3:::finathon/*",
                "arn:aws:s3:::finathon"
            ]
        }
    ]
}
```

* [ ] Test the lambda function


```javascript
{
  "Records": [
    {
      "eventVersion": "2.0",
      "eventSource": "aws:s3",
      "awsRegion": "us-east-1",
      "eventTime": "1970-01-01T00:00:00.000Z",
      "eventName": "ObjectCreated:Put",
      "userIdentity": {
        "principalId": "EXAMPLE"
      },
      "requestParameters": {
        "sourceIPAddress": "127.0.0.1"
      },
      "responseElements": {
        "x-amz-request-id": "EXAMPLE123456789",
        "x-amz-id-2": "EXAMPLE123/5678abcdefghijklambdaisawesome/mnopqrstuvwxyzABCDEFGH"
      },
      "s3": {
        "s3SchemaVersion": "1.0",
        "configurationId": "testConfigRule",
        "bucket": {
          "name": "finathon",
          "ownerIdentity": {
            "principalId": "EXAMPLE"
          },
          "arn": "arn:aws:s3:::XXXXX"
        },
        "object": {
          "key": "XXXXX.csv",
          "size": 209,
          "eTag": "XXXXXX"
        }
      }
    }
  ]
}
```




