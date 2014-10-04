from __future__ import with_statement
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from contextlib import closing
import sqlite3
import datetime
import itertools
from collections import defaultdict
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

    
# TODO: store this in a common location
# configuration
DATABASE = '/tmp/test.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'secret'

class Ingredient(db.Model):
    __tablename__ = "Ingredients"
    id = db.Column(db.Integer, primary_key=True)
    name  = db.Column(db.String(40))
    displayname  = db.Column(db.String(40))
    type = db.Column(db.Integer)
    def __init__(self, name, displayname, type):
        self.name  = name
        self.displayname = displayname
        self.type = type

    def __repr__(self):
        return '<Ingredient %r %r, %r, %r>' % (self.id, self.name, self.displayname, self.type)

class Pizza(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    createdOn = db.Column(db.Date())
    createdBy = db.Column(db.String(80)) # should be a user id
    style = db.Column(db.Integer())
    
    def __init__(self, createdOn, createdBy, style):
        self.createdOn = createdOn
        self.createdBy = createdBy
        self.style = style

    def __repr__(self):
        return '<Pizza %r, %r, %r>' % (self.createdOn, self.createdBy, self.style)

class IngredientType(db.Model):
    __tablename__ = "IngredientTypes"
    id = db.Column(db.Integer, primary_key=True)
    name  = db.Column(db.String(40))
    displayname  = db.Column(db.String(40))
    def __init__(self, name, displayname):
        self.name  = name
        self.displayname = displayname

    def __repr__(self):
        return '<IngredientType %r, %r, %r>' % (self.id, self.name, self.displayname)

class PizzaIngredient(db.Model):
    pizza = db.Column(db.Integer, db.ForeignKey(Pizza.id), primary_key=True)
    ingredient  = db.Column(db.Integer, db.ForeignKey(Ingredient.id))
    displayname  = db.Column(db.String(40))
    def __init__(self, pizza, ingredient, displayname):
        self.pizza = pizza
        self.ingredient = ingredient
        self.displayname = displayname
    def __repr__(self):
        return '<PizzaIngredient %r, %r, %r>' % (self.pizza, self.ingredient, self.displayname)

class Style(db.Model):
    __tablename__ = "Styles"
    id = db.Column(db.Integer, primary_key=True)
    name  = db.Column(db.String(40))
    displayname  = db.Column(db.String(40))
    def __init__(self, name, displayname):
        self.name  = name
        self.displayname = displayname

    def __repr__(self):
        return '<Style %r, %r, %r>' % (self.id, self.name, self.displayname)
    
class StyleIngredient(db.Model):
    __tablename__ = "StylesIngredients"
    id = db.Column(db.Integer, primary_key=True)
    style = db.Column(db.Integer, db.ForeignKey(Style.id))
    ingredient = db.Column(db.Integer, db.ForeignKey(Ingredient.id))
    def __init__(self, style, ingredient):
        self.style = style
        self.ingredient = ingredient

    def __repr__(self):
        return '<StyleIngredient %r, %r>' % (self.style, self.ingredient)

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
   ["cheese_focaccia", "Cheese Focaccia", "pizza_base"],
   ["herb_focaccia", "Herb Focaccia", "pizza_base"],
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
    ["sesame_seeds", "Sesame Seeds", "veggies", ["veggie", "african", "fresh", "fishy", "sweet"]],
    ["spinach", "Spinach", "veggies", ["veggie", "fresh", "healthy", "african", "english"]],
    ["sundried_tomatoes", "Sundried Tomatoes", "veggies", ["mediterranean", "italian", "fresh", "veggie", "cheezy", "meaty"]],

# Herbs
    ["basil", "Basil", "herbs", ["italian", "fresh"]],
    ["chillies", "Chillies", "herbs", ["spicy", "african", "cheezy", "american", "portuguese", "meaty", "veggie", "tropical", "fresh"]],
    ["chives", "Chives", "herbs", ["french", "meaty", "cheezy", "english"]],
    ["coriander", "Coriander", "herbs", ["fresh", "healthy", "meaty", "african", "american", "veggie", "spicy"]],
    ["garlic", "Garlic", "herbs",  ["italian", "french", "american", "fishy", "portuguese", "spicy"]],
    ["roasted_garlic", "Roasted Garlic", "herbs" , ["cheezy", "italian",  "french", "meaty", "mediterranean", "veggie"]],
    ["rocket", "Rocket", "herbs", ["fresh", "american", "healthy", "meaty", "veggie", "spicy"]],
    ["rosemary", "Rosemary", "herbs", ["sweet", "english", "meaty"]],
    ["spring_onions", "Spring Onions", "herbs", ["french", "cheezy", "fishy"]],

# Sweets
    ["flake", "Flake", "sweets", ["sweet"]],
     ["jelly_tots", "Jelly Tots", "sweets",  ["sweet"]],
    ["marshmallows", "Marshmallows", "sweets", ["sweet"]],
    ["oreo_biscuits", "Oreo Biscuits", "sweets", ["sweet"]],
    ["peppermint_aero", "Peppermint Aero", "sweets", ["sweet"]],
    ["smarties", "Smarties", "sweets", ["sweet"]],
    ["whispers", "Whispers", "sweets", ["sweet"]],
    ["100s_and_1000s", "100's & 1000's", "sweets", ["sweet"]]
]

