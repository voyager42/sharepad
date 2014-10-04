import datetime
import itertools
from collections import defaultdict
import random

import sqlite3

from sharepad.ingredients import (
    ingr_types, ingredients, styles, styles_ingredients)

# TODO: store this in a common location
# configuration
DATABASE = 'sharepad.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'secret'


def create_ingredienttypes_table():
    con = connect_db()
    with con:
        cur = con.cursor()
        cur.execute("DROP TABLE IF EXISTS IngredientTypes;")
        cur.execute(
            ("CREATE TABLE IngredientTypes (Id INTEGER PRIMARY KEY "
             "AUTOINCREMENT, Name TEXT, DisplayName TEXT);"))


def init_ingredienttypes_table():
    con = connect_db()
    with con:
        cur = con.cursor()
        for i in ingr_types:
            t = (i[0], i[1])
            cur.execute(
                ("INSERT INTO IngredientTypes (Name, DisplayName) VALUES "
                 "(?, ?);"), t)


def get_ingredienttype_id(ingredienttype):
    con = connect_db()
    with con:
        cur = con.cursor()
        cur.execute(
            "SELECT Id FROM IngredientTypes WHERE Name=?", (ingredienttype,))
        id = cur.fetchone()
        try:
            return id[0]
        except TypeError:
            return None


def create_ingredients_table():
    con = connect_db()
    with con:
        cur = con.cursor()
        cur.execute("DROP TABLE IF EXISTS Ingredients;")
        cur.execute(
            ("CREATE TABLE Ingredients (Id INTEGER PRIMARY KEY AUTOINCREMENT, "
             "Name TEXT, DisplayName TEXT, Type INTEGER, FOREIGN KEY (Type) "
             "REFERENCES IngredientTypes(Id));"))


def init_ingredients_table():
    con = connect_db()
    with con:
        cur = con.cursor()
        for i in ingredients:
            t = (i[0], i[1], get_ingredienttype_id(i[2]))
            cur.execute(
                ("INSERT INTO Ingredients (Name, DisplayName, Type) VALUES "
                 "(?, ?, ?);"), t)


def get_ingredient_id(ingredient):
    con = connect_db()
    with con:
        cur = con.cursor()
        cur.execute("SELECT Id FROM Ingredients WHERE Name=?", (ingredient,))
        id = cur.fetchone()
        if id is None:
            print "Ingredient %s not found in db" % (ingredient,)
        return id[0]


def create_pizzasingredients_table():
    con = connect_db()
    with con:
        cur = con.cursor()
        cur.execute("DROP TABLE IF EXISTS PizzasIngredients;")
        cur.execute(
            ("CREATE TABLE PizzasIngredients (Pizza INTEGER, Ingredient "
             "INTEGER, FOREIGN KEY (Pizza) REFERENCES Pizzas (Id), FOREIGN "
             "KEY (Ingredient) REFERENCES Ingredients (Id));"))


def create_pizzas_table():
    con = connect_db()
    with con:
        cur = con.cursor()
        cur.execute("DROP TABLE IF EXISTS Pizzas;")
        cur.execute(
            ("CREATE TABLE Pizzas (Id INTEGER PRIMARY KEY AUTOINCREMENT, "
             "CreatedOn DATE, CreatedBy TEXT, Style INTEGER, FOREIGN KEY "
             "(Style) REFERENCES Styles (Id));"))


def init_styles_table():
    con = connect_db()
    with con:
        cur = con.cursor()
        for i in styles:
            t = (i[0], i[1])
            cur.execute(
                "INSERT INTO Styles (Name, DisplayName) VALUES (?, ?);", t)


def create_styles_ingredients_table():
    con = connect_db()
    with con:
        cur = con.cursor()
        cur.execute("DROP TABLE IF EXISTS StylesIngredients;")
        cur.execute(
            ("CREATE TABLE StylesIngredients (Style INTEGER, Ingredient "
             "INTEGER, FOREIGN KEY (Style) REFERENCES Styles (Id), FOREIGN "
             "KEY (Ingredient) REFERENCES Ingredients (Id));"))


