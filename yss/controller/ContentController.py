# -*- coding: utf-8 -*-
from yss.controller.Common import *

@app.route('/')
def showContents():
    entries = Content.readFromDatabase()
    return render_template('show_entries.html', entries=entries)

@app.route('/content/<id>', methods=['GET'])
def showContent(id=None):
    content = Content.contentWithId(id)
    relateList = content.relatedContentList
    relateIds = relateList.split(',')

    relateNames = list()
    for id in relateIds:
        relateContent = Content.contentWithId(id)
        relateNames.append(relateContent.name)

    relateContentsDesc = ''
    if relateNames.count > 0:
        relateContentsDesc = ','.join(relateNames)
    content.relateContentsDesc = relateContentsDesc;

    chapters = Chapter.chaptersWithContentId(id)
    return render_template('content.html', content=content, chapters=chapters)

@app.route('/add_content', methods=['POST'])
def addContent():
    if not session.get('logged_in'):
        abort(401)

    content = Content()
    content.setFromRequest()
    content.save();

    flash("item created")
    return redirect(url_for('showContents'))

@app.route('/relate_content/<id>', methods=['GET','POST'])
def showRelateContent(id=None):
    if request.method == 'GET':
        content = Content.contentWithId(id)
        relateList = content.relatedContentList
        relateIds = relateList.split(',')
        print relateIds
        entries = Content.readFromDatabase()
        for content in entries:
            print content.contentId
            contentId = "%s" % content.contentId
            if contentId in relateIds:
                content.selected = True
            else:
                content.selected = False

        title = u"%s:相关书籍 %s" %  (content.name, id)
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
        return redirect(url_for('showRelateContent', id = id))
