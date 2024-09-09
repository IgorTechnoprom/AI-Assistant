import sqlite3

# Connect to SQLite database (or create it)
conn = sqlite3.connect('your_database.db')
cursor = conn.cursor()

# Read SQL file
with open('database.sql', 'r') as file:
    sql_script = file.read()

# Execute SQL script
cursor.executescript(sql_script)
conn.commit()
conn.close()
