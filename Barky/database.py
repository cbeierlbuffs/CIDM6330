'''
This module supports the following schema:

ID — The ID is the primary key of the table, or the main identifier of each record. It should automatically increment each time a new record is added, using the AUTOINCREMENT keyword. This column is an INTEGER type; the rest are TEXT.
Title — The title is required because it’s hard to skim your existing bookmarks if they’re only URLs. You can tell SQLite the column can’t be empty by using the NOT NULL keyword.
URL — The URL is required, so it gets NOT NULL as well.
Notes — Notes for a bookmark are optional, so only the TEXT specifier is necessary.
Date — The date the bookmark was added is required, so it gets NOT NULL.

SQL reference: https://www.w3schools.com/sql/default.asp

CREATE TABLE IF NOT EXISTS bookmarks
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    url TEXT NOT NULL,
    notes TEXT,
    date_added TEXT NOT NULL
);

'''

import sqlite3

class DatabaseManager:
    def __init__(self, database_filename) -> None:
        # added this to persist the name of the database file
        self.database_filename = database_filename
        self.connection = sqlite3.connect(database_filename)
    
    def __del__(self):
        self.connection.close()

    def _execute(self, statement, values=None):
        '''
        The _execute method should:

        1. Accept a statement as a string argument
        2. Get a cursor from the database connection
        3. Execute a statement using the cursor (more on this shortly)
        4. Return the cursor, which has stored the result of the executed statement (if any)        

        this is designed to use placeholders in SQL statements to insert values
        '''
        with self.connection: #https://www.pythonforbeginners.com/files/with-statement-in-python
            cursor = self.connection.cursor()
            cursor.execute(statement, values or [])
            return cursor

    def create_table(self, table_name, columns):
        '''
        The method offers a flexible way to pass data definition:
        1. Accept two arguments: the name of the table to create, and a dictionary of column names mapped to their data types and constraints
        2. Construct a CREATE TABLE SQL statement like the one shown earlier
        3. Execute the statement using DatabaseManager._execute
        '''
        columns_with_types = [
            f'{column_name} {data_type}'
            for column_name, data_type in columns.items() #this loop reads all column information
        ]

        self._execute(
            f'''
            CREATE TABLE IF NOT EXISTS {table_name}
            ({','.join(columns_with_types)});
            '''
        )

    def drop_table(self, table_name):
        '''
        The method drops a table:
        1. Accept two arguments: the name of the table to create, and a dictionary of column names mapped to their data types and constraints
        2. Construct a DROP TABLE SQL statement like the one shown earlier
        3. Execute the statement using DatabaseManager._execute
        '''
        self._execute(
            f'''
            DROP TABLE {table_name};
            '''
        )

    def add(self, table_name, data):
        '''
        Adding records using placeholders in SQL insert statements:
        INSERT INTO bookmarks
        (title, url, notes, date_added)
        VALUES (?, ?, ?, ?);

        This method: 
        1. Accepts two arguments: the name of the table, and a dictionary that maps column names to column values
        2. Constructs a placeholder string (a ? for each column specified)
        3. Constructs the string of the column names
        4. Gets the column values as a tuple (A dictionary’s .values() returns a dict_ values object, which happens not to work with sqlite3’s execute method.)
        5. Executes the statement with _execute, passing the SQL statement with placeholders and the column values as separate arguments
        '''
        placeholders = ', '.join('?' * len(data))
        column_names = ', '.join(data.keys())
        column_values = tuple(data.values())

        self._execute(
            f'''
            INSERT INTO {table_name}
            ({column_names})
            VALUES ({placeholders});
            ''',
            column_values,
        )

    def delete(self, table_name, criteria):
        '''
        We delete a record from the database in SQL using:
        DELETE FROM bookmarks
        WHERE ID = 3;

        To do so, this method:
        1. Accepts two arguments: the table name to delete records from, and a dictionary mapping column names to the value to match on. The criteria should be a required argument, because you don’t want to delete all your records.
        2. Constructs a string of placeholders for the WHERE clause.
        3. Constructs the full DELETE FROM query and executes it with _execute.

        '''
        placeholders = [f'{column} = ?' for column in criteria.keys()]
        delete_criteria = ' AND '.join(placeholders)
        self._execute(
            f'''
            DELETE FROM {table_name}
            WHERE {delete_criteria};
            ''',
            tuple(criteria.values()), #https://www.w3schools.com/python/python_tuples.asp
        )

    def select(self, table_name, criteria=None, order_by=None):
        '''
        we commonly need to find, select, and sort data
        SQL select:
        SELECT * FROM bookmarks
        WHERE ID = 3;

        SQL sort:
        SELECT * FROM bookmarks
        WHERE ID = ?
        ORDER BY title;
        '''
        criteria = criteria or {}

        query = f'SELECT * FROM {table_name}'
        if criteria:
            placeholders = [f'{column} = ?' for column in criteria.keys()]
            select_criteria = ' AND '.join(placeholders)
            query += f' WHERE {select_criteria}'

        if order_by:
            query += f' ORDER BY {order_by}'

        return self._execute(
            query,
            tuple(criteria.values()),
        )

