import sqlite3
from core.entity import Entity

class SQLPipeline:
    """ An entity class"""
    def __init__(self, name = 'entity'):
        self.conn = None
        self.db_name = name
        self.last_post_id = 0
        self.create_connection()
        self.create_table()
        self.save_changes()
        # self.store_data()

    def create_connection(self, erase_first=False):
        if (erase_first==True):
            try:
                os.remove(('{0}.db').format(self.db_name))
            except Exception:
                pass
        self.conn = sqlite3.connect(('data/{0}.db').format(self.db_name))
        # :memory:
        db  = self.conn.cursor()

    def create_table(self):
        db = self.conn.cursor()

        # PRAGMA FOREIGN KEYS

        db.execute("""DROP TABLE IF EXISTS entity""")
        db.execute("""CREATE TABLE entity
        (id TEXT, name TEXT, subname TEXT, address TEXT, city TEXT, state TEXT, PRIMARY KEY(id))
        """) # Add Status field later

        db.execute("""DROP TABLE IF EXISTS parent""")
        db.execute("""CREATE table parent
        (id TEXT, name TEXT UNIQUE, subname TEXT, address TEXT, city TEXT, state TEXT, PRIMARY KEY(id)) """)

        db.execute("""DROP TABLE IF EXISTS child""")
        db.execute("""CREATE table child(child_id TEXT, parent_id INTEGER, name TEXT, subname TEXT, address TEXT, city TEXT, state TEXT, PRIMARY KEY(child_id), FOREIGN KEY(parent_id) REFERENCES parent(id))""")

        db.execute("""DROP TABLE IF EXISTS contract""")
        db.execute("""CREATE table contract
        (contract_id TEXT, parent_id INTEGER, name TEXT, subname TEXT, address TEXT, city TEXT, state TEXT, PRIMARY KEY(contract_id), FOREIGN KEY(parent_id) REFERENCES parent(id))""")

    def save_changes(self):
        self.conn.commit()
        self.conn.close()

    def store_data(self, entities_list, table_name):
        db = self.conn.cursor()
        if table_name == 'entity':
            for ent in entities_list:
                query = '''INSERT INTO entity (id, name, subname, address, city, state) VALUES(?, ?, ?, ?, ?, ?)'''
                data = (ent.id, ent.name, ent.subname, ent.address, ent.city, ent.state)
                db.execute(query, data)
                print(ent.name, "entity was stored in table")
            # db.execute('''INSERT INTO entities(id, name, subname, address, city, state) VALUES(?, ?, ?, ?, ?, ?)''', ent.id, ent.name, ent.subname, ent.address, ent.city, ent.state)

    def process_entity(self, ent):
        self.store_db(entity)
        print("Pipeline: "+ ent.name) #print("Pipeline: "+ entity['name'][0])
        return entity



# Reference: https://github.com/casperbh96/Web-Scraping-Reddit/blob/master/scraper.py
