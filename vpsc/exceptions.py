class APIException(Exception):
    def __init__(self, status, json):
        self.status = status
        self.json = json


def exception_handler(exc):
    if isinstance(exc, APIException):
        if exc.status == 404:
            print(f"error_code：{exc.json['code']}\nmessage:{exc.json['message'] }")
        else:
            print(f"status_code: {exc.status}")
            print(f"content: {exc.json}")
