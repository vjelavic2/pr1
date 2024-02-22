from flask import Flask, render_template, request, redirect, url_for
from flask import session

app = Flask(__name__)

users = {
    'user1': {'username': 'user1', 'password': 'password1'},
    'user2': {'username': 'user2', 'password': 'password2'}
}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username]['password'] == password:
            return redirect(url_for('page1', username=username))
        elif username in users and users[username]['password'] == password:
            session['logged_in'] = True
            session['username'] = username
        else:
            return render_template('login.html', message='Invalid username or password.')
    return render_template('login.html', message='')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users:
            return render_template('signup.html', message='Username already exists.')
        else:
            users[username] = {'username': username, 'password': password}
            return redirect(url_for('login'))
    return render_template('signup.html', message='')


@app.route('/page1/<username>')
def page1(username):
    return render_template('page1.html', username=username)


if __name__ == '__main__':
    app.run(debug=True)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    return redirect(url_for(''))
