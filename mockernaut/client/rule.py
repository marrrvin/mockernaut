

class InvalidRule(Exception):
    pass


class Request(object):
    def __init__(self):
        self.path = None
        self.methods = None
        self.body = None

    def to_dict(self):
        return {
            'status': self.path,
            'methods': self.methods,
            'body': self.body
        }


class Response(object):
    def __init__(self):
        self.status = None
        self.headers = None
        self.body = None

    def to_dict(self):
        return {
            'status': self.status,
            'headers': self.headers,
            'body': self.body
        }


class Rule(object):
    def __init__(self):
        self.request = Request()
        self.response = Response()

    def to_dict(self):
        return {
            'request': self.request.to_dict(),
            'response': self.response.to_dict()
        }
