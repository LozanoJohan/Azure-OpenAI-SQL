# sql_db.py

import pyodbc
import pandas as pd
import json

def create_connection():
    """ Create or connect to an msSQL Server database """
    connection = None

    server = 'localhost'
    database = 'BRUDER2'
    username = 'jlozanol'
    password = 'JPMvef56*'

    connection_string = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'

    try:
        connection = pyodbc.connect(connection_string)
    except Exception as e:
        print(f"Error: {str(e)}")

    return connection

def query_database(query):
    """ Run SQL query and return results in a dataframe """
    conn = create_connection()
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def query_database(query):
    """ Run SQL query and return results in a dataframe """
    conn = create_connection()
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df





def get_schema_representation():
    """ Get the database schema in a JSON-like format """
    conn = create_connection()
    cursor = conn.cursor()
    
    # Query to get all table names
    cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_type = 'BASE TABLE';")
    tables = cursor.fetchall()
    
    db_schema = {}
    
    for table in tables:
        table_name = table[0]
        
        # Query to get column details for each table
        cursor.execute(f"SELECT COLUMN_NAME, DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table_name}';")
        columns = cursor.fetchall()
        
        column_details = {}

        for column in columns:
            column_name = column[0]
            column_type = column[1]
            column_details[column_name] = column_type
        
        db_schema[table_name] = column_details
    
    conn.close()
    return db_schema


def get_schema_representation_from_json():
    with open("schema_lite.json", 'r') as archivo_json:
        return json.load(archivo_json)

# This will create the table and insert 100 rows when you run sql_db.py
if __name__ == "__main__":

    db_schema = get_schema_representation()
    print(db_schema)

    # Store db schema in JSON file
    with open("schema.json", "w") as f:
        json.dump(db_schema, f)



