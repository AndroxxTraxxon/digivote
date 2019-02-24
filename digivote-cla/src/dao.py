import sqlite3
import uuid


class CLADAO:

    sql_create_table = """
    CREATE TABLE IF NOT EXISTS voters (
        id 
    );
    """

    def __init__(self, db_name=None):
        self.db = sqlite3.connect(db_name)
        self.c = self.db.cursor()

    def startup_tables():
        pass

    def create_connection(self, db_name):
        self.db = sqlite3.connect(db_name or "cla_data.db")
    
    def create_table(self, table_name, columns):

