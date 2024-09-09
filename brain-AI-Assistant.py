import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('thoughts.db')
cursor = conn.cursor()

# Create the necessary tables
cursor.execute('''CREATE TABLE IF NOT EXISTS thoughts
                  (id INTEGER PRIMARY KEY, 
                   session_id TEXT, 
                   thought TEXT, 
                   sender TEXT, 
                   date TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS relationships
                  (id INTEGER PRIMARY KEY, 
                   parent_thought_id INTEGER, 
                   child_thought_id INTEGER, 
                   relationship_type TEXT CHECK(relationship_type IN ('child', 'parent', 'jump')),
                   FOREIGN KEY (parent_thought_id) REFERENCES thoughts(id),
                   FOREIGN KEY (child_thought_id) REFERENCES thoughts(id))''')

# Add a thought to the database
def add_thought(thought, session_id, sender):
    cursor.execute("INSERT INTO thoughts (session_id, thought, sender) VALUES (?, ?, ?)", 
                   (session_id, thought, sender))
    conn.commit()
    return cursor.lastrowid

# Add a relationship between thoughts
def add_relationship(parent_id, child_id, relationship_type):
    cursor.execute("INSERT INTO relationships (parent_thought_id, child_thought_id, relationship_type) VALUES (?, ?, ?)",
                   (parent_id, child_id, relationship_type))
    conn.commit()

# Retrieve thoughts by session ID
def get_thoughts_by_session(session_id):
    cursor.execute("SELECT * FROM thoughts WHERE session_id = ?", (session_id,))
    return cursor.fetchall()

# Retrieve relationships for a specific thought
def get_relationships(thought_id):
    cursor.execute("SELECT * FROM relationships WHERE parent_thought_id = ? OR child_thought_id = ?", (thought_id, thought_id))
    return cursor.fetchall()

def close_connection():
    conn.close()
