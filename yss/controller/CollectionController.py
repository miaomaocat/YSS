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

@app.route('/delete_colletion/<id>')
def deleteCollection(id=None):
    collection = Collection.collectionWithId(id)
    collection.delete()
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
            if content != None:
                contents.append(content)

    collection.contents = contents
    return render_template('collection.html', collection=collection)

@app.route('/collection_contents/<id>', methods=['GET','POST'])
def showCotentsUnderCollection(id=None):
    if not session.get('logged_in'):
        abort(401)
    if request.method == 'GET':
        collection = Collection.collectionWithId(id)
        contents = Content.readFromDatabase()
        contentList = collection.contentList
        relateIds = contentList.split(',')

        contents = Content.readFromDatabase()
        for content in contents:
            contentId = "%s" % content.contentId
            if contentId in relateIds:
                content.selected = True
            else:
                content.selected = False

        return render_template('collectionContents.html',id=id, collection=collection, contents= contents)
    else:
        collection = Collection.collectionWithId(id)
        form = request.form
        collectionName = form['collectionName']
        imageUrl = form['imageUrl']
        collection.name = collectionName
        collection.imageUrl = imageUrl
        relateItems = list()
        for k in form:
            if form[k] == 'on':
                relateItems.append(k);
        relateDesc = ','.join(relateItems)
        collection.contentList = relateDesc;
        collection.save()
        return redirect(url_for('showCollection', id = id))
