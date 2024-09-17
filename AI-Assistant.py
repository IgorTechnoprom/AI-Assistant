import sys
import uuid
import logging
import os
import subprocess
from brain_integration import create_thought, search_thoughts, get_thought_details
from mind_map_visualization import update_visualization
from nlp_analysis import analyze_thought

# Set up logging
logging.basicConfig(filename='ai_assistant.log', level=logging.INFO)

# Path to your database file
DATABASE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database', 'thoughts.db')

def initialize_database():
    """
    Checks if the database exists. If not, runs init-database.py to initialize it.
    """
    if not os.path.exists(DATABASE_PATH):
        print("Database not found. Initializing the database...")
        try:
            # Run init-database.py
            init_script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'init-database.py')
            result = subprocess.run(['python', init_script_path], check=True)
            print("Database initialized successfully.")
        except subprocess.CalledProcessError as e:
            print(f"An error occurred while initializing the database: {e}")
            sys.exit(1)
    else:
        print("Database found. Proceeding with the application.")

def get_user_choice():
    while True:
        choice = input("Enter your choice (1-4): ")
        if choice in ['1', '2', '3', '4']:
            return choice
        else:
            print("Invalid option. Please select a valid option.")

def main():
    # Initialize the database if not present
    initialize_database()

    # Generate a session ID
    session_id = str(uuid.uuid4())

    print("Welcome to AI Assistant!")
    print(f"Your session ID is {session_id}")
    while True:
        print("\nSelect an option:")
        print("1. Create a new thought")
        print("2. Search for thoughts")
        print("3. Get details of a specific thought")
        print("4. Exit")
        choice = get_user_choice()
        
        if choice == '1':
            create_new_thought(session_id)
        elif choice == '2':
            search_for_thoughts(session_id)
        elif choice == '3':
            get_thought_information(session_id)
        elif choice == '4':
            print("Exiting AI Assistant.")
            break

def create_new_thought(session_id):
    brain_id = input("Enter the Brain ID: ")
    thought_name = input("Enter the name of the new thought: ")
    thought_description = input("Enter a description for the thought (optional): ")
    try:
        # Analyze the thought description using NLP
        analysis_result = analyze_thought(thought_description)
        entities = analysis_result['entities']
        keywords = analysis_result['keywords']

        print("Extracted Entities:")
        for entity_text, entity_label in entities:
            print(f" - {entity_text} ({entity_label})")

        print("Extracted Keywords:")
        print(", ".join(keywords))

        # Proceed to create the thought in TheBrain
        result = create_thought(brain_id, thought_name, thought_description)
        if result:
            print(f"Thought created successfully. Thought ID: {result['id']}")
            logging.info(f"Created thought '{thought_name}' with ID {result['id']} in brain {brain_id}")
            update_visualization()
        else:
            print("Failed to create thought.")
    except Exception as e:
        print(f"An error occurred while creating the thought: {e}")
        logging.error(f"Error creating thought: {e}")

def search_for_thoughts(session_id):
    brain_id = input("Enter the Brain ID: ")
    query = input("Enter the search query: ")
    try:
        results = search_thoughts(brain_id, query)
        if results:
            print("Search Results:")
            for thought in results:
                print(f"Thought ID: {thought['id']}, Name: {thought['name']}")
        else:
            print("No thoughts found matching the query.")
        logging.info(f"Searched for '{query}' in brain {brain_id}")
    except Exception as e:
        print(f"An error occurred during the search: {e}")
        logging.error(f"Error searching thoughts: {e}")

def get_thought_information(session_id):
    brain_id = input("Enter the Brain ID: ")
    thought_id = input("Enter the Thought ID: ")
    try:
        thought_details = get_thought_details(brain_id, thought_id)
        if thought_details:
            print("Thought Details:")
            print(f"ID: {thought_details['id']}")
            print(f"Name: {thought_details['name']}")
            print(f"Description: {thought_details.get('description', 'No description available.')}")
            logging.info(f"Retrieved details for thought ID {thought_id} in brain {brain_id}")
        else:
            print("Failed to retrieve thought details.")
    except Exception as e:
        print(f"An error occurred while retrieving thought details: {e}")
        logging.error(f"Error retrieving thought details: {e}")

if __name__ == "__main__":
    main()