styles = [
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
    ["tropical", "Tropical"],
    ["healthy", "Healthy"],
    ["wacky", "Wacky"],
    ["fishy", "Fishy"],
    ["sweet", "Sweet"]
]

styles_ingredients = {"italian": ["margherita", "mini_margherita", "garlic_focaccia", "cheese_focaccia", "herb_focaccia", "rosso", "gorgonzola", "mozzarella", "mini_mozzarella", "parmigiano", "anchovies", "egg_x2", "lamb", "mince", "parma_ham", "salami", "tuna", "almonds_roasted", "artichokes", "baby_marrow", "capers", "cherry_tomatoes", "mushrooms", "olives", "sundried_tomatoes", "basil", "chillies", "chives", "coriander", "garlic", "roasted_garlic", "rocket", "rosemary", "spring_onions"],
"greek": ["margherita", "mini_margherita", "garlic_focaccia", "herb_focaccia", "pizza_wrap", "feta", "haloumi", "mozzarella", "mini_mozzarella", "anchovies", "lamb", "mince", "tuna", "almonds_roasted", "artichokes", "baby_marrow", "brinjals",  "caramelised_onions", "cherry_tomatoes", "olives", "onions", "sesame_seeds", "spinach", "chillies", "chives", "coriander", "garlic", "rosemary", "spring_onions"],
"portuguese": ["margherita", "mini_margherita", "garlic_focaccia", "cheese_focaccia", "herb_focaccia", "mozzarella", "mini_mozzarella", "anchovies", "chourico", "egg_x2", "lamb", "parma_ham", "salami", "spicy_chicken", "capers", "cherry_tomatoes", "green_peppers", "mushrooms", "olives", "onions", "spinach", "sundried_tomatoes", "chillies", "chives", "coriander", "garlic", "roasted_garlic", "rocket", "rosemary", "spring_onions"],
"american": ["margherita", "mini_margherita", "garlic_focaccia", "cheese_focaccia", "herb_focaccia", "rosso", "nutella", "cheddar", "mozzarella", "mini_mozzarella",  "anchovies", "bacon", "ham", "salami", "spare_ribs", "avocado", "caramelised_onions", "green_peppers", "jalapenos", "mushrooms", "olives", "onions", "basil", "chillies", "chives", "coriander", "garlic", "roasted_garlic", "rocket", "spring_onions", "marshmallows", "oreo_biscuits"],
"french":["margherita", "mini_margherita", "gluten_free", "garlic_focaccia", "cheese_focaccia", "herb_focaccia", "rosso",  "gorgonzola", "mozzarella", "mini_mozzarella", "parmigiano", "anchovies", "parma_ham", "salami",  "tuna", "almonds_roasted", "artichokes", "avocado", "baby_marrow", "brinjals", "capers", "cherry_tomatoes", "green_peppers", "mushrooms", "onions", "spinach", "chives", "garlic", "roasted_garlic", "spring_onions"],
"english":["margherita", "mini_margherita", "garlic_focaccia", "cheese_focaccia", "herb_focaccia", "cheddar", "feta", "haloumi", "ham", "bacon", "chourico", "almonds_roasted", "artichokes", "avocado", "baby_marrow", "brinjals", "capers", "caramelised_onions", "cherry_tomatoes", "green_peppers", "mushrooms", "olives", "spinach", "sundried_tomatoes", "basil", "chives", "coriander", "rocket", "rosemary"],
"meaty" :["margherita", "mini_margherita", "gluten_free", "wholewheat", "mozzarella", "mini_mozzarella", "parmigiano", "bacon", "biltong", "chourico", "ham", "lamb", "mince", "parma_ham", "salami", "spare_ribs", "spicy_chicken", "almonds_roasted", "capers", "caramelised_onions", "cherry_tomatoes", "green_peppers", "jalapenos", "mushrooms", "olives", "onions", "peppadews", "pineapple", "sesame_seeds", "spinach", "chives", "coriander", "garlic", "roasted_garlic", "rocket", "rosemary", "spring_onions"],
"spicy":["margherita", "mini_margherita", "chakalaka", "garlic_focaccia", "herb_focaccia", "pizza_wrap", "nutella", "haloumi", "mozzarella", "mini_mozzarella", "chourico", "egg_x2", "mince", "salami", "spare_ribs", "spicy_chicken", "avocado", "banana", "brinjals", "green_peppers", "jalapenos", "mushrooms", "olives", "onions", "peppadews", "pineapple", "chillies", "chives", "coriander", "garlic", "roasted_garlic", "rocket", "rosemary", "spring_onions"],
"fresh":["margherita", "mini_margherita", "gluten_free", "wholewheat", "chakalaka", "garlic_focaccia", "cheese_focaccia", "herb_focaccia", "pizza_wrap", "rosso", "feta", "haloumi", "mozzarella", "mini_mozzarella", "egg_x2", "ham", "parma_ham", "spare_ribs", "spicy_chicken", "artichokes", "avocado", "baby_marrow", "banana", "brinjals", "capers", "cherry_tomatoes", "green_peppers", "jalapenos", "mushrooms", "olives", "onions", "peppadews", "pineapple", "sesame_seeds", "spinach", "basil", "chillies", "chives", "coriander", "garlic", "rocket", "rosemary", "spring_onions"],
"veggie":["margherita", "mini_margherita", "gluten_free", "wholewheat", "chakalaka", "garlic_focaccia", "cheese_focaccia", "herb_focaccia", "pizza_wrap", "rosso", "feta", "haloumi", "mozzarella", "mini_mozzarella", "parmigiano", "anchovies", "bacon", "biltong", "chourico", "almonds_roasted", "artichokes", "avocado", "baby_marrow", "banana", "brinjals", "capers", "caramelised_onions", "cherry_tomatoes", "green_peppers", "jalapenos", "mushrooms", "olives", "onions", "peppadews", "pineapple", "sesame_seeds", "spinach", "sundried_tomatoes", "basil", "chillies", "chives", "coriander", "garlic", "roasted_garlic", "rocket", "rosemary", "spring_onions"],
"mediterranean":["margherita", "mini_margherita", "gluten_free", "wholewheat", "garlic_focaccia", "herb_focaccia", "pizza_wrap", "rosso", "feta", "gorgonzola", "haloumi", "mozzarella", "mini_mozzarella", "parmigiano", "anchovies", "lamb", "mince", "parma_ham", "salami", "tuna", "almonds_roasted", "artichokes", "baby_marrow", "brinjals", "capers", "green_peppers", "olives", "sesame_seeds", "sundried_tomatoes", "basil", "garlic", "roasted_garlic", "rosemary"],
"african": ["margherita", "mini_margherita", "chakalaka", "cheddar", "feta", "haloumi", "mozzarella", "mini_mozzarella", "biltong", "lamb", "mince", "spare_ribs", "spicy_chicken",  "avocado", "banana", "onions", "peppadews", "sesame_seeds", "spinach", "sundried_tomatoes", "basil", "chillies", "chives", "coriander", "garlic", "roasted_garlic", "rocket"],
"cheesy": ["margherita", "mini_margherita", "chakalaka", "garlic_focaccia", "cheese_focaccia", "herb_focaccia", "cheddar", "feta", "gorgonzola", "haloumi", "mozzarella", "mini_mozzarella", "parmigiano", "bacon", "biltong", "chourico", "ham", "lamb", "mince", "parma_ham", "salami", "capers", "caramelised_onions", "cherry_tomatoes", "green_peppers", "jalapenos", "peppadews", "spinach", "sundried_tomatoes", "basil", "chives", "garlic", "roasted_garlic", "rocket", "spring_onions"],
"tropical":["margherita", "mini_margherita", "gluten_free", "wholewheat", "chakalaka", "garlic_focaccia", "cheese_focaccia", "herb_focaccia", "pizza_wrap", "mozzarella", "mini_mozzarella", "bacon", "chourico", "ham", "lamb", "spicy_chicken", "avocado", "banana", "cherry_tomatoes", "green_peppers", "jalapenos", "onions", "peppadews", "pineapple", "spinach", "chillies", "chives", "coriander"],
"healthy":["mini_margherita", "gluten_free", "wholewheat", "chakalaka", "garlic_focaccia", "herb_focaccia", "pizza_wrap", "rosso", "feta", "gorgonzola", "haloumi", "mini_mozzarella", "egg_x2", "ham", "lamb", "parma_ham", "spare_ribs", "spicy_chicken", "tuna", "almonds_roasted", "artichokes", "avocado", "baby_marrow", "banana", "brinjals", "capers", "caramelised_onions", "cherry_tomatoes", "green_peppers", "jalapenos", "mushrooms", "olives", "onions", "peppadews", "pineapple", "sesame_seeds", "spinach", "sundried_tomatoes", "basil", "chillies", "chives", "coriander", "garlic", "roasted_garlic", "rocket", "rosemary", "spring_onions"],
"fishy":["margherita", "mini_margherita", "gluten_free", "wholewheat", "chakalaka", "garlic_focaccia", "cheese_focaccia", "herb_focaccia", "pizza_wrap", "rosso", "feta", "gorgonzola", "haloumi", "mozzarella", "mini_mozzarella", "parmigiano", "anchovies", "tuna", "almonds_roasted", "artichokes", "avocado", "baby_marrow", "brinjals", "capers", "caramelised_onions", "cherry_tomatoes", "green_peppers", "olives", "onions", "peppadews", "pineapple", "sesame_seeds", "spinach", "sundried_tomatoes", "basil", "chives", "coriander", "garlic", "rocket", "spring_onions"],
"sweet":["margherita", "mini_margherita", "gluten_free", "wholewheat", "chakalaka", "garlic_focaccia", "cheese_focaccia", "herb_focaccia", "pizza_wrap", "rosso", "nutella", "cheddar", "feta", "gorgonzola", "haloumi", "mozzarella", "mini_mozzarella", "parmigiano", "anchovies", "bacon", "biltong", "chourico", "egg_x2", "ham", "lamb", "mince", "parma_ham", "salami", "spare_ribs", "spicy_chicken", "tuna", "almonds_roasted", "artichokes", "avocado", "baby_marrow", "banana", "brinjals", "capers", "caramelised_onions", "cherry_tomatoes", "green_peppers", "jalapenos", "mushrooms", "olives", "onions", "peppadews", "pineapple", "sesame_seeds", "spinach", "sundried_tomatoes", "basil", "chillies", "chives", "coriander", "garlic", "roasted_garlic", "rocket", "rosemary", "spring_onions", "flake", "jelly_tots", "marshmallows", "oreo_biscuits", "peppermint_aero", "smarties", "whispers", "100s_and_1000s"]}

 #   any_one("base").and_also(any_number("veggies").except_for(["", ""]))

