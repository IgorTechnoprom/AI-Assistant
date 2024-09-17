import sqlite3

class ThoughtDatabase:
    """
    A class to manage thoughts and relationships in the SQLite database.
    """

    def __init__(self, db_file='thoughts.db'):
        self.db_file = db_file
        self._initialize_database()

    def _initialize_database(self):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            # Create the necessary tables
            cursor.execute('''CREATE TABLE IF NOT EXISTS thoughts
                              (id INTEGER PRIMARY KEY, 
                               session_id TEXT NOT NULL, 
                               thought TEXT NOT NULL, 
                               sender TEXT NOT NULL CHECK(sender IN ('user', 'ai')), 
                               date TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')

            cursor.execute('''CREATE TABLE IF NOT EXISTS relationships
                              (id INTEGER PRIMARY KEY, 
                               from_thought_id INTEGER NOT NULL, 
                               to_thought_id INTEGER NOT NULL, 
                               relationship_type TEXT NOT NULL CHECK(relationship_type IN ('hierarchical', 'jump')),
                               FOREIGN KEY (from_thought_id) REFERENCES thoughts(id),
                               FOREIGN KEY (to_thought_id) REFERENCES thoughts(id))''')

    def add_thought(self, thought, session_id, sender):
        """
        Adds a new thought to the database.

        Parameters:
        - thought (str): The content of the thought.
        - session_id (str): The session identifier.
        - sender (str): The sender of the thought ('user' or 'ai').

        Returns:
        - int: The ID of the newly inserted thought, or None if an error occurred.
        """
        if sender not in ('user', 'ai'):
            print(f"Invalid sender: {sender}")
            return None
        if not thought or not session_id:
            print("Thought and session_id cannot be empty.")
            return None

        try:
            with sqlite3.connect(self.db_file) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO thoughts (session_id, thought, sender) VALUES (?, ?, ?)", 
                    (session_id, thought, sender))
                conn.commit()
                return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"An error occurred while adding a thought: {e}")
            return None

    def add_relationship(self, from_thought_id, to_thought_id, relationship_type):
        """
        Adds a relationship between two thoughts.

        Parameters:
        - from_thought_id (int): The ID of the source thought.
        - to_thought_id (int): The ID of the target thought.
        - relationship_type (str): The type of relationship ('hierarchical' or 'jump').

        Returns:
        - None
        """
        if relationship_type not in ('hierarchical', 'jump'):
            print(f"Invalid relationship type: {relationship_type}")
            return

        try:
            with sqlite3.connect(self.db_file) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO relationships (from_thought_id, to_thought_id, relationship_type) VALUES (?, ?, ?)",
                    (from_thought_id, to_thought_id, relationship_type))
                conn.commit()
        except sqlite3.Error as e:
            print(f"An error occurred while adding a relationship: {e}")

    def get_thoughts_by_session(self, session_id):
        """
        Retrieves all thoughts associated with a given session ID.

        Parameters:
        - session_id (str): The session identifier.

        Returns:
        - list of tuples: Each tuple represents a thought record.
        """
        try:
            with sqlite3.connect(self.db_file) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM thoughts WHERE session_id = ?", (session_id,))
                return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"An error occurred while retrieving thoughts: {e}")
            return []

    def get_relationships(self, thought_id):
        """
        Retrieves all relationships involving a specific thought.

        Parameters:
        - thought_id (int): The ID of the thought.

        Returns:
        - list of tuples: Each tuple represents a relationship record.
        """
        try:
            with sqlite3.connect(self.db_file) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT * FROM relationships WHERE from_thought_id = ? OR to_thought_id = ?", 
                    (thought_id, thought_id))
                return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"An error occurred while retrieving relationships: {e}")
            return []
