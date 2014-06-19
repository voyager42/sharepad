from __future__ import with_statement
from contextlib import closing
import sqlite3

import sharepad_db as db

def test_get_sharepad():
    sharepad = db.get_sharepad()
    assert(sharepad.has_key('elements'))
    assert(sharepad.has_key('groups'))
    names=[]
    # check duplicates
    for i in sharepad['elements']:
        assert(i['name'] not in names)
        names.append(i['name'])

def test_styles_ingredients():
    con = db.connect_db()
    con.row_factory = sqlite3.Row 
    with con:
        cur = con.cursor()
        cur.execute("SELECT Id as id, Name as name from Styles;")
        styles = cur.fetchall()
        for s in styles:
            cur.execute("SELECT DISTINCT si.Ingredient as ingredient, i.Name as name FROM StylesIngredients as si JOIN Ingredients as i ON si.Ingredient=i.Id WHERE si.Style=?;", (s[0],))        
            r = cur.fetchall()
            style = s[1]
            for row in r:
                ingredient = row[1]
                try:
                    assert(ingredient in ingredients[styles_ingredients[style]][1])
                except:
                    print "ingredient {} is not in style {}".format(ingredient, style)

def test_generate_pizza_by_style():
    some_styles = [i[0] for i in db.get_styles() if i[0] not in ['wacky', 'sweet']]
    for style in some_styles:
        pizza = db.generate_pizza_by_style(style)
        assert(db.is_valid_pizza(pizza))
    
def pizzas_are_equal(pizza1, pizza2):
    retval = True
    for k in pizza1.keys():
        if (k == 'ingredients'):
            for j in pizza1[k]:
                retval = pizza2[k].has_key(j) and pizza2[k][j]==pizza1[k][j]
                
        elif (k != 'id') and (k!='created_on') and (k!='created_by'):
            if not pizza2.has_key(k):
                print "Key %s does not exist in pizza2" % (k)
                retval = False
            if (pizza2.has_key(k) and pizza2[k]!=pizza1[k]):
                print "does not match in ", k                    
                retval = False
            elif (pizza2.has_key(k) and pizza2[k]==pizza1[k]):
                print "has key %s and matches" % (k)
    return retval
                    

        
def test_add_pizza():
    some_styles = [i[0] for i in db.get_styles() if i[0] not in ['wacky', 'sweet']]
    for style in some_styles:
        pizza = db.generate_pizza_by_style(style)
        print pizza
        id = db.add_pizza(pizza)
        pizza2 = db.get_pizza_by_id(id)
        print pizza2
        assert(pizzas_are_equal(pizza,pizza2))