def init_ingredienttypes_table():
    for i in ingr_types:
        t = IngredientType(i[0], i[1])
        db.session.add(t)
    db.session.commit()

def get_ingredienttype_id(ingredienttype):
    return IngredientType.query.filter_by(name=ingredienttype).first().id

def init_ingredients_table():
    for i in ingredients:
        ingredient = Ingredient(i[0], i[1], get_ingredienttype_id(i[2]))
        db.session.add(ingredient)
    db.session.commit()

def get_ingredient_id(ingredient):
    id = Ingredient.query.filter_by(name=ingredient).first().id
    if id==None:
        print "Ingredient %s not found in db" %(ingredient)
    return id
       
def init_styles_table():
    for i in styles:
        style  = Style(i[0], i[1])
        db.session.add(style)
    db.session.commit()

def init_styles_ingredients_table():
    for i in styles_ingredients:
        for j in styles_ingredients[i]:
            t = StyleIngredient(get_style_id(i), get_ingredient_id(j))
            db.session.add(t)
    db.session.commit()

def add_pizza(pizza):
    pizza_id = None
    now = datetime.datetime.now()
    pizza = Pizza(now, "TESTUSER", get_style_id(pizza['style']))
    pizza_id = db.session.add(pizza)
    print pizza_id
# TODO get lastrowid??
        # ingredients = list(itertools.chain.from_iterable(pizza['ingredients'].values()))
        # for i in ingredients:
        #     ingr_id = get_ingredient_id(i)
        #     t = [pizza_id, ingr_id]
        #     cur.execute("INSERT INTO PizzasIngredients (Pizza, Ingredient) VALUES (?, ?);", t)
        # print pizza
        # base = pizza['pizza_base']
        # ingr_id = get_ingredient_id(base)
        # t = [pizza_id, ingr_id]
        # cur.execute("INSERT INTO PizzasIngredients (Pizza, Ingredient) VALUES (?, ?);", t)
    return pizza_id    

