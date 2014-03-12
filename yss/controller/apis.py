from yss import app
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash, jsonify
import sqlite3
from contextlib import closing
try:
    import simplejson as json
except ImportError:
    import json

#apis
@app.route('/api/books')
def show_books():
    if not session.get('logged_in'):
        abort(401)
    cur = g.db.execute('select fileName, description, publish, author, length from books order by id desc')
    entries = [dict(fileName=row[0], description=row[1], publish=row[2], author=row[3], length=row[4]) for row in cur.fetchall()]
    return  jsonify(books = entries)

@app.route('/api/recomands')
def show_recom():
    if not session.get('logged_in'):
        abort(401)
    cur =  g.db.execute('select fileName, description, publish, author, length from books where id in (select bookId from recomandBooks) order by id desc')
    entries = [dict(fileName=row[0], description=row[1], publish=row[2], author=row[3], length=row[4]) for row in cur.fetchall()]
    return  jsonify(books = entries)
