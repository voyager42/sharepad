import sqlite3

from sharepad import sharepad_db
from sharepad.sharepad_db import ingredients, styles_ingredients


def test_get_sharepad():
    sharepad = sharepad_db.get_sharepad()
    assert('elements' in sharepad)
    assert('groups' in sharepad)
    names = []
    # check duplicates
    for i in sharepad['elements']:
        assert(i['name'] not in names)
        names.append(i['name'])


def test_styles_ingredients():
    con = sharepad_db.connect_db()
    con.row_factory = sqlite3.Row
    with con:
        cur = con.cursor()
        cur.execute("SELECT Id as id, Name as name from Styles;")
        styles = cur.fetchall()
        for s in styles:
            cur.execute(
                ("SELECT DISTINCT si.Ingredient as ingredient, i.Name as name "
                 "FROM StylesIngredients as si JOIN Ingredients as i ON "
                 "si.Ingredient=i.Id WHERE si.Style=?;"), (s[0],))
            r = cur.fetchall()
            style = s[1]
            for row in r:
                ingredient = row[1]
                try:
                    pizza_ingredients = (
                        ingredients[styles_ingredients[style]][1])
                    assert(ingredient in pizza_ingredients)
                except:
                    print "ingredient {0} is not in style {1}".format(
                        ingredient, style)


def test_generate_pizza_by_style():
    some_styles = [i[0] for i in sharepad_db.get_styles()
                   if i[0] not in ['wacky', 'sweet']]
    for style in some_styles:
        pizza = sharepad_db.generate_pizza_by_style(style)
        assert(sharepad_db.is_valid_pizza(pizza))


def pizzas_are_equal(pizza1, pizza2):
    retval = True
    for k in pizza1.keys():
        if (k == 'ingredients'):
            for j in pizza1[k]:
                retval = (j in pizza2[k]) and pizza2[k][j] == pizza1[k][j]

        elif (k != 'id') and (k != 'created_on') and (k != 'created_by'):
            if k not in pizza2:
                print "Key %s does not exist in pizza2" % (k)
                retval = False
            if (k in pizza2) and pizza2[k] != pizza1[k]:
                print "does not match in ", k
                retval = False
            elif (k in pizza2) and pizza2[k] == pizza1[k]:
                print "has key %s and matches" % (k)
    return retval


def test_add_pizza():
    some_styles = [i[0] for i in sharepad_db.get_styles()
                   if i[0] not in ['wacky', 'sweet']]
    for style in some_styles:
        pizza = sharepad_db.generate_pizza_by_style(style)
        print pizza
        id = sharepad_db.add_pizza(pizza)
        pizza2 = sharepad_db.get_pizza_by_id(id)
        print pizza2
        assert(pizzas_are_equal(pizza, pizza2))


def test_ingr_displaynames():
    ingr_displaynames = sharepad_db.get_ingr_displaynames()
    con = sharepad_db.connect_db()
    con.row_factory = sqlite3.Row
    with con:
        cur = con.cursor()
        cur.execute(
            ("SELECT Id as id, Name as name, DisplayName as display_name "
             "FROM Ingredients;"))
        rows = cur.fetchall()
        for r in rows:
            assert(r['display_name'] == ingr_displaynames[r['name']])
