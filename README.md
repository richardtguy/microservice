# Overview
Demonstrator of minimal microservice framework using AWS API Gateway, Lambda and in-memory storage.
TODO: Implement persistent storage using e.g. DynamoDB

### Create new AWS Lambda function in the AWS Lambda console
- Lambda > Functions > Create function
- Choose Author from scratch
- Enter function name and choose runtime Python 3.7
- In Runtime Settings, change Handler to name of module (e.g. `microservice.py`).

### Create virtual environment, activate and install dependencies
```
python3 -m venv venv
source venv/bin/activate   
pip install -r requirements.txt
```

### Deactivate, create deployment package and deploy to Lambda
```
deactivate
zip -r deployment-package.zip venv/lib/python3.7/site-packages/.
zip -g deployment-package.zip microservice.py
aws lambda update-function-code --function-name microservice --zip-file fileb://deployment-package.zip
```

### Add API Gateway trigger in the Lambda console
- Add trigger
- Create an API
- API type: HTTP API
- Security: Open (for demo only, or use JWT authentication)
- Note the API endpoint (will be of the form:
[https://some-id.execute-api.aws-region.amazonaws.com/default/microservice](https://<some-id>.execute-api.<aws-region>.amazonaws.com/default/microservice))

Review the logs in Cloudwatch if there are any problems.
