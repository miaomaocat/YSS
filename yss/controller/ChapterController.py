# -*- coding: utf-8 -*-
from yss.controller.Common import *

@app.route('/add_chapter', methods=['GET', 'POST'])
def addChapter():
    chapter = Chapter()
    chapter.setFromRequest()
    chapter.save()
    return redirect(url_for('showContent', id = chapter.contentId))

@app.route('/chapter/<id>', methods=['GET'])
def showChapter(id=None):
    chapter = Chapter.chapterWithId(id)
    return render_template('chapter.html', chapter=chapter)

@app.route('/delete_chapter/<id>')
def deleteChapter(id=None):
    chapter = Chapter.chapterWithId(id)
    contentId = chapter.contentId
    chapter.delete()
    return redirect(url_for('showContent', id = contentId))