def init_styles_ingredients_table():
    con = connect_db()
    with con:
        cur = con.cursor()
        for i in styles_ingredients:
            for j in styles_ingredients[i]:
                t = (get_style_id(i), get_ingredient_id(j))
                cur.execute(
                    ("INSERT INTO StylesIngredients (Style, Ingredient) "
                     "VALUES (?, ?);"), t)


def add_pizza(pizza):
    pizza_id = None
    con = connect_db()
    now = datetime.datetime.now()
    with con:
        cur = con.cursor()
        t = (now, "TESTUSER", get_style_id(pizza['style']))
        cur.execute(
            ("INSERT INTO Pizzas (CreatedOn, CreatedBy, Style) VALUES "
             "(?, ?, ?);"), t)
        pizza_id = cur.lastrowid
        ingredients = list(
            itertools.chain.from_iterable(pizza['ingredients'].values()))
        for i in ingredients:
            ingr_id = get_ingredient_id(i)
            t = [pizza_id, ingr_id]
            cur.execute(
                ("INSERT INTO PizzasIngredients (Pizza, Ingredient) VALUES "
                 "(?, ?);"), t)
        print pizza
        base = pizza['pizza_base']
        ingr_id = get_ingredient_id(base)
        t = [pizza_id, ingr_id]
        cur.execute(
            "INSERT INTO PizzasIngredients (Pizza, Ingredient) VALUES (?, ?);",
            t)
    return pizza_id


def get_pizza_by_id(pizza_id):
    con = connect_db()
    con.row_factory = sqlite3.Row

    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM Pizzas WHERE Id=?;", (pizza_id,))
        p = cur.fetchone()
        if p is None:
            pizza = None
        else:
            pizza = defaultdict(dict)
            pizza['id'] = p['Id']
            pizza['created_on'] = p['CreatedOn']
            pizza['created_by'] = p['CreatedBy']
            style = p['Style']
            cur.execute(
                ("SELECT it.Name as category, it.DisplayName as "
                 "category_name, i.Name as ingredient FROM PizzasIngredients "
                 "as pi JOIN Ingredients as i ON pi.Ingredient=i.Id JOIN "
                 "IngredientTypes as it ON Type=it.Id WHERE pi.Pizza=?;"),
                (pizza_id,))
            rows = cur.fetchall()
            ingredients = defaultdict(list)
            base = ""
            for row in rows:
                if row['category'] != 'pizza_base':
                    ingredients[row['category']].append(row['ingredient'])
                else:
                    base = row['ingredient']
            pizza['ingredients'] = ingredients
            pizza['pizza_base'] = base
        cur.execute(
            ("SELECT pt.Name as type, pt.Id as id FROM Styles as pt WHERE "
             "pt.Id=?;"), (style,))
        try:
            pizza['style'] = cur.fetchone()[0]
        except:
            pizza['style'] = "UNKNOWN"
    return pizza


def get_pizza_by_style(style):
    con = connect_db()
    con.row_factory = sqlite3.Row

    with con:
        cur = con.cursor()
        cur.execute(
            "SELECT * FROM Pizzas WHERE Style=?;", (get_style_id(style),))
        p = cur.fetchall()
        if p is None:
            pizzas = None
        else:
            pizzas = []
            for pi in p:
                pizza = defaultdict(dict)
                pizza['id'] = pi['Id']
                pizza['created_on'] = pi['CreatedOn']
                pizza['created_by'] = pi['CreatedBy']
                cur.execute(
                    ("SELECT it.DisplayName as category, i.DisplayName as "
                     "ingredient FROM PizzasIngredients as pi JOIN "
                     "Ingredients as i ON pi.Ingredient=i.Id JOIN "
                     "IngredientTypes as it ON Type=it.Id WHERE pi.Pizza=?;"),
                    (pizza['id'],))
                rows = cur.fetchall()
                ingredients = defaultdict(list)
                for row in rows:
                    if row['category'] == 'pizza_base':
                        pizza['pizza_base'] = row['ingredients']
                    else:
                        ingredients[row['category']].append(row['ingredient'])
                pizza['ingredients'] = ingredients
                pizza['style'] = style
    return pizzas


