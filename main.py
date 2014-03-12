from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash, jsonify
import sqlite3
from contextlib import closing
try:
    import simplejson as json
except ImportError:
    import json

# config
DATABASE = 'flaskr.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

app = Flask(__name__)
app.debug = True
app.config.from_object(__name__)
app.secret_key = 'N&u\x92\xd3\x0c\xebi\xbd\xd7\xbf&\xc1\xe2]3\xf1I\xc62&\xb1\x88\xea'
# global

@app.route('/api')
def api():
    return "api"

@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])


@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


@app.route('/')
def show_entries():
    cur = g.db.execute('select fileName, description, publish, author, length from books order by id desc')
    entries = [dict(fileName=row[0], description=row[1], publish=row[2], author=row[3], length=row[4]) for row in cur.fetchall()]
    return render_template('show_entries.html', entries=entries)

@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    g.db.execute('insert into books (fileName, description, publish, author, length) values (?, ?, ?, ?, ?)',
                 [request.form['fileName'], request.form['description'], request.form['publish'], request.form['author'], request.form['length']])
    g.db.commit()
    flash("item created")
    return redirect(url_for('show_entries'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        cur = g.db.execute('select password from users where userName = \'' + request.form['username'] + '\'')
        users = cur.fetchall()
        if not users :
            error = 'Invalid username'
        elif users[0][0] != request.form['password']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            session['user_name'] = request.form['username']
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)

@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        g.db.execute('insert into users (userName, password, nickName, phoneNumber, email, birthDay) values (?, ? , ? , ? , ?, ?)',
            [request.form['username'],
             request.form['password'],
             request.form['nickName'],
             request.form['phoneNumber'],
             request.form['email'],
             request.form['birthDay']])
        g.db.commit()
        flash("register sucessfull")
        return redirect(url_for('login'))        
    else:
        return render_template('register.html', error=error)

@app.route('/_get_current_user')
def get_current_user():
    return jsonify(username = session.get('user_name'))

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))

@app.route('/download')
def download(fileName=None):
    if not session.get('logged_in'):
        abort(401)
    else:
        return redirect(url_for('static', filename='files/' + request.args.get('fileName', '')))

#apis
@app.route('/api/books')
def show_books():
    if not session.get('logged_in'):
        abort(401)
    cur = g.db.execute('select fileName, description, publish, author, length from books order by id desc')
    entries = [dict(fileName=row[0], description=row[1], publish=row[2], author=row[3], length=row[4]) for row in cur.fetchall()]
    return  jsonify(books = entries)

@app.route('/api/recomands')
def show_recom():
    if not session.get('logged_in'):
        abort(401)
    cur =  g.db.execute('select fileName, description, publish, author, length from books where id in (select bookId from recomandBooks) order by id desc')
    entries = [dict(fileName=row[0], description=row[1], publish=row[2], author=row[3], length=row[4]) for row in cur.fetchall()]
    return  jsonify(books = entries)

if __name__ == '__main__':
    app.run()
