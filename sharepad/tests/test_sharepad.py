from __future__ import with_statement
from contextlib import closing
import sqlite3
from nose import with_setup
import sharepad_db as db
import sharepad as sharepad

def make_pizza():
    db.add_pizza(db.generate_pizza_by_style('cheesy'))

def clear_db():
    pass

@with_setup(make_pizza, clear_db)
def test_get_random():
    pizza = sharepad.get_random_pizza()
    assert(db.is_valid_pizza(pizza))


