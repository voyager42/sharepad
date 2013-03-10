from __future__ import with_statement
from contextlib import closing
import sqlite3
import datetime
from collections import defaultdict

# TODO: store this in a common location
# configuration
DATABASE = 'sharepad.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

# name, display_name
ingr_types = [
   ["pizza_base", "Pizza Base"],
   ["extra_cheese", "Extra Cheese"],
   ["meat_fish_and_poultry", "Meat, Fish and Poultry"],
   ["veggies", "Veggies"],
   ["herbs", "Herbs"],
   ["sweets", "Sweets"],
]

# name, display_name, ingr_type
ingredients = [
# Pizza Base
   ["margherita", "Margherita", "pizza_base"],
   ["mini_margherita", "Mini Margherita", "pizza_base"],
   ["gluten_free", "Gluten Free", "pizza_base"],
   ["wholewheat", "Wholewheat", "pizza_base"],
   ["chakalaka", "Chakalaka", "pizza_base"],
   ["garlic_focaccia", "Garlic Focaccia", "pizza_base"],
   ["cheese_foccacia", "Cheese Focaccia", "pizza_base"],
   ["herb_foccacia", "Herb Focaccia", "pizza_base"],
   ["pizza_wrap", "Pizza Wrap", "pizza_base"],
   ["rosso", "Rosso", "pizza_base"],
   ["nutella", "Nutella", "pizza_base"],

# Extra Cheese
    ["cheddar", "Cheddar", "extra_cheese"],
    ["feta", "Feta", "extra_cheese"],
    ["gorgonzola", "Gorgonzola", "extra_cheese"],
    ["haloumi", "Haloumi", "extra_cheese"],
    ["mozzarella", "Mozzarella", "extra_cheese"],
    ["mini_mozzarella", "Mini Mozzarella", "extra_cheese"],
    ["parmigiano", "Parmigiano", "extra_cheese"],

# Fish, Meat and Poultry
    ["anchovies", "Anchovies", "meat_fish_and_poultry"],
    ["bacon", "Bacon", "meat_fish_and_poultry"],
    ["biltong", "Biltong", "meat_fish_and_poultry"],
    ["chourico", "Chourico", "meat_fish_and_poultry"],
    ["egg_x2", "Egg [x2]", "meat_fish_and_poultry"],
    ["ham", "Ham", "meat_fish_and_poultry"],
    ["lamb", "Lamb", "meat_fish_and_poultry"],
    ["mince", "Mince", "meat_fish_and_poultry"],
    ["parma_ham", "Parma Ham", "meat_fish_and_poultry"],
    ["salami", "Salami", "meat_fish_and_poultry"],
    ["spare_ribs", "Spare Ribs", "meat_fish_and_poultry"],
    ["spicy_chicken", "Spicy Chicken", "meat_fish_and_poultry"],
    ["tuna", "Tuna", "meat_fish_and_poultry"],

# Veggies
    ["almonds_roasted", "Almonds [Roasted]", "veggies"],
    ["artichokes", "Artichokes", "veggies"],
    ["avocado", "Avocado", "veggies"],
    ["baby_marrow", "Baby Marrow", "veggies"],
    ["bananas", "Bananas", "veggies"],
    ["brinjals", "Brinjals", "veggies"],
    ["capers", "Capers", "veggies"],
    ["caramelised_onions", "Caramelised Onions", "veggies"],
    ["cherry_tomatoes", "Cherry Tomatoes", "veggies"],
    ["green_peppers", "Green Peppers", "veggies"],
    ["jalapenos", "Jalapenos", "veggies"],
    ["mushrooms", "Mushrooms", "veggies"],
    ["olives", "Olives", "veggies"],
    ["onions", "Onions", "veggies"],
    ["peppadews", "Peppadews", "veggies"],
    ["pineapple", "Pineapple", "veggies"],
    ["sesame_seeds", "Sesame Seeds", "veggies"],
    ["spinach", "Spinach", "veggies"],
    ["sundried_tomatoes", "Sundried Tomatoes", "veggies"],

# Herbs
    ["basil", "Basil", "herbs"],
    ["chillies", "Chillies", "herbs"],
    ["chives", "Chives", "herbs"],
    ["coriander", "Coriander", "herbs"],
    ["garlic", "Garlic", "herbs"],
    ["roasted_garlic", "Roasted Garlic", "herbs"],
    ["rocket", "Rocket", "herbs"],
    ["rosemary", "Rosemary", "herbs"],
    ["spring_onions", "Spring Onions", "herbs"],

# Sweets
    ["flake", "Flake", "sweets"],
    ["jelly_tots", "Jelly Tots", "sweets"],
    ["marshmallows", "Marshmallows", "sweets"],
    ["oreo_biscuits", "Oreo Biscuits", "sweets"],
    ["peppermint_aero", "Peppermint Aero", "sweets"],
    ["smarties", "Smarties", "sweets"],
    ["whispers", "Whispers", "sweets"],
    ["100s_and_1000s", "100's & 1000's", "sweets"]
]


def create_ingredienttypes_table():
    con = connect_db()
    with con:
        cur = con.cursor()
        cur.execute("DROP TABLE IF EXISTS IngredientTypes;")
        cur.execute("CREATE TABLE IngredientTypes (Id INTEGER PRIMARY KEY AUTOINCREMENT, Name TEXT, DisplayName TEXT);")

