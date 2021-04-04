import sqlite3

class Entity:
    """ An entity class"""
    def __init__(self, id, name, subname, address, city, state):
        self.id = id
        self.name = name
        self.subname = subname
        self.address = address
        self.city  = city
        self.state = state

    def __repr__(self):
        return "Entity:'{}', '{}', {}".format(self.name, self.subname, self.state)
