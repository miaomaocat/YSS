# -*- coding: utf-8 -*-
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash, jsonify
import sqlite3
from contextlib import closing
try:
    import simplejson as json
except ImportError:
    import json

# config
DATABASE = 'flaskr.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

app = Flask(__name__)
app.debug = True
app.config.from_object(__name__)
app.secret_key = 'N&u\x92\xd3\x0c\xebi\xbd\xd7\xbf&\xc1\xe2]3\xf1I\xc62&\xb1\x88\xea'
# global


def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

import yss.controller.UtilController
import yss.controller.apis
import yss.controller.ContentController
import yss.controller.ChapterController
import yss.controller.UserController
import yss.controller.UserController
import yss.controller.CollectionController

if __name__ == '__main__':
    app.run()