def get_pizza_ids():
    con = connect_db()
    with con:
        cur = con.cursor()
        cur.execute("SELECT Id as id FROM Pizzas;")
        ids = cur.fetchall()
    flatids = [i[0] for i in ids]
    return flatids


def get_pizza_count():
    count = 0
    con = connect_db()
    with con:
        cur = con.cursor()
        cur.execute("SELECT COUNT(*) FROM Pizzas;")
        count = cur.fetchone()[0]
    return count


def create_styles_table():
    con = connect_db()
    with con:
        cur = con.cursor()
        cur.execute("DROP TABLE IF EXISTS Styles;")
        cur.execute(
            ("CREATE TABLE Styles (Id INTEGER PRIMARY KEY AUTOINCREMENT, "
             "Name TEXT, DisplayName TEXT);"))


def init_pizzastyles_table():
    con = connect_db()
    with con:
        cur = con.cursor()
        for i in styles:
            t = (i[0], i[1])
            cur.execute(
                "INSERT INTO Styles (Name, DisplayName) VALUES (?, ?);", t)


def get_style_id(style):
    con = connect_db()
    with con:
        cur = con.cursor()
        cur.execute("SELECT Id FROM Styles WHERE Name=?;", (style,))
        id = cur.fetchone()
        return id[0]


def join_and(items):
    if items:
        if len(items) >= 2:
            joined = "{0} and {1}".format(", ".join(items[:-2]), items[-1])
        else:
            joined = " and ".join(items)
    else:
        joined = ""
    return joined


def get_description(pizza):
    formatted = ""
    if pizza:
        style = pizza['style']
        ingredients = pizza['ingredients']
        base = pizza['pizza_base']  # assume only one pizza base
        extra_cheese = ingredients['extra_cheese']
        meat_fish_and_poultry = ingredients['meat_fish_and_poultry']
        veggies = ingredients['veggies']
        herbs = ingredients['herbs']
        sweets = ingredients['sweets']
        ingrs = extra_cheese + meat_fish_and_poultry + veggies + herbs + sweets
        ingr_display_names = []
        display_names = get_ingr_displaynames()
        for i in ingrs:
            ingr_display_names.append(display_names[i])

        description = join_and(ingr_display_names)
        if description:
            formatted = "{0} base with {1} ({2})".format(
                display_names[base], description, style)

    return formatted


def get_rand_length(l):
    if len(l) > 2:
        return random.randint(1, len(l) - 1)
    else:
        return 1


