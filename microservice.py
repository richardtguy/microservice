import json
import logging

logger = logging.getLogger('microservice')
logger.setLevel(logging.DEBUG)

class Request():
    """
    The request context, accesible inside functions decorated with the route decorator
    """
    def __init__(self, method, headers, path, queryStringParameters=None, body=None):
        self.method = method
        self.path = path
        self.headers = headers
        self.args = queryStringParameters
        self.body = body

    def get_json(self):
        if self.headers["content-type"] == "application/json":
            return json.loads(self.body)
        else:
            return None

class Microservice():
    """
    Minimal request handler for web microservices
    """
    def __init__(self, config=None, request_type="AWS_HTTP_API"):
        self.routes = {}
        self.request = None
        if request_type == "AWS_HTTP_API":
            self.handle_request = self._handle_aws_http_request

    def _handle_aws_http_request(self, event):
        """
        Parse request context from AWS API Gateway event and update the global
        request object before calling the generic request handler
        """
        global request
        request = Request(
            event["requestContext"]["http"]["method"],
            event["headers"],
            event["requestContext"]["http"]["path"],
            queryStringParameters = event.get("queryStringParameters"),
            body = event.get("body")
        )
        return self._handle_request()

    def _handle_request(self):
        """
        Handle a generic request by calling the corresponding view function
        """
        try:
            route = self.routes[request.path]
        except KeyError:
            return {
                "statusCode": 404,
                "body": json.dumps({"message": "Resource not found"})
            }
        if request.method not in route["methods"]:
            return {
                "statusCode": 405,
                "body": json.dumps({"message": "Method not allowed"})
            }
        result = route["func"]()
        return {
            "statusCode": 200,
            "body": json.dumps(result)
        }

    def route(self, path, methods=["GET"]):
        """
        A decorator that is used to register a function for a given path
        """
        def decorator(func):
            self._register_url(func, path, methods=methods)
            return func
        return decorator

    def _register_url(self, func, path, methods):
        """
        Map a function to a given url for specified methods
        """
        self.routes[path] = {"func": func, "methods": methods}

def current_request():
    """
    Return the current request context
    """
    return request

# Initialise global request context
request = None
