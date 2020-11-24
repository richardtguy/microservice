import json

store = {}

def get_resource(key):
    """
    Get resource from store
    """
    return store[key]

def create_resource(key, value):
    """
    Create or update resource in store
    """
    store[key] = value
    return (key, value)

def lambda_handler(event, context):
    """
    Handle trigger from API Gateway, process request and return results
    """
    if event["requestContext"]["http"]["method"] == "GET":
        key = event["queryStringParameters"]["key"]
        try:
            value = get_resource(key)
        except KeyError:
            return {
                "statusCode": 404,
                "body": json.dumps({"message": "Resource not found"})
            }
        return {
            "statusCode": 200,
            "body": json.dumps({"key": key, "value": value})
        }
    elif event["requestContext"]["http"]["method"] == "POST":
        body = json.loads(event["body"])
        (key, value) = create_resource(body["key"], body["value"])
        return {
            "statusCode": 201,
            "body": json.dumps({"key": key, "value": value})
        }
    else:
        return {
            "statusCode": 405,
            "body": json.dumps({"message": "Method not allowed"})
        }
