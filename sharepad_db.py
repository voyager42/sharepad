from __future__ import with_statement
from contextlib import closing
import sqlite3
import datetime
import itertools
from collections import defaultdict

# TODO: store this in a common location
# configuration
DATABASE = 'sharepad.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'secret'

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
    ["banana", "Banana", "veggies"],
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

pizza_types = [
    ["italian", "Italian"],
    ["greek", "Greek"],
    ["portuguese", "Portuguese"],
    ["american", "American"],
    ["french", "French"],
    ["english", "English"],
    ["meaty", "Meaty"],
    ["spicy", "Spicy"],
    ["fresh", "Fresh"],
    ["veggie", "Veggie"],
    ["mediterranean", "Mediterranean"],
    ["african", "African"],
    ["cheesy", "Cheesy"],
    ["american", "American"],
    ["tropical", "Tropical"],
    ["healthy", "Healthy"],
    ["crazy", "Crazy"],
    ["fishy", "Fishy"]
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
            cur.execute("INSERT INTO IngredientTypes (Name, DisplayName) VALUES (?, ?);", t)

def get_ingredienttype_id(ingredienttype):
    con = connect_db()
    with con:
        cur = con.cursor()
        cur.execute("SELECT Id FROM IngredientTypes WHERE Name=?", (ingredienttype,))
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
        cur.execute("CREATE TABLE Ingredients (Id INTEGER PRIMARY KEY AUTOINCREMENT, Name TEXT, DisplayName TEXT, Type INTEGER, FOREIGN KEY (Type) REFERENCES IngredientTypes(Id));")

def init_ingredients_table():
    con = connect_db()
    with con:
        cur = con.cursor()
        for i in ingredients:
            t = (i[0], i[1], get_ingredienttype_id(i[2]))
            cur.execute("INSERT INTO Ingredients (Name, DisplayName, Type) VALUES (?, ?, ?);", t)
 
def get_ingredient_id(ingredient):
    con = connect_db()
    with con:
        cur = con.cursor()
        cur.execute("SELECT Id FROM Ingredients WHERE Name=?", (ingredient,))
        id = cur.fetchone()
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
        cur.execute("CREATE TABLE Pizzas (Id INTEGER PRIMARY KEY AUTOINCREMENT, CreatedOn DATE, CreatedBy TEXT, Type INTEGER, FOREIGN KEY (Type) REFERENCES PizzaTypes (Id));")

def add_pizza(pizza):
    pizza_id = None
    con = connect_db()
    now = datetime.datetime.now()
    with con:
        cur = con.cursor()
        t = (now, "TESTUSER", get_pizzatype_id(pizza['category'])) # TODO pizza type
        cur.execute("INSERT INTO Pizzas (CreatedOn, CreatedBy, Type) VALUES (?, ?, ?);", t)
        pizza_id = cur.lastrowid
        ingredients = list(itertools.chain.from_iterable(pizza['ingredients'].values()))
        for i in ingredients:
            print "{}".format(i)
            ingr_id = get_ingredient_id(i)
            t = [pizza_id, ingr_id]
            cur.execute("INSERT INTO PizzasIngredients (Pizza, Ingredient) VALUES (?, ?);", t)
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
            pizza = defaultdict(list)        
            pizza['id'] = p['Id']
            pizza['created_on'] = p['CreatedOn']
            pizza['created_by'] = p['CreatedBy']
            cur.execute("SELECT it.Name as category, it.DisplayName as category_name, i.DisplayName as ingredient FROM PizzasIngredients as pi JOIN Ingredients as i ON pi.Ingredient=i.Id JOIN IngredientTypes as it ON Type=it.Id WHERE pi.Pizza=?;", (pizza_id,))
            rows = cur.fetchall()
            ingredients = defaultdict(list)
            categories = defaultdict(list)
            base = ""
            for row in rows:
                categories[row['category']] = row['category_name']
                print "{}".format(row['category_name'])
                if row['category'] != 'pizza_base':
                    ingredients[row['category']].append(row['ingredient'])
                else:
                    base = row['ingredient']
            pizza['ingredients'] = ingredients
            pizza['base'] = base
            pizza['categories'] = categories
    return pizza    

def get_pizza_by_type(pizza_type):
    con = connect_db()
    con.row_factory = sqlite3.Row 

    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM Pizzas WHERE Type=?;", (get_pizzatype_id(pizza_type),))        
        p = cur.fetchall()
        if p is None:
            pizzas = None
        else:
            pizzas = []
            for pi in p:
                pizza = defaultdict(list)        
                pizza['id'] = pi['Id']
                pizza['created_on'] = pi['CreatedOn']
                pizza['created_by'] = pi['CreatedBy']
                cur.execute("SELECT it.DisplayName as category, i.DisplayName as ingredient FROM PizzasIngredients as pi JOIN Ingredients as i ON pi.Ingredient=i.Id JOIN IngredientTypes as it ON Type=it.Id WHERE pi.Pizza=?;", (pizza['id'],))
                rows = cur.fetchall()
                ingredients = defaultdict(list)
                for row in rows:
                    ingredients[row['category']].append(row['ingredient'])
                pizza['ingredients'] = ingredients
                pizzas.append(pizza)
    return pizzas    

def get_pizza_count():
    con = connect_db()
    with con:
        cur = con.cursor()
        cur.execute("SELECT COUNT(*) FROM Pizzas;");
        count = cur.fetchone()[0]
    return count

def create_pizzatypes_table():
    con = connect_db()
    with con:
        cur = con.cursor()
        cur.execute("DROP TABLE IF EXISTS PizzaTypes;")
        cur.execute("CREATE TABLE PizzaTypes (Id INTEGER PRIMARY KEY AUTOINCREMENT, Name TEXT, DisplayName TEXT);")

def init_pizzatypes_table():
    con = connect_db()
    with con:
        cur = con.cursor()
        for i in pizza_types:
            t = (i[0], i[1])
            cur.execute("INSERT INTO PizzaTypes (Name, DisplayName) VALUES (?, ?);", t)

def get_pizzatype_id(pizzatype):
    con = connect_db()
    with con:
        cur = con.cursor()
        cur.execute("SELECT Id FROM PizzaTypes WHERE Name=?", (pizzatype,))
        id = cur.fetchone()
        return id[0]

def join_and(items):
    if items:        
        if len(items) >= 2:
            joined = "{} and {}".format(", ".join(items[:-2]), items[-1])
        else:
            joined = " and ".join(items)
    else:
        joined = ""
    return joined

def get_description(pizza):

    ingredients = pizza['ingredients']
    pizza_base = pizza['base'] # assume only one pizza base
    extra_cheese = ingredients['extra_cheese']
    meat_fish_and_poultry = ingredients['meat_fish_and_poultry']
    veggies = ingredients['veggies']
    herbs = ingredients['herbs']
    sweets = ingredients['sweets']
    description = join_and(extra_cheese + meat_fish_and_poultry + veggies + herbs + sweets)

    if description:
        formatted = "{} with {}".format(pizza_base, description)
    else:
        formatted = None
    return formatted

def get_sharepad():
    """returns a dict which is useful for generating the sharepad form"""
    sharepad = {}
    con = connect_db()
    con.row_factory = sqlite3.Row    
    with con:
        cur = con.cursor()
        cur.execute("SELECT Name as name, DisplayName as display_name FROM IngredientTypes;")
        rows = cur.fetchall()
        sharepad['groups'] = rows        
        cur.execute("SELECT i.Name as name, i.DisplayName as display_name, it.Name as type_name, it.DisplayName as type_display_name FROM Ingredients as i JOIN IngredientTypes as it ON it.Id=i.Type;")
        rows = cur.fetchall()
        i = 1
        elements = []
        prev_type_name = None
        for r in rows:
            item = {}
            for k in ['name', 'display_name', 'type_name']:
                item[k] = r[k]
            # convert number to 0 padded string of length 3
            item['id'] = "{}_{:03d}".format(r['type_name'], i)
            elements.append(item)
            if prev_type_name == r['type_name'] or prev_type_name is None:
                i = i + 1
            else:
                i = 1
                prev_type_name = r['type_name']
        sharepad['elements'] = elements

        cur.execute("SELECT Name as name, DisplayName as display_name FROM PizzaTypes;")
        rows = cur.fetchall()
        categories = []
        for r in rows:
            item = {}
            item['name'] = r['name']
            item['display_name'] = r['display_name']
            print "{}  {}".format(item['name'], item['display_name'])
            categories.append(item)
        sharepad['categories'] = categories
    return sharepad

def get_admin():
    admin = {}
    con = connect_db()
    con.row_factory = sqlite3.Row 
    with con:
        cur = con.cursor()   
        cur.execute("SELECT Name as name, DisplayName as display_name FROM PizzaTypes;")
        rows = cur.fetchall()
    admin['pizza_types'] = rows   

    return admin

def connect_db():
    return sqlite3.connect(DATABASE)

def create_db():
    """Create the database tables"""
    create_ingredienttypes_table()
    create_ingredients_table()
    create_pizzatypes_table()
    create_pizzas_table()
    create_pizzasingredients_table()

def init_db():
    """Initialise the database"""
    init_ingredienttypes_table()
    init_ingredients_table()
    init_pizzatypes_table()

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
    pizza['ingredients'] = defaultdict(dict)
    for i in ingredient_types:
        pizza['ingredients'][i] = form.getlist(i)   
    pizza['category'] = form.getlist('category')[0]
    add_pizza(pizza)    
    return pizza

def main():
    create_db()
    init_db()

if __name__ == "__main__":
    main()
