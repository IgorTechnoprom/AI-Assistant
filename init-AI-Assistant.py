import openai
import uuid
from dotenv import load_dotenv
import os
import time
from brain_AI_Assistant import add_thought, add_relationship, get_thoughts_by_session

# Load environment variables
load_dotenv()

# Retrieve the OpenAI API key from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")

if not openai.api_key:
    raise ValueError("OpenAI API key is not set. Please set it in your environment variables or .env file.")

# Function to chat with AI and store thoughts in mind-mapping structure
def chat_with_ai(prompt, session_id, parent_thought_id=None):
    """
    Sends the user's prompt to the OpenAI API, logs the conversation,
    and updates the mind-mapping structure.

    Parameters:
    - prompt (str): The user's input.
    - session_id (str): The unique session identifier.
    - parent_thought_id (int, optional): The ID of the parent thought.

    Returns:
    - ai_response (str): The AI assistant's response.
    - user_thought_id (int): The ID of the user's thought in the database.
    """
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=150
        )
        ai_response = response.choices[0].text.strip()
    except openai.error.OpenAIError as e:
        print(f"An error occurred with the OpenAI API: {e}")
        return None, None

    # Log the user input and AI response with the session
    try:
        user_thought_id = add_thought(prompt, session_id, "user")
        ai_thought_id = add_thought(ai_response, session_id, "ai")
    except Exception as e:
        print(f"An error occurred while adding thoughts to the database: {e}")
        return ai_response, None

    # If there's a parent thought, link it as a hierarchical relationship
    if parent_thought_id:
        try:
            add_relationship(parent_thought_id, user_thought_id, "hierarchical")
            add_relationship(user_thought_id, ai_thought_id, "hierarchical")
        except Exception as e:
            print(f"An error occurred while adding relationships: {e}")

    return ai_response, user_thought_id

# Generate unique session IDs
def create_new_session():
    """
    Generates a new unique session identifier.

    Returns:
    - str: A new session ID.
    """
    return str(uuid.uuid4())

# Retrieve past thoughts from a specific session
def retrieve_past_session(session_id):
    """
    Retrieves all thoughts associated with a given session ID.

    Parameters:
    - session_id (str): The session identifier.

    Returns:
    - list of tuples: Each tuple represents a thought record.
    """
    return get_thoughts_by_session(session_id)
