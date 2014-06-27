# -*- coding: utf-8 -*-
from yss.controller.Common import *

@app.route('/showcontent/<type>')
def showContents(type=None):
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    contentName = u"书籍"
    if type == BaseModel.content_type_book:
        contentName = u"书籍"
    elif type == BaseModel.content_type_music:
        contentName = u"音乐"
    else:
        contentName = u"讲座"

    print type
    entries = Content.readFromDatabaseWithType(type)
    return render_template('show_entries.html', entries=entries, contentName=contentName, contentType=type)

@app.route('/delete_content/<id>')
def deleteContent(id=None):
    content = Content.contentWithId(id)
    content.delete()
    Chapter.deleteChaptersWithContentId(id)
    return redirect(url_for('showContents'))

@app.route('/content/<id>', methods=['GET'])
def showContent(id=None):
    content = Content.contentWithId(id)
    relateList = content.relatedContentList
    relateIds = relateList.split(',')

    relateNames = list()
    for cotentId in relateIds:
        if cotentId != u'':
            relateContent = Content.contentWithId(cotentId)
            relateNames.append(relateContent.name)

    relateContentsDesc = ''
    if relateNames.count > 0:
        relateContentsDesc = ','.join(relateNames)
    content.relateContentsDesc = relateContentsDesc;

    chapters = Chapter.chaptersWithContentId(id)
    return render_template('content.html', content=content, chapters=chapters)

@app.route('/edit_content/<id>', methods=['POST','GET'])
def editContentInfo(id=None):
    if not session.get('logged_in'):
        abort(401)

    content = Content.contentWithId(id)
    if request.method == 'POST':
        form = request.form
        content.name = form['contentName']
        content.author = form['contentAuthor']
        content.desc = form['contentDesc']
        content.save()
        return redirect(url_for('showContent', id = id))
    else:
        return render_template('contentInfo.html', content=content)

@app.route('/add_content', methods=['POST'])
def addContent():
    if not session.get('logged_in'):
        abort(401)

    content = Content()
    content.setFromRequest()
    content.save();

    flash("item created")
    return redirect(url_for('showContents', type=content.type))

@app.route('/relate_content/<id>', methods=['GET','POST'])
def showRelateContent(id=None):
    if request.method == 'GET':
        content = Content.contentWithId(id)
        relateList = content.relatedContentList
        relateIds = relateList.split(',')
        print relateIds
        entries = Content.readFromDatabaseWithType(content.type)
        for content in entries:
            print content.contentId
            contentId = "%s" % content.contentId
            if contentId in relateIds:
                content.selected = True
            else:
                content.selected = False

        title = u"%s:相关内容 %s" %  (content.name, id)
        return render_template('relateContent.html',id=id, title=title, entries=entries)
    else:
        content = Content.contentWithId(id)
        form = request.form
        relateItems = list()
        for k in form:
            if form[k] == 'on':
                relateItems.append(k);
        relateDesc = ','.join(relateItems)
        content.relatedContentList = relateDesc;
        content.save();
        return redirect(url_for('showContent', id = id))