def get_pizza_by_id(pizza_id):
    p = Pizza.query.filter_by(id=pizza_id).first()
    if p is None:
        pizza = None
    else:
        pizza = defaultdict(dict)        
        pizza['id'] = p.id
        pizza['created_on'] = p.createdOn
        pizza['created_by'] = p.createdBy
        style = p.style
        print PizzaIngredient.query.join(ingredient).all()
    return None
        #cur.execute("SELECT it.Name as category, it.DisplayName as category_name, i.Name as ingredient FROM PizzasIngredients as pi JOIN Ingredients as i ON pi.Ingredient=i.Id JOIN IngredientTypes as it ON Type=it.Id WHERE pi.Pizza=?;", (pizza_id,))
        # rows = cur.fetchall()
        #     ingredients = defaultdict(list)
        #     base = ""
        #     for row in rows:
        #         if row['category'] != 'pizza_base':
        #             ingredients[row['category']].append(row['ingredient'])
        #         else:
        #             base = row['ingredient']
        #     pizza['ingredients'] = ingredients
        #     pizza['pizza_base'] = base
        # cur.execute("SELECT pt.Name as type, pt.Id as id FROM Styles as pt WHERE pt.Id=?;", (style,)) 
        # try:
        #     pizza['style'] = cur.fetchone()[0]
        # except:
        #     pizza['style'] = "UNKNOWN"
