from yss.controller.Common import *

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
    return redirect(url_for('showContents'))
