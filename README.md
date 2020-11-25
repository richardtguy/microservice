# Overview
Demonstrator of minimal microservice framework using AWS API Gateway, Lambda and in-memory storage.

## Limitations
Note that the AWS API Gateway will only pass through requests to specifically
defined endpoints - by default only /default/<function-name>.

## Setup

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

### Usage

Create the Microservice application object
```python
app = Microservice()
```

Decorate view functions with the corresponding URL and methods
```python
@app.route('/default/microservice', methods=["GET", "POST"])
```

Use `current_request()` to access request data within the view function.
```python
request = current_request()
query = request.args.get("query")
```
