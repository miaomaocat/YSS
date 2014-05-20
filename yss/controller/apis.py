# -*- coding: utf-8 -*-
from yss.controller.Common import *

try:
    import simplejson as json
except ImportError:
    import json

#apis
@app.route('/api/contents')
def show_contents():
    contents = Content.readFromDatabase()
    books = []
    for content in contents:
        books.append(content.jsondict())

    return  jsonify(books=books)

@app.route('/api/content/<id>', methods=['GET'])
def show_content(id=None):
    content = Content.contentWithId(id)
    return  jsonify(content.jsondict())

@app.route('/api/collection/<id>', methods=['GET'])
def show_collection(id=None):
    collection = Collection.collectionWithId(id)
    return  jsonify(collection.jsondict())

@app.route('/api/collections')
def show_collections():
    collections = Collection.readFromDatabase()
    entries = []
    for collection in collections:
        entries.append(collection.jsondict())
    return  jsonify(collections = entries)
