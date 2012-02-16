from datetime import datetime

from w3fu.base import Response
from w3fu.resources import Middleware

from app import config


class user(Middleware):

    def __init__(self, required=False):
        self._required = required

    def _handler(self, res, req, handler):
        req.ctx.user = None
        session_id = req.cookie.get(config.session_cookie)
        if session_id is not None:
            req.ctx.user = res.ctx.storage.users.find_valid_session(session_id.value,
                                                                    datetime.utcnow())
        if self._required and req.session is None:
            return Response(403)
        resp = handler(res, req)
        if req.ctx.user is not None and resp.status == 200:
            resp.content['user'] = req.ctx.user
        return resp
