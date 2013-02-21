from __future__ import with_statement
from contextlib import closing
import sqlite3

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
    ["herbs", "Herbs", "herbs"],
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


def create_toppingtypes_table():
    con = connect_db()
    with con:
        cur = con.cursor()
        cur.execute("DROP TABLE IF EXISTS ToppingTypes;")
        cur.execute("CREATE TABLE ToppingTypes(Id INTEGER PRIMARY KEY AUTOINCREMENT, Name TEXT, DisplayName TEXT);")

def init_toppingstypes_table():
    con = connect_db()
    with con:
        cur = con.cursor()
        for i in ingr_types:
            t = (i[0], i[1])
            cur.execute("INSERT INTO ToppingTypes (Name, DisplayName) VALUES (?, ?);", t)
            print " %s : %s" % (cur.lastrowid, t)

def get_toppingtype_id(toppingtype):
    print "Looking for " + toppingtype
    con = connect_db()
    with con:
        cur = con.cursor()
        cur.execute("SELECT Id FROM ToppingTypes WHERE Name=?", (toppingtype,))
        id = cur.fetchone()
        print "%s : %s" % (toppingtype, id[0])
        return id[0]

def create_ingredients_table():
    con = connect_db()
    with con:
        cur = con.cursor()
        cur.execute("DROP TABLE IF EXISTS Ingredients;")
        cur.execute("CREATE TABLE Ingredients(Id INTEGER PRIMARY KEY AUTOINCREMENT, Name TEXT, DisplayName TEXT, Type INTEGER, FOREIGN KEY(Type) REFERENCES ToppingTypes(Id));")

def init_ingredients_table():
    con = connect_db()
    with con:
        cur = con.cursor()
        for i in ingredients:
            t = (i[0], i[1], get_toppingtype_id(i[2]))
            cur.execute("INSERT INTO Ingredients (Name, DisplayName, Type) VALUES (?, ?, ?);", t)
            print " %s : %s" % (cur.lastrowid, t)
        


def connect_db():
    return sqlite3.connect(DATABASE)

def create_db():
    """Create the database tables"""
    create_toppingtypes_table()
    create_ingredients_table()

def init_db():
    """Initialise the database"""
    init_toppingstypes_table()
    init_ingredients_table()

def show_ingredients():
    con = connect_db()
    with con:
        cur = con.cursor()    
        cur.execute("SELECT Name FROM ToppingTypes")
        rows = cur.fetchall()
        for row in rows:
            print row[0]

def main():
    create_db()
    init_db()
    show_ingredients()

if __name__ == "__main__":
    main()
