from sqlalchemy import Column, String, Integer, ForeignKey, Date
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

from sharepad.ingredients import (
    ingr_types, ingredients, styles, styles_ingredients)

Base = declarative_base()

from sqlalchemy import create_engine
engine = create_engine('sqlite:///sharepad.db')

from sqlalchemy.orm import sessionmaker
session = sessionmaker()
session.configure(bind=engine)
Base.metadata.create_all(engine)

class IngredientTypes(Base):
    __tablename__= "IngredientTypes"
    Id = Column(Integer, primary_key=True)
    Name = Column(String)
    DisplayName = Column(String)

    def __repr__(self):
        return "<IngredientType(Id='%s', Name='%s', DisplayName='%s')>" % (self.Id, self.Name, self.DisplayName)

class Ingredients(Base):
    __tablename__= "Ingredients"
    Id = Column(Integer, primary_key=True)
    Name = Column(String)
    DisplayName = Column(String)
    Type = Column(Integer, ForeignKey('IngredientTypes.Id'))

    def __repr__(self):
        return "<Ingredient(Id='%s', Name='%s', DisplayName='%s', Type='%s')>" % (self.Id, self.Name, self.DisplayName, self.Type)

class PizzasIngredients(Base):
    __tablename__ = "PizzasIngredients"
# SQLAlchemy needs a primary key so use a composite primary key as per 
# http://stackoverflow.com/questions/9291307/python-sqlalchemy-table-with-no-primary-keys-and-duplicate-values
    Pizza =  Column(Integer, ForeignKey('Pizzas.Id'), primary_key=True)
    Ingredient = Column(Integer, ForeignKey('Ingredients.Id'), primary_key=True)

    def __repr__(self):
        return "<PizzaIngredient(Pizza='%s', Ingredient='%s')>" % (self.Pizza, self.Ingredient)


class Pizzas(Base):
    __tablename__ = "Pizzas"
    Id = Column(Integer, primary_key=True)
    CreatedOn = Column(Date)
    CreatedBy = Column(String)
    Style = Column(Integer, ForeignKey('Styles.Id'))

    def __repr__(self):
        return "<Pizza(Id='%s', CreatedOn='%s', CreatedBy='%s', Style='%s')>" % (self.Id, self.CreatedOn, self.CreatedBy, self.Style)


class Styles(Base):
    __tablename__ = "Styles"
    Id = Column(Integer, primary_key=True)
    Name = Column(String)
    DisplayName=Column(String)

    def __repr__(self):
        return "<Style(Id='%s', Name='%s', DisplayName='%s')>" % (self.Id, self.Name, self.DisplayName)

class StylesIngredients(Base):
    __tablename__ = "StylesIngredients"
# SQLAlchemy needs a primary key so use a composite primary key as per 
# http://stackoverflow.com/questions/9291307/python-sqlalchemy-table-with-no-primary-keys-and-duplicate-values
    Style = Column(Integer, ForeignKey('Styles.Id'), primary_key=True)
    Ingredient = Column(Integer, ForeignKey('Ingredients.Id'), primary_key=True)

    def __repr__(self):
        return "<StyleIngredient(Style='%s', Ingredient='%s')>" % (self.Style, self.Ingredient)


from sqlalchemy import select
s = session()
count=0
for i in s.query(IngredientTypes).all():
#    print i
    count = count + 1
print "IngredientTypes", count

count=0
for i in s.query(Ingredients).all():
#    print i
    count = count + 1
print "Ingredients", count


count=0
for i in s.query(PizzasIngredients).all():
#    print i
    count = count + 1
print "PizzasIngredients", count

count=0
for i in s.query(Pizzas).all():
#    print i
    count = count + 1
print "Pizzas", count

count=0
for i in s.query(Styles).all():
#    print i
    count = count + 1
print "Styles", count

count=0
for i in s.query(StylesIngredients).all():
#    print i
    count = count + 1
print "StylesIngredients", count





