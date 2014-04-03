# -*- coding: utf-8 -*-
from yss.controller.Common import *

@app.route('/collections/')
def showCollections():
    collections = Collection.readFromDatabase();
    return render_template('collections.html', collections=collections)


@app.route('/add_collection', methods=['POST'])
def addCollection():
    if not session.get('logged_in'):
        abort(401)

    collection = Collection()
    collection.setFromRequest()
    collection.save();

    flash( u"专题创建成功" )
    return redirect(url_for('showCollections'))

@app.route('/collection/<id>', methods=['GET'])
def showCollection(id=None):
    if not session.get('logged_in'):
        abort(401)
    collection = Collection.collectionWithId(id)

    contentList = collection.contentList
    contentIds = contentList.split(',')
    contents = list()
    print contentIds
    for id in contentIds:
        if id != u'':
            content = Content.contentWithId(id)
            contents.append(relateContent.name)

    collection.contents = contents
    return render_template('collection.html', collection=collection)
