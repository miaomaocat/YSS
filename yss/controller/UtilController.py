# -*- coding: utf-8 -*-
from yss.controller.Common import *
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = 'yss/static/Uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


@app.route('/download/<chapterId>')
def download(chapterId=None):
    if not session.get('logged_in'):
        abort(401)
    else:
        chapter = Chapter.chapterWithId(chapterId)
        contentId = str(chapter.contentId)
        chapterId = str(chapter.chapterId)
        chapterFileName = chapter.chapterFileName

        dir = os.path.join('Uploads', contentId)
        dir = os.path.join(dir, chapterId)
        dir = os.path.join(dir, chapterFileName)
        return redirect(url_for('static', filename=dir))

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if not session.get('logged_in'):
        abort(401)
    else:
        f = request.files['file']
        contentId = request.form['contentId']
        chapterId = request.form['chapterId']
        chapterName = request.form['chapterName']
        fname = secure_filename(f.filename)

        chapter = Chapter.chapterWithId(chapterId)
        chapter.chapterFileName = fname
        chapter.save()

        dir = os.path.join(UPLOAD_FOLDER, contentId)
        dir = os.path.join(dir, chapterId)

        # check dir
        if not os.path.isdir(dir):
            os.makedirs(dir)

        dir = os.path.join(dir, fname)
        f.save(dir)
        return redirect(url_for('showChapter', id = chapterId))
