
class Request(object):
    def __init__(self):
        self.schema = None
        self.userinfo = None
        self.host = None
        self.port = None
        self.path = None
        self.fragment = None
        self.methods = None
        self.args = None
        self.form = None
        self.headers = None
        self.body = None

    def to_dict(self):
        return {
            'schema': self.schema,
            'userinfo': self.userinfo,
            'host': self.host,
            'port': self.port,
            'path': self.path,
            'fragment': self.fragment,
            'methods': self.methods,
            'args': self.args,
            'form': self.form,
            'headers': self.headers,
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


def rule(request, response):
    r = Rule()

    return r.to_dict()
