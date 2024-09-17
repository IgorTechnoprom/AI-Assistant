import sqlite3
import sys
import os

# Define paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, 'database', 'thoughts.db')
sql_path = os.path.join(BASE_DIR, 'database', 'database.sql')

def init_database(db_file, sql_file):
    try:
        # Ensure the database directory exists
        os.makedirs(os.path.dirname(db_file), exist_ok=True)
        
        # Connect to SQLite database (or create it)
        with sqlite3.connect(db_file) as conn:
            cursor = conn.cursor()
            
            # Read SQL file
            try:
                with open(sql_file, 'r') as file:
                    sql_script = file.read()
            except FileNotFoundError:
                print(f"Error: SQL file not found at '{sql_file}'.")
                sys.exit(1)
            
            # Execute SQL script
            cursor.executescript(sql_script)
            conn.commit()
            print(f"Database '{db_file}' initialized successfully.")
    except sqlite3.Error as e:
        print(f"An error occurred while initializing the database: {e}")
        sys.exit(1)

if __name__ == "__main__":
    init_database(db_path, sql_path)