#    return pizza    


def get_pizza_by_style(style):
    # con = connect_db()
    # con.row_factory = sqlite3.Row 

    # with con:
    #     cur = con.cursor()
    #     cur.execute("SELECT * FROM Pizzas WHERE Style=?;", (get_style_id(style),))        
    #     p = cur.fetchall()
    #     if p is None:
    #         pizzas = None
    #     else:
    #         pizzas = []
    #         for pi in p:
    #             pizza = defaultdict(dict)        
    #             pizza['id'] = pi['Id']
    #             pizza['created_on'] = pi['CreatedOn']
    #             pizza['created_by'] = pi['CreatedBy']
    #             cur.execute("SELECT it.DisplayName as category, i.DisplayName as ingredient FROM PizzasIngredients as pi JOIN Ingredients as i ON pi.Ingredient=i.Id JOIN IngredientTypes as it ON Type=it.Id WHERE pi.Pizza=?;", (pizza['id'],))
    #             rows = cur.fetchall()
    #             ingredients = defaultdict(list)
    #             for row in rows:
    #                 if row['category'] == 'pizza_base':
    #                     pizza['pizza_base'] = row['ingredients']
    #                 else:
    #                     ingredients[row['category']].append(row['ingredient'])
    #             pizza['ingredients'] = ingredients
    #             pizza['style'] = style
    # return pizzas    
    return None

def get_pizza_ids():
    flatids = Pizza.query.all().id
    # con = connect_db()
    # with con:
    #     cur = con.cursor()
    #     cur.execute("SELECT Id as id FROM Pizzas;")
    #     ids = cur.fetchall()
    # flatids = [i[0] for i in ids]
    return flatids

def get_pizza_count():
    count=Pizza.query.all().count()
    return count

# def init_pizzastyles_table():
#     con = connect_db()
#     with con:
#         cur = con.cursor()
#         for i in styles:
#             t = (i[0], i[1])
#             cur.execute("INSERT INTO Styles (Name, DisplayName) VALUES (?, ?);", t)

