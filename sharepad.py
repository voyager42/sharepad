from __future__ import with_statement
from contextlib import closing
import sqlite3
from flask import Flask, flash, redirect, render_template, request, url_for, session, g
from collections import defaultdict

# TODO: store this in a common locatio
# configuration
DATABASE = 'sharepad.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

app = Flask(__name__)
app.config.from_object(__name__)

def connect_db():
    """Returns a new connection to the database."""
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    """Creates the database tables."""
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql') as f:
            db.cursor().executescript(f.read())
        db.commit()


@app.before_request
def before_request():
    """Make sure we are connected to the database each request."""
    g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'db'):
        g.db.close()
        
@app.route('/')
def index():
    return render_template('app.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or \
                request.form['password'] != 'secret':
            error = 'Invalid credentials'
        else: 
            session['username'] = request.form['username']
            flash('You were successfully logged in')
            return redirect(url_for('index'))
    return render_template('login.html', error=error)

# @app.route('/hello')
# def hello():
#     return 'Hello World'

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)

@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % username

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id

@app.route('/projects/')
def projects():
    return 'The project page'

@app.route('/about')
def about():
    return 'The about page'

def process_form(form):
    items = defaultdict(list)
    for k in form.keys():
        items[k] = form.getlist(k)
    print "////////////////////////////////////////"    
    print items
    return items

@app.route('/share', methods=['GET', 'POST'])
def share():
    if request.method == 'POST':
        # validate in js?        
        # write to database
        submitted = process_form(request.form)
        return render_template('pizza.html', pizza=submitted)
       #g.db.execute('insert into entries (ingredients) values (?)', [request.form['ingredients']])
    return render_template('share.html')
                               

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.debug = True
    app.run()
