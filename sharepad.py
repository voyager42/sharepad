from __future__ import with_statement

import sqlite3
from flask import Flask, flash, redirect, render_template, request, url_for, session, g
from collections import defaultdict
from sharepad_db import create_tables, init_database, add_pizza, get_pizza_by_id, get_pizza_by_style, get_pizza_count, get_sharepad, process_form, get_pizza_ids, generate_pizza_by_style, get_admin, get_description, is_valid_style, get_random_pizza, is_valid_pizza

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
    create_tables()
    init_database()
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

@app.route('/all')
def all_pizzas():
    pizzas = """<html>"""
    ids = get_pizza_ids()
    for id in ids:
        pizzas += get_description(get_pizza_by_id(id))
        pizzas += """<br>"""
    pizzas+="""</html>"""
    error = None
    return render_template('random.html', pizza=pizzas, error=error)


@app.route('/random')
def random_pizza():
    pizza = get_random_pizza()
    if pizza is None:
        pizza = None
        error = u'Nothing found...'
    else:
        pizza_desc = get_description(pizza)
        error = None
    return render_template('random.html', pizza=pizza_desc, error=error)

@app.route('/generate/<style>')
def generate_type(style):
    if (is_valid_style(style)):
        pizza = generate_pizza_by_style(style)
        error = None
        pizza_desc = get_description(pizza)
    else:
        pizza_desc = ""
        error = "something went wrong"
    return render_template('random.html', pizza=pizza_desc, error=error)


@app.route('/style/<style>')
def random_style(style):
    error = None
    pizza = get_pizza_by_style(style)
    pizza_desc = get_description(pizza)
    if pizza == None:
        error = "Nothing found..."
    return render_template('random.html', pizza=pizza_desc, error=error)


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
        pizza = get_description(get_pizza_by_id(submitted)) 
        return render_template('pizza.html', pizza=pizza)
    return render_template('share.html', sharepad=get_sharepad())

if __name__ == '__main__':
    random.seed()
    app.debug = True
    app.run()
else:
    random.seed()
