import pyodbc
import os
import sys
# from pathlib import Path

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config.config import DB_SERVER, DB_USERNAME, DB_PASSWORD






def get_db_connection(db):
  

    try:
        
        connection_string = (
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={DB_SERVER};"
            f"DATABASE={db};"
            f"UID={DB_USERNAME};"
            f"PWD={DB_PASSWORD}"
        )
       
        conn = pyodbc.connect(connection_string)
       
        return conn
    except pyodbc.Error as e:
    
        print(f"Error connecting to the database: {e}")
        raise




