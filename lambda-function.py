from microservice import Microservice, current_request
import json

# this store is only persistent for each instance of the function!
store = {}

app = Microservice()

@app.handler
def main():
    """
    Get or update resource from store
    """
    request = current_request()
    if request.method == "GET":
        return store[request.args.get("key")]
    elif request.method == "POST":
        body = request.get_json()
        key = body.get("key")
        value = body.get("value")
        store[key] = value
        return {"key": key, "value": value}

def lambda_handler(event, context):
    """
    Handle trigger from API Gateway, process request and return results
    """
    return app.handle_request(event)
