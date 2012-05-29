from Cookie import SimpleCookie, CookieError, Morsel
from cgi import FieldStorage
from Cookie import Morsel


class Context(dict):

    def __getattr__(self, name):
        return self[name]

    def __setattr__(self, name, value):
        self[name] = value


class Application(object):

    def __init__(self, context, handler):
        self.ctx = context
        self._handler = handler

    def __call__(self, environ, start_response):
        ctx = Context(req=Request(environ))
        resp = self._handler(ctx)
        return resp(start_response)

    def debug(self, environ):
        def start_response(status, headers):
            print(status)
            for name, value in headers:
                print('{0}: {1}'.format(name, value))
        for data in self(environ, start_response):
            print
            print(data)


class Request(object):

    def __init__(self, environ):
        self.environ = environ

    @property
    def scheme(self):
        return self.environ.get('wsgi.url_scheme', 'http')

    @property
    def host(self):
        return self.environ.get('HTTP_HOST', '')

    @property
    def path(self):
        return self.environ.get('PATH_INFO', '')

    @property
    def referer(self):
        return self.environ.get('HTTP_REFERER')

    @property
    def method(self):
        return self.environ.get('REQUEST_METHOD', '')

    @property
    def cookie(self):
        try:
            return self._cookie
        except AttributeError:
            try:
                cookie = SimpleCookie(self.environ.get('HTTP_COOKIE'))
            except CookieError:
                cookie = {}
            self._cookie = dict((k, v.value) for k, v in cookie.iteritems())
            return self._cookie

    @property
    def fs(self):
        try:
            return self._fs
        except AttributeError:
            self._fs = FieldStorage(fp=self.environ['wsgi.input'],
                                    environ=self.environ,
                                    keep_blank_values=True)
            return self._fs


class Response(object):

    @classmethod
    def ok(cls, content=None, content_type=None):
        return cls(200, 'OK', content, content_type)

    @classmethod
    def redirect(cls, url):
        return cls(302, 'Found').header('Location', url)

    @classmethod
    def bad_request(cls, content=None, content_type=None):
        return cls(400, 'Bad Request', content, content_type)

    @classmethod
    def forbidden(cls):
        return cls(403, 'Forbidden')

    @classmethod
    def not_found(cls):
        return cls(404, 'Not Found')

    @classmethod
    def method_not_allowed(cls):
        return cls(405, 'Method Not Allowed')

    @classmethod
    def conflict(cls, content=None, content_type=None):
        return cls(409, 'Conflict', content, content_type)

    @classmethod
    def unsupported_media_type(cls):
        return cls(415, 'Unsupported Media Type')

    @classmethod
    def internal_server_error(cls, content=None, content_type=None):
        return cls(500, 'Internal Server Error', content, content_type)

    @classmethod
    def unavailable(cls):
        return cls(503, 'Service Unavailable')

    def __init__(self, status=200, reason='OK',
                 content=None, content_type=None):
        self.status = status
        self.reason = reason
        self.content = content
        self.content_type = content_type
        self.headers = []

    def __call__(self, start_response):
        if self.content is not None:
            self.header('Content-Type', self.content_type + '; charset=UTF-8')
        start_response(str(self.status) + ' ' + self.reason, self.headers)
        return [] if self.content is None else [self.content]

    def header(self, name, value):
        self.headers.append((name, value))
        return self

    def set_cookie(self, name, value, expires=None, path='/'):
        morsel = Morsel()
        morsel.set(name, value, str(value))
        morsel['path'] = path
        if expires is not None:
            morsel['expires'] = expires.strftime('%a, %d %b %Y %H:%M:%S GMT')
        self.header('Set-Cookie', morsel.OutputString())
        return self
