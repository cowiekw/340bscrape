import sqlite3
import os
from core.entity import Entity

class SQLPipeline:
    """ An entity class"""
    def __init__(self, name = 'entity'):
        self.conn = None
        self.db_name = name
        self.last_post_id = 0

    def create_connection(self, erase_first=False):
        if(erase_first):
            try:
                os.remove(('{0}.db').format(self.db_name))
                print("database was removed")
            except Exception as ex:
                print("database was not removed: ", ex)
                pass

        print("normal SQL connection created")
        self.conn = sqlite3.connect(('data/{0}.db').format(self.db_name))
        db  = self.conn.cursor()

    def create_table(self):
        db = self.conn.cursor()
        db.execute("""DROP TABLE IF EXISTS entity""")
        db.execute("""CREATE TABLE entity
        (id TEXT, name TEXT, subname TEXT,
        address TEXT, city TEXT, state TEXT, PRIMARY KEY(id))
        """)

        db.execute("""DROP TABLE IF EXISTS parent""")
        db.execute("""CREATE table parent
        (id INTEGER UNIQUE NOT NULL, entity_id TEXT, name TEXT,
        address TEXT, city TEXT, state TEXT, PRIMARY KEY(id), FOREIGN KEY(entity_id) REFERENCES entity(id))
        """)

        db.execute("""DROP TABLE IF EXISTS child""")
        db.execute("""CREATE table child (id INTEGER UNIQUE NOT NULL, entity_id TEXT, parent_name TEXT, name TEXT,
        address TEXT, city TEXT, state TEXT, PRIMARY KEY(id), FOREIGN KEY(entity_id) REFERENCES entity(id), FOREIGN KEY(name) REFERENCES parent(name))""") #

        db.execute("""DROP TABLE IF EXISTS contract""")
        db.execute("""CREATE table contract
        (contract_id TEXT,  name TEXT, subname TEXT, address TEXT, city TEXT, state TEXT, PRIMARY KEY(contract_id))""")

    def store_data(self, entities_list, table_name):
        db = self.conn.cursor()
        if table_name == 'entity' or table_name == 'entities':
            for ent in entities_list:
                query = '''INSERT INTO entity (id, name, subname, address, city, state) VALUES(?, ?, ?, ?, ?, ?)'''
                data = (ent.id, ent.name, ent.subname, ent.address, ent.city, ent.state)
                db.execute(query, data)
                print(ent.name, "entity was stored in table")

        elif (table_name == 'parent') or (table_name == 'parents'):
            for ent in entities_list:
                query = '''INSERT INTO parent (entity_id, name, address, city, state) VALUES(?, ?, ?, ?, ?)'''
                data = (ent.id, ent.name, ent.address, ent.city, ent.state)
                db.execute(query, data)

        elif table_name == 'child' or table_name == 'children':
            for ent in entities_list:
                query = '''INSERT INTO child (entity_id, parent_name, name, address, city, state) VALUES(?, ?, ?, ?, ?, ?)'''
                data = (ent.id, ent.name, ent.subname, ent.address, ent.city, ent.state)
                db.execute(query, data)

    def save_changes(self):
        self.conn.commit()
        self.conn.close()
# Reference: https://github.com/casperbh96/Web-Scraping-Reddit/blob/master/scraper.py
