from yss.controller.Common import *

@app.route('/download')
def download(fileName=None):
    if not session.get('logged_in'):
        abort(401)
    else:
        return redirect(url_for('static', filename='files/' + request.args.get('fileName', '')))
