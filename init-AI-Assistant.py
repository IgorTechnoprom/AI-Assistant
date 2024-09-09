import openai
import uuid
from brain_AI_Assistant import add_thought, add_relationship, get_thoughts_by_session

openai.api_key = "YOUR_OPENAI_API_KEY"

# Function to chat with AI and store thoughts in mind-mapping structure
def chat_with_ai(prompt, session_id, parent_thought_id=None):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150
    )
    ai_response = response.choices[0].text.strip()
    
    # Log the user input and AI response with the session
    user_thought_id = add_thought(prompt, session_id, "user")
    ai_thought_id = add_thought(ai_response, session_id, "ai")
    
    # If there's a parent thought, link it as a child
    if parent_thought_id:
        add_relationship(parent_thought_id, user_thought_id, "child")
        add_relationship(user_thought_id, ai_thought_id, "child")
    
    return ai_response, user_thought_id

# Generate unique session IDs
def create_new_session():
    return str(uuid.uuid4())

# Retrieve past thoughts from a specific session
def retrieve_past_session(session_id):
    return get_thoughts_by_session(session_id)
