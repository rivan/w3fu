# -*- coding: utf-8 -*-
import sys
import MySQLdb
from MySQLdb.cursors import DictCursor

APP_PATH = '/home/nbahob/workspace/w3fu-trunk'

sys.path.append(APP_PATH + '/src')

from w3fu.web import Application
from w3fu.data.xml import XSLT
from w3fu.storage import Storage
from w3fu.storage.dbapi import Connection
from w3fu.storage.orm.auth import Users, Sessions

from w3fu.res import Controller
from w3fu.res.index import Index
from w3fu.res.test import HtmlTest, JsonTest
from w3fu.res.auth import Login, Register


controller = Controller([Index, JsonTest, HtmlTest, Login, Register])

conn_config = {
               'host': 'localhost',
               'db': 'w3fu',
               'user': 'root',
               'passwd': '12345678',
               'cursorclass': DictCursor,
               'use_unicode': True,
               'charset': 'utf8'
               }

storage = Storage(lambda storage: Connection(
                                             storage=storage,
                                             driver=MySQLdb,
                                             config=conn_config,
                                             mappers=(Users, Sessions)
                                             ))

xslt = XSLT(APP_PATH + '/xsl')

app = Application(controller, storage, xslt)
