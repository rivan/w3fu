from datetime import datetime
from uuid import uuid4
from pymongo.errors import DuplicateKeyError

from w3fu import config
from w3fu.storage.errors import storagemethod
from w3fu.storage.documents import Document, Property, ListContainer
from w3fu.data.util import b64e, salted_hash


class Session(Document):

    id = Property('id')
    expires = Property('expires')

    @classmethod
    def new(cls):
        return cls(id=b64e(uuid4().bytes),
                   expires=datetime.utcnow() + config.session_ttl)


class User(Document):

    login = Property('login')
    password = Property('password', [])
    sessions = ListContainer('sessions', Session, [])

    def check_password(self, password):
        return self.password == salted_hash(password, self.password)

    @classmethod
    def new(cls, login, password):
        return cls(login=login, password=salted_hash(password))

    @storagemethod
    def push_session(self, storage, session):
        self.c(storage).update({'_id': self.id},
                               {'$push': {'sessions': session}})

    @classmethod
    @storagemethod
    def pull_session(cls, storage, id):
        cls.c(storage).update({'sessions.id': id},
                              {'$pull': {'sessions': {'id': id}}})

    @classmethod
    @storagemethod
    def ensure_indexes(cls, storage):
        cls.c(storage).ensure_index('login', unique=True)
        cls.c(storage).ensure_index('sessions.id')

    @classmethod
    @storagemethod
    def insert(cls, storage, doc):
        try:
            cls.c(storage).insert(doc, safe=True)
            return True
        except DuplicateKeyError:
            return False

    @classmethod
    @storagemethod
    def find_login(cls, storage, login):
        return cls.c(storage).find_one({'login': login}, as_class=cls)

    @classmethod
    @storagemethod
    def find_valid_session(cls, storage, id, expires):
        return cls.c(storage).find_one({'sessions.id': id,
                                        'sessions.expires': {'$gt': expires}},
                                       as_class=cls)
