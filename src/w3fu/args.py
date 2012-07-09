import re
from bson.objectid import ObjectId

from w3fu import util


class ArgError(Exception):

    def __init__(self):
        self._contents = dict(error=self._code)

    def dump(self):
        return self._contents

    def __getitem__(self, name):
        return self._contents[name]


class ArgAbsentError(ArgError):

    _code = 'absent'


class ArgSizeError(ArgError):

    _code = 'size'


class ArgTypeError(ArgError):

    _code = 'type'


class ArgRangeError(ArgError):

    _code = 'range'


class SingleArg(object):

    def __init__(self, field, default=None, **custom):
        self._field = field
        self._default = default
        self.custom = custom

    def unpack(self, packed):
        try:
            return self._unpack(packed[self._field])
        except KeyError:
            if self._default is None:
                raise ArgAbsentError
            else:
                return self._default

    def pack(self, value, packed):
        packed[self._field] = self._pack(value)

    def fields(self):
        return [self._field]

    def _pack(self, value):
        return str(value)


class StrArg(SingleArg):

    def __init__(self, field, trim=True, pattern=None,
                 min_size=0, max_size=65535, **custom):
        super(StrArg, self).__init__(field, **custom)
        self._trim = trim
        self._min_size = min_size
        self._max_size = max_size
        self._pattern = pattern
        self._cpattern = pattern and re.compile(pattern)

    def _unpack(self, value):
        if self._trim:
            s = value.strip()
        if not self._min_size <= len(s) <= self._max_size:
            raise ArgSizeError
        if self._pattern is not None and not self._cpattern.match(s):
            raise ArgTypeError
        return s

    def pattern(self):
        return self._pattern or \
            '.{{0},{1}}'.format(self._min_size, self._max_size)


class IntArg(SingleArg):

    def __init__(self, field, min=0, max=None, **custom):
        super(IntArg, self).__init__(field, **custom)
        self._min = min
        self._max = max

    def _unpack(self, value):
        try:
            x = int(value)
        except ValueError:
            raise ArgTypeError
        if ((self._min is not None and x < self._min) or
            (self._max is not None and x > self._max)):
            raise ArgRangeError
        return x

    def pattern(self):
        return '-?\d+'


class BoolArg(SingleArg):

    def __init__(self, field, **custom):
        super(BoolArg, self).__init__(field, default=False, **custom)

    def _unpack(self, value):
        return value and True or False

    def pattern(self):
        return '[01]'


class IdArg(StrArg):

    def __init__(self, field, **custom):
        super(IdArg, self).__init__(field, pattern='[\da-zA-Z_-]{16}',
                                    **custom)

    def _unpack(self, value):
        value = super(IdArg, self)._unpack(value)
        return ObjectId(util.b64d(value))

    def _pack(self, value):
        return util.b64e(value.binary)