def get_style_id(style):
    return Style.query.filter_by(name=style).first().id

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
    formatted = ""
    if pizza:
        style = pizza['style']
        ingredients = pizza['ingredients']
        base = pizza['pizza_base'] # assume only one pizza base
        extra_cheese = ingredients['extra_cheese']
        meat_fish_and_poultry = ingredients['meat_fish_and_poultry']
        veggies = ingredients['veggies']
        herbs = ingredients['herbs']
        sweets = ingredients['sweets']
        ingr_displaynames = get_ingr_displaynames()
        ingrs = extra_cheese + meat_fish_and_poultry + veggies + herbs + sweets
        ingr_display_names = []
        display_names = get_ingr_displaynames()
        for i in ingrs:
            ingr_display_names.append(display_names[i])
            
        description = join_and(ingr_display_names)
        if description:
            formatted = "{} base with {} ({})".format(display_names[base], description, style)

    return formatted

def get_rand_length(l):
    if len(l) > 2:
        return random.randint(1, len(l) - 1)
    else:
        return 1

def generate_pizza_by_style(style):
    return None
    # con = connect_db()
    # con.row_factory = sqlite3.Row
    # random.seed()
    # with con:
    #     cur = con.cursor()
    #     cur.execute("SELECT i.Id, i.Name as name, i.DisplayName as name, it.Id, it.Name as type, it.DisplayName FROM StylesIngredients as si JOIN Ingredients as i ON si.Ingredient=i.Id JOIN IngredientTypes as it ON i.Type=it.Id WHERE (Style=? AND it.Name=?);", (get_style_id(style), 'pizza_base',))
    #     p = cur.fetchall()
    #     pb = [i['name'] for i in p]
    #     pizza_base = random.choice(pb)

    #     cur.execute("SELECT i.Id, i.Name as name, i.DisplayName as name, it.Id, it.Name as type, it.DisplayName FROM StylesIngredients as si JOIN Ingredients as i ON si.Ingredient=i.Id JOIN IngredientTypes as it ON i.Type=it.Id WHERE (Style=? AND it.Name=?);", (get_style_id(style), 'extra_cheese',))
    #     p = cur.fetchall()
    #     ec = [i['name'] for i in p if  i['type']=='extra_cheese']
    #     extra_cheese = random.sample(ec, get_rand_length(ec))
                
    #     cur.execute("SELECT i.Id, i.Name as name, i.DisplayName as name, it.Id, it.Name as type, it.DisplayName FROM StylesIngredients as si JOIN Ingredients as i ON si.Ingredient=i.Id JOIN IngredientTypes as it ON i.Type=it.Id WHERE (Style=? AND it.Name=?);", (get_style_id(style), 'meat_fish_and_poultry',))
    #     p = cur.fetchall()
    #     mfp = [i['name'] for i in p if  i['type']=='meat_fish_and_poultry']
    #     meat_fish_and_poultry = random.sample(mfp, get_rand_length(mfp))
        
    #     cur.execute("SELECT i.Id, i.Name as name, i.DisplayName as name, it.Id, it.Name as type, it.DisplayName FROM StylesIngredients as si JOIN Ingredients as i ON si.Ingredient=i.Id JOIN IngredientTypes as it ON i.Type=it.Id WHERE (Style=? AND it.Name=?);", (get_style_id(style), 'veggies',))
    #     p = cur.fetchall()
    #     v = [i['name'] for i in p if  i['type']=='veggies']
    #     veggies = random.sample(v, get_rand_length(v))
    
    #     cur.execute("SELECT i.Id, i.Name as name, i.DisplayName as name, it.Id, it.Name as type, it.DisplayName FROM StylesIngredients as si JOIN Ingredients as i ON si.Ingredient=i.Id JOIN IngredientTypes as it ON i.Type=it.Id WHERE (Style=? AND it.Name=?);", (get_style_id(style), 'herbs',))
    #     p = cur.fetchall()

    #     h = [i['name'] for i in p if  i['type']=='herbs']
    #     herbs = random.sample(h, get_rand_length(h))

    #     # cur.execute("SELECT i.Id, i.Name, i.DisplayName, it.Id, it.Name, it.DisplayName FROM StylesIngredients as si JOIN Ingredients as i ON si.Ingredient=i.Id JOIN IngredientTypes as it ON i.Type=it.Id WHERE (Style=? AND it.Name=?);", (get_style_id(style), 'sweets',))
    #     # p = cur.fetchall()

    #     # sw = [i[1] for i in p if  i[4]=='sweets']
    #     # try:
    #     #     sweets = random.sample(sw, get_rand_length(sw))
    #     # except:
    #     sweets = []
        
    #     pizza = defaultdict(dict)        
    #     pizza['pizza_base'] = pizza_base
    #     pizza['ingredients'] = defaultdict(list)
    #     pizza['ingredients']['veggies'] = veggies
    #     pizza['ingredients']['meat_fish_and_poultry'] = meat_fish_and_poultry
    #     pizza['ingredients']['extra_cheese'] = extra_cheese
    #     pizza['ingredients']['herbs'] = herbs
    #     pizza['ingredients']['sweets'] = sweets
    #     pizza['style'] = style
    #     pizza['created_on'] = datetime.datetime.now()
    #     pizza['created_by'] = "GENERATED"

    # return pizza

