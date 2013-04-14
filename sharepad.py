from __future__ import with_statement
from contextlib import closing
import sqlite3
from flask import Flask, flash, redirect, render_template, request, url_for, session, g
from collections import defaultdict
from sharepad_db import create_db, init_db, add_pizza, get_pizza_by_id, get_pizza_by_type, get_pizza_count, get_sharepad, process_form
from sharepad_db import get_admin
from sharepad_pizza import Pizza

import random
import pretty

# TODO: store this in a common location
# configuration
DATABASE = 'sharepad.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'secret'

app = Flask(__name__)
app.config.from_object(__name__)

def connect_db():
    """Returns a new connection to the database."""
    return sqlite3.connect(app.config['DATABASE'])

def initialise_db():
    """Creates the database tables."""
    create_db()
    init_db()
    # with closing(connect_db()) as db:
    #     with app.open_resource('schema.sql') as f:
    #         db.cursor().executescript(f.read())
    #     db.commit()


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
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
            session['foo'] = "bar"         
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
            session['quux'] = "baz"
        else: 
            session['username'] = "hello" #request.form['username']
            flash('You were successfully logged in')
            return redirect(url_for('index'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    flash('You were logged out')
    return redirect(url_for('index'))

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

@app.route('/random')
def random_pizza():
    count = get_pizza_count()
    if count > 0:
        id = random.randint(1, get_pizza_count())
        pizza = get_pizza_by_id(id) 
    else:
        pizza = None
    return render_template('random.html', pizza=pizza)

@app.route('/type/<type>')
def random_type(type):
    pizza = None
    pizzas = get_pizza_by_type(type)
    if pizzas:
        pizza = random.choice(pizzas)       
        error = None
    else:        
        error = "Nothing found..."
    return render_template('random.html', pizza=pizza, error=error)


@app.route('/admin')
def admin():    
    return render_template('admin.html', admin=get_admin())

@app.route('/about')
def about():
    return 'The about page'



@app.route('/share', methods=['GET', 'POST'])
def share():
    if request.method == 'POST':
        # TODO: validate in js
        # write to database
        submitted = process_form(request.form)
        return render_template('pizza.html', pizza=submitted)
    return render_template('share.html', sharepad=get_sharepad())

if __name__ == '__main__':
    random.seed()
    app.debug = True
    app.run()
else:
    random.seed()
