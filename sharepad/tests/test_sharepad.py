from __future__ import with_statement
from contextlib import closing
import sqlite3
# from nose import with_setup
from sharepad import sharepad_db
from sharepad import server

def make_pizza():
    sharepad_db.add_pizza(sharepad_db.generate_pizza_by_style('cheesy'))

def clear_db():
    pass

# @with_setup(make_pizza, clear_db)
def test_get_random():
    make_pizza()
    pizza = server.get_random_pizza()
    assert(sharepad_db.is_valid_pizza(pizza))