import pytest
 
def test_create_table_mapped_method(dbm, table_name, table_structure):
    dbm.create_table(table_name,table_structure)
    stmt_cursor = dbm._execute(
        f'''
        SELECT count(*) FROM sqlite_master WHERE type='table' AND name='{table_name}';
        '''
    )
    dbm.connection.commit()
    table_count = stmt_cursor.fetchone()[0]
    dbm.connection.close
    assert table_count == 1

def test_drop_table(dbm, table_name):
    stmt_cursor = dbm._execute(
        f'''
        CREATE TABLE '{table_name}' (id int PRIMARY KEY);
        '''
    )
    dbm.connection.commit()
    dbm.drop_table(table_name)
    stmt_cursor = dbm._execute(
        f'''
        SELECT count(*) FROM sqlite_master WHERE type='table' AND name='{table_name}';
        '''
    )
    dbm.connection.commit()
    table_count = stmt_cursor.fetchone()[0]
    dbm.connection.close()
    assert table_count == 0

def test_add_record(dbm, table_name, table_structure, record1):
    dbm.create_table(table_name,table_structure)
    dbm.add(table_name,record)
    dbm.connection.commit()
    stmt_cursor = dbm._execute(
        f'''
        SELECT count(*) FROM {table_name} WHERE title='{record1['title']}';
        '''
    )
    record_count = stmt_cursor.fetchone()[0]
    dbm.connection.close()
    assert record_count == 1

def test_delete_records(dbm, table_name, table_structure, record1):
    del_criteria = {
        "title" : "testtitle",
        "url" : "hxxp://www.test.url/"
    }
    del_criteria_string = ''
    del_criteria_len = len(del_criteria)
    del_criteria_cnt = 1
    for del_criteria_key in del_criteria:   
        del_criteria_string = del_criteria_string + del_criteria_key + "=" + "'" + del_criteria[del_criteria_key] + "'"
        if del_criteria_len > 1 and del_criteria_cnt < del_criteria_len:
            del_criteria_string = del_criteria_string + " AND "
            del_criteria_cnt = del_criteria_cnt + 1 
    dbm.create_table(table_name,table_structure)
    dbm.add(table_name,record1)
    dbm.delete(table_name,del_criteria)
    dbm.connection.commit()

    stmt_cursor = dbm._execute(
        f'''
        SELECT count(*) FROM {table_name} WHERE {del_criteria_string};
        '''
    )
    record_count = stmt_cursor.fetchone()[0]
    dbm.connection.close()
    assert record_count == 0

def test_select_records(dbm, table_name, table_structure, record1, record2, record3):
   
    select_criteria = {
        "url" : "hxxp://www.test.url/"
    }
    dbm.create_table(table_name,table_structure)
    dbm.add(table_name,record1)
    dbm.add(table_name,record2)
    dbm.add(table_name,record3)
    dbm.connection.commit()   
    dbm.select(table_name,select_criteria)
    stmt_cursor = dbm._execute(
        f'''
        SELECT * FROM {table_name} WHERE url='{select_criteria['url']}' ORDER BY date_added;
        '''
    )
    first_record_id = stmt_cursor.fetchone()[0]
    dbm.connection.close()
    assert first_record_id == 2    

#test using python -m pytest .\database.py