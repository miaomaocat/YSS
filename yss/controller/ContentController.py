from yss.controller.Common import *

@app.route('/')
def showContents():
    entries = Content.readFromDatabase()
    return render_template('show_entries.html', entries=entries)

@app.route('/content/<id>', methods=['GET'])
def showContent(id=None):
    content = Content.contentWithId(id)
    chapters = Chapter.chaptersWithContentId(id)
    return render_template('content.html', content=content, chapters=chapters)

@app.route('/addContent', methods=['POST'])
def addContent():
    if not session.get('logged_in'):
        abort(401)

    content = Content()
    content.setFromRequest()
    content.save();

    flash("item created")
    return redirect(url_for('showContents'))
