from json import dumps

from w3fu.res.middleware import Middleware
from w3fu.data.xml import element


class json(Middleware):

    def _handler(self, res, req, handler):
        resp = handler(res, req)
        if resp.status == 200:
            resp.ctype = 'application/json'
            resp.content = dumps(resp.content)
        return resp


class xml(Middleware):

    def __init__(self, xslt=None):
        self._xslt = xslt

    def _handler(self, res, req, handler):
        resp = handler(res, req)
        t = None if 'no-xslt' in req.query else self._xslt
        ctype = 'application/xml' if t is None else 'text/html'
        if resp.status == 200:
            resp.ctype = ctype
            e = element(res.name(), resp.content)
            resp.content = res.app.xslt.transform(e, t)
        return resp
