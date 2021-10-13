import sqlite3

from .manager import DB_FILE, TBL_NAME, SQL, MEMORY_LIST


class Database():

    def __init__(self):
        # Create the database or connect to it
        self.cnn = sqlite3.connect(DB_FILE)
        self.table = TBL_NAME
        try:
            self.init_table()
        except sqlite3.OperationalError:
            pass

    def init_table(self):
        self.crud_query(f'''CREATE TABLE {self.table} {SQL}''')
        self.create_data('', 0, 0, MEMORY_LIST)

    def crud_query(self, query, *args):
        cur = self.cnn.cursor() # Create cursor
        if args != (): cur.executemany(query, *args) # Make the query list
        else: cur.execute(query) # Make the query
        self.data = cur.fetchall() # Search the data
        self.cnn.commit() # Commit changes
        # self.cnn.close() # Close connection

    def create_data(self, username='', score=0, highscore=0, *args):
        if args != ():
            self.crud_query(f'INSERT INTO {self.table} VALUES (?, ?, ?)', *args)
        else:
            self.crud_query(f'INSERT INTO {self.table} VALUES ("{username}", {score}, {highscore})')

    def read_data(self, field=None, tidy=None):
        if tidy!= None:
            self.crud_query(f'SELECT * FROM {self.table} ORDER BY {field} DESC LIMIT {tidy}')
        elif field != None:
            self.crud_query(f'SELECT * FROM {self.table} WHERE username like "{field}"')
        else:
            self.crud_query(f'SELECT * FROM {self.table}')

        return self.data

    def update_data(self, username, score, highscore):
        # self.crud_query(f'UPDATE {self.table} SET score={score} WHERE username like "{username}"')
        self.crud_query(f'UPDATE {self.table} SET highscore={highscore} WHERE username like "{username}"')

    def delete_data(self, username):
        self.crud_query(f'DELETE FROM {self.table} WHERE username like "{username}"')

    def __del__(self):
        self.cnn.close() # Close connection
