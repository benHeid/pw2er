from peewee import *

db = SqliteDatabase("people.db")


class House(Model):
    street = CharField()


class Person(Model):
    name = CharField()
    birthday = DateField()
    home = ForeignKeyField(House, backref="inhabitants")
    class Meta:
        database = db # This model uses the "people.db" database.

class Pet(Model):
    owner = ForeignKeyField(Person, backref='pets')
    name = CharField()
    animal_type = CharField()

    class Meta:
        database = db # this model uses the "people.db" database

class Dog(Pet):
    type = CharField()

class Golder(Dog):
    color = CharField()
    mom = ForeignKeyField('self', backref="mom")

