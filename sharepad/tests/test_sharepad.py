from sharepad import sharepad_db
from sharepad import server


def make_pizza():
    sharepad_db.add_pizza(sharepad_db.generate_pizza_by_style('cheesy'))


def clear_db():
    pass


def test_get_random():
    make_pizza()
    pizza = server.get_random_pizza()
    assert(sharepad_db.is_valid_pizza(pizza))