def generate_pizza_by_style(style):
    con = connect_db()
    con.row_factory = sqlite3.Row
    random.seed()
    with con:
        cur = con.cursor()
        cur.execute(
            ("SELECT i.Id, i.Name as name, i.DisplayName as name, it.Id, "
             "it.Name as type, it.DisplayName FROM StylesIngredients as si "
             "JOIN Ingredients as i ON si.Ingredient=i.Id JOIN "
             "IngredientTypes as it ON i.Type=it.Id WHERE (Style=? AND "
             "it.Name=?);"), (get_style_id(style), 'pizza_base',))
        p = cur.fetchall()
        pb = [i['name'] for i in p]
        pizza_base = random.choice(pb)

        cur.execute(
            ("SELECT i.Id, i.Name as name, i.DisplayName as name, it.Id, "
             "it.Name as type, it.DisplayName FROM StylesIngredients as si "
             "JOIN Ingredients as i ON si.Ingredient=i.Id JOIN "
             "IngredientTypes as it ON i.Type=it.Id WHERE (Style=? AND "
             "it.Name=?);"), (get_style_id(style), 'extra_cheese',))
        p = cur.fetchall()
        ec = [i['name'] for i in p if i['type'] == 'extra_cheese']
        extra_cheese = random.sample(ec, get_rand_length(ec))

        cur.execute(
            ("SELECT i.Id, i.Name as name, i.DisplayName as name, it.Id, "
             "it.Name as type, it.DisplayName FROM StylesIngredients as si "
             "JOIN Ingredients as i ON si.Ingredient=i.Id JOIN "
             "IngredientTypes as it ON i.Type=it.Id WHERE (Style=? AND "
             "it.Name=?);"), (get_style_id(style), 'meat_fish_and_poultry',))
        p = cur.fetchall()
        mfp = [i['name'] for i in p if i['type'] == 'meat_fish_and_poultry']
        meat_fish_and_poultry = random.sample(mfp, get_rand_length(mfp))

        cur.execute(
            ("SELECT i.Id, i.Name as name, i.DisplayName as name, it.Id, "
             "it.Name as type, it.DisplayName FROM StylesIngredients as si "
             "JOIN Ingredients as i ON si.Ingredient=i.Id JOIN "
             "IngredientTypes as it ON i.Type=it.Id WHERE (Style=? AND "
             "it.Name=?);"), (get_style_id(style), 'veggies',))
        p = cur.fetchall()
        v = [i['name'] for i in p if i['type'] == 'veggies']
        veggies = random.sample(v, get_rand_length(v))

        cur.execute(
            ("SELECT i.Id, i.Name as name, i.DisplayName as name, it.Id, "
             "it.Name as type, it.DisplayName FROM StylesIngredients as si "
             "JOIN Ingredients as i ON si.Ingredient=i.Id JOIN "
             "IngredientTypes as it ON i.Type=it.Id WHERE (Style=? AND "
             "it.Name=?);"), (get_style_id(style), 'herbs',))
        p = cur.fetchall()

        h = [i['name'] for i in p if i['type'] == 'herbs']
        herbs = random.sample(h, get_rand_length(h))

        # cur.execute(
        #     ("SELECT i.Id, i.Name, i.DisplayName, it.Id, it.Name, "
        #      "it.DisplayName FROM StylesIngredients as si JOIN Ingredients "
        #      "as i ON si.Ingredient=i.Id JOIN IngredientTypes as it ON "
        #      "i.Type=it.Id WHERE (Style=? AND it.Name=?);"),
        #     (get_style_id(style), 'sweets',))
        # p = cur.fetchall()

        # sw = [i[1] for i in p if  i[4]=='sweets']
        # try:
        #     sweets = random.sample(sw, get_rand_length(sw))
        # except:
        sweets = []

        pizza = defaultdict(dict)
        pizza['pizza_base'] = pizza_base
        pizza['ingredients'] = defaultdict(list)
        pizza['ingredients']['veggies'] = veggies
        pizza['ingredients']['meat_fish_and_poultry'] = meat_fish_and_poultry
        pizza['ingredients']['extra_cheese'] = extra_cheese
        pizza['ingredients']['herbs'] = herbs
        pizza['ingredients']['sweets'] = sweets
        pizza['style'] = style
        pizza['created_on'] = datetime.datetime.now()
        pizza['created_by'] = "GENERATED"

    return pizza


def get_sharepad():
    """returns a dict which is useful for generating the sharepad form"""
    sharepad = {}
    con = connect_db()
    con.row_factory = sqlite3.Row
    with con:
        cur = con.cursor()
        cur.execute(
            ("SELECT Name as name, DisplayName as display_name FROM "
             "IngredientTypes;"))
        rows = cur.fetchall()
        sharepad['groups'] = rows
        cur.execute(
            ("SELECT DISTINCT i.Name as name, i.DisplayName as display_name, "
             "it.Name as type_name, it.DisplayName as type_display_name FROM "
             "Ingredients as i JOIN IngredientTypes as it ON it.Id=i.Type;"))
        rows = cur.fetchall()
        i = 1
        elements = []
        prev_type_name = None
        for r in rows:
            item = {}
            for k in ['name', 'display_name', 'type_name']:
                item[k] = r[k]
            # convert number to 0 padded string of length 3
            item['id'] = "{0}_{1:03d}".format(r['type_name'], i)
            elements.append(item)
            if prev_type_name == r['type_name'] or prev_type_name is None:
                i = i + 1
            else:
                i = 1
                prev_type_name = r['type_name']
        sharepad['elements'] = elements

        cur.execute(
            "SELECT Name as name, DisplayName as display_name FROM Styles;")
        rows = cur.fetchall()
        styles = []
        for r in rows:
            item = {}
            item['name'] = r['name']
            item['display_name'] = r['display_name']
            # print "{0}  {1}".format(item['name'], item['display_name'])
            styles.append(item)
        sharepad['styles'] = styles
    return sharepad