def get_sharepad():
    """returns a dict which is useful for generating the sharepad form"""
    return None
    # sharepad = {}
    # con = connect_db()
    # con.row_factory = sqlite3.Row    
    # with con:
    #     cur = con.cursor()
    #     cur.execute("SELECT Name as name, DisplayName as display_name FROM IngredientTypes;")
    #     rows = cur.fetchall()
    #     sharepad['groups'] = rows        
    #     cur.execute("SELECT DISTINCT i.Name as name, i.DisplayName as display_name, it.Name as type_name, it.DisplayName as type_display_name FROM Ingredients as i JOIN IngredientTypes as it ON it.Id=i.Type;")
    #     rows = cur.fetchall()
    #     i = 1
    #     elements = []
    #     prev_type_name = None
    #     for r in rows:
    #         item = {}
    #         for k in ['name', 'display_name', 'type_name']:
    #             item[k] = r[k]
    #         # convert number to 0 padded string of length 3
    #         item['id'] = "{}_{:03d}".format(r['type_name'], i)
    #         elements.append(item)
    #         if prev_type_name == r['type_name'] or prev_type_name is None:
    #             i = i + 1
    #         else:
    #             i = 1
    #             prev_type_name = r['type_name']
    #     sharepad['elements'] = elements

    #     cur.execute("SELECT Name as name, DisplayName as display_name FROM Styles;")
    #     rows = cur.fetchall()
    #     styles = []
    #     for r in rows:
    #         item = {}
    #         item['name'] = r['name']
    #         item['display_name'] = r['display_name']
    #         # print "{}  {}".format(item['name'], item['display_name'])
    #         styles.append(item)
    #     sharepad['styles'] = styles
    # return sharepad

# def get_admin():
#     admin = {}
#     con = connect_db()
#     con.row_factory = sqlite3.Row 
#     with con:
#         cur = con.cursor()   
#         cur.execute("SELECT Name as name, DisplayName as display_name FROM Styles;")
#         rows = cur.fetchall()
#     admin['styles'] = rows   

#     return admin

def connect_db():
    return sqlite3.connect(DATABASE)

def create_tables():
    """Create the database tables"""
    db.create_all()

def init_database():
    """Initialise the database"""
    init_ingredienttypes_table()
    init_ingredients_table()
    init_styles_table()
    init_styles_ingredients_table()

def show_ingredients():
    rows = Ingredient.query.all()
    for row in rows:
        print row

def is_valid_style(style):
    return style in [i[0] for i in styles]

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
    rows = Ingredient.query.all()
    ingr_displaynames = {}
    for r in rows:
        ingr_displaynames[r.name] = r.displayname
    return ingr_displaynames

def is_valid_base(base):
    return base in get_bases()

def is_valid_style(style):
    return style in [i[0] for i in get_styles()]

def is_valid_pizza(pizza):
    assert(pizza.has_key('created_on') and pizza['created_on'] is not None)
    assert(pizza.has_key('created_by') and pizza['created_by'] is not None)

    assert(pizza.has_key('ingredients'))
    assert(pizza.has_key('pizza_base'))
    assert(is_valid_base(pizza['pizza_base']))
    assert(pizza['ingredients'].has_key('extra_cheese'))
    assert(pizza['ingredients'].has_key('meat_fish_and_poultry'))
    assert(pizza['ingredients'].has_key('veggies'))
    assert(pizza['ingredients'].has_key('herbs'))       
    assert(pizza.has_key('style'))
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
                print "ingredient {} is not in style {}".format(ingredient, style)
            assert(get_ingredient_id(ingredient)!=None)
            
    return True

def main():
    create_tables()
    init_database()

if __name__ == "__main__":
    main()



