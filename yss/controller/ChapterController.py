from yss.controller.Common import *

@app.route('/add_chapter', methods=['GET', 'POST'])
def addChapter():
    chapter = Chapter()
    chapter.setFromRequest()
    chapter.save()
    return redirect(url_for('showContent', id = chapter.contentId))
    