def get_admin():
    admin = {}
    con = connect_db()
    con.row_factory = sqlite3.Row
    with con:
        cur = con.cursor()
        cur.execute(
            "SELECT Name as name, DisplayName as display_name FROM Styles;")
        rows = cur.fetchall()
    admin['styles'] = rows

    return admin


def connect_db():
    return sqlite3.connect(DATABASE)


def create_tables():
    """Create the database tables"""
    create_ingredienttypes_table()
    create_ingredients_table()
    create_styles_table()
    create_pizzas_table()
    create_pizzasingredients_table()
    create_styles_ingredients_table()


def init_database():
    """Initialise the database"""
    init_ingredienttypes_table()
    init_ingredients_table()
    init_styles_table()
    init_styles_ingredients_table()


def show_ingredients():
    con = connect_db()
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM Ingredients;")
        rows = cur.fetchall()
        for row in rows:
            print row


def process_form(form):
    ingredient_types = [i[0] for i in ingr_types]
    pizza = defaultdict(dict)
    pizza['ingredients'] = defaultdict(list)
    for i in ingredient_types:
        pizza['ingredients'][i] = form.getlist(i)
    pizza['style'] = form.getlist('style')[0]
    id = add_pizza(pizza)
    return id


def get_styles():
    return styles


def get_bases():
    # TODO: get bases from db
    return [i[0] for i in ingredients if i[2] == 'pizza_base']


def get_ingredient_types():
    # TODO: get ingr_types from db
    return [i[0] for i in ingr_types]


def get_random_pizza():
    count = get_pizza_count()
    pizza = None
    if count > 0:
        ids = get_pizza_ids()
        id = random.choice(ids)
        pizza = get_pizza_by_id(id)
    return pizza


def get_ingr_displaynames():
    con = connect_db()
    con.row_factory = sqlite3.Row
    with con:
        cur = con.cursor()
        cur.execute(
            ("SELECT Name as name, DisplayName as display_name FROM "
             "Ingredients;"))
        rows = cur.fetchall()
        ingr_displaynames = {}
        for r in rows:
            ingr_displaynames[r['name']] = r['display_name']
    return ingr_displaynames


def is_valid_base(base):
    return base in get_bases()


def is_valid_style(style):
    return style in [i[0] for i in get_styles()]


def is_valid_pizza(pizza):
    assert(pizza.get('created_on') is not None)
    assert(pizza.get('created_by') is not None)

    assert('ingredients' in pizza)
    assert('pizza_base' in pizza)
    assert(is_valid_base(pizza['pizza_base']))
    assert('extra_cheese' in pizza['ingredients'])
    assert('meat_fish_and_poultry' in pizza['ingredients'])
    assert('veggies' in pizza['ingredients'])
    assert('herbs' in pizza['ingredients'])
    assert('style' in pizza)
    style = pizza['style']
    try:
        assert(is_valid_style(style))
    except:
        print style
#    print db.get_description(pizza)
    for ingredient_type in get_ingredient_types():
        for ingredient in pizza['ingredients'][ingredient_type]:
            try:
                # TODO: get styles_ingredients from db
                assert(ingredient in styles_ingredients[style])
            except:
                print "ingredient {0} is not in style {1}".format(
                    ingredient, style)
            assert(get_ingredient_id(ingredient) is not None)

    return True


def main():
    create_tables()
    init_database()


if __name__ == "__main__":
    main()