def init_ingredienttypes_table():
    con = connect_db()
    with con:
        cur = con.cursor()
        for i in ingr_types:
            t = (i[0], i[1])
            cur.execute("INSERT INTO Ingredienttypes (Name, DisplayName) VALUES (?, ?);", t)
            print " %s : %s" % (cur.lastrowid, t)

def get_ingredienttype_id(ingredienttype):
    print "Looking for Ingredient Type" + ingredienttype
    con = connect_db()
    with con:
        cur = con.cursor()
        cur.execute("SELECT Id FROM IngredientTypes WHERE Name=?", (ingredienttype,))
        id = cur.fetchone()
        print "%s : %s" % (ingredienttype, id[0])
        return id[0]

def create_ingredients_table():
    con = connect_db()
    with con:
        cur = con.cursor()
        cur.execute("DROP TABLE IF EXISTS Ingredients;")
        cur.execute("CREATE TABLE Ingredients (Id INTEGER PRIMARY KEY AUTOINCREMENT, Name TEXT, DisplayName TEXT, Type INTEGER, FOREIGN KEY (Type) REFERENCES IngredientTypes(Id));")

def init_ingredients_table():
    con = connect_db()
    with con:
        cur = con.cursor()
        for i in ingredients:
            t = (i[0], i[1], get_ingredienttype_id(i[2]))
            cur.execute("INSERT INTO Ingredients (Name, DisplayName, Type) VALUES (?, ?, ?);", t)
            print " %s : %s" % (cur.lastrowid, t)
 
def get_ingredient_id(ingredient):
    print ingredient
    print "Looking for Ingredient " + ingredient
    con = connect_db()
    with con:
        cur = con.cursor()
        cur.execute("SELECT Id FROM Ingredients WHERE Name=?", (ingredient,))
        id = cur.fetchone()
        print "%s : %s" % (ingredient, id[0])
        return id[0]
       
def create_pizzasingredients_table():
    con = connect_db()
    with con:
        cur = con.cursor()
        cur.execute("DROP TABLE IF EXISTS PizzasIngredients;")
        cur.execute("CREATE TABLE PizzasIngredients (Pizza INTEGER, Ingredient INTEGER, FOREIGN KEY (Pizza) REFERENCES Pizzas (Id), FOREIGN KEY (Ingredient) REFERENCES Ingredients (Id));")

def create_pizzas_table():
    con = connect_db()
    with con:
        cur = con.cursor()
        cur.execute("DROP TABLE IF EXISTS Pizzas;")
        cur.execute("CREATE TABLE Pizzas (Id INTEGER PRIMARY KEY AUTOINCREMENT, CreatedOn DATE, CreatedBy TEXT);")

def add_pizza(pizza):
    pizza_id = None
    con = connect_db()
    now = datetime.datetime.now()
    with con:
        cur = con.cursor()
        t = (now, "TESTUSER")
        cur.execute("INSERT INTO Pizzas (CreatedOn, CreatedBy) VALUES (?, ?);", t)
        print "Created pizza %s" % (cur.lastrowid)
        pizza_id = cur.lastrowid
        for k in pizza.keys():
            print "%s : %s" %(k, pizza[k])
            for i in pizza[k]:
                t = [pizza_id, get_ingredient_id(i)]
                cur.execute("INSERT INTO PizzasIngredients (Pizza, Ingredient) VALUES (?, ?);", t)

    return pizza_id    

def get_pizza(pizza_id):
    con = connect_db()
    con.row_factory = sqlite3.Row 

    now = datetime.datetime.now()
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM Pizzas WHERE Id=?;", (pizza_id,))
        p = cur.fetchone()
        pizza = defaultdict(list)        
        # pizza['id'] = p['Id']
        # pizza['created_on'] = p['CreatedOn']
        # pizza['created_by'] = p['CreatedBy']
        cur.execute("SELECT it.Name as category, i.Name as ingredient FROM PizzasIngredients as pi JOIN Ingredients as i ON pi.Ingredient=i.Id JOIN IngredientTypes as it ON Type=it.Id WHERE pi.Pizza=?;", (pizza_id,))
        rows = cur.fetchall()
        ingredients = defaultdict(list)
        for row in rows:
            ingredients[row['category']].append(row['ingredient'])
        # dump return value
        # for k in ingredients.keys():
        #     print "%s : %s" %(k, ingredients[k])
    return ingredients    

def get_pizza_count():
    con = connect_db()
    now = datetime.datetime.now()
    with con:
        cur = con.cursor()
        cur.execute("SELECT COUNT(*) FROM Pizzas;");
        count = cur.fetchone()[0]
    return count

def connect_db():
    return sqlite3.connect(DATABASE)

def create_db():
    """Create the database tables"""
    create_ingredienttypes_table()
    create_ingredients_table()
    create_pizzas_table()
    create_pizzasingredients_table()

def init_db():
    """Initialise the database"""
    init_ingredienttypes_table()
    init_ingredients_table()

def show_ingredients():
    con = connect_db()
    with con:
        cur = con.cursor()    
        cur.execute("SELECT * FROM Ingredients;")
        rows = cur.fetchall()
        for row in rows:
            print row

    

def main():
    create_db()
    init_db()

if __name__ == "__main__":
    main()
