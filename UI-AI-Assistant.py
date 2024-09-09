import tkinter as tk
from tkinter import scrolledtext
import subprocess
from init_AI_Assistant import chat_with_ai, create_new_session, retrieve_past_session

# Create a new session when the app starts
session_id = create_new_session()
parent_thought_id = None  # Initialize with no parent thought

def on_submit():
    global parent_thought_id
    user_input = input_text.get("1.0", tk.END).strip()
    if user_input:
        # Get AI response and log thought relationship
        ai_response, user_thought_id = chat_with_ai(user_input, session_id, parent_thought_id)
        
        # Display user input and AI response
        response_text.insert(tk.END, "You: " + user_input + "\n")
        response_text.insert(tk.END, "AI: " + ai_response + "\n\n")
        
        # Set the parent thought for the next input (continuing the thought thread)
        parent_thought_id = user_thought_id
        
        # Clear the input text box
        input_text.delete("1.0", tk.END)

def show_mind_map():
    subprocess.run(["python", "mind_map_visualization.py"])  # Adjust the script name as needed

def retrieve_session():
    session_data = retrieve_past_session(session_id)
    if session_data:
        response_text.insert(tk.END, "\n--- Previous Session ---\n")
        for thought in session_data:
            sender = "You" if thought[3] == "user" else "AI"
            response_text.insert(tk.END, f"{sender}: {thought[2]}\n")
        response_text.insert(tk.END, "\n")

root = tk.Tk()
root.title("AI Assistant")

# Input area
input_label = tk.Label(root, text="Enter your thought:")
input_label.pack()
input_text = scrolledtext.ScrolledText(root, height=5)
input_text.pack()

# Submit button
submit_button = tk.Button(root, text="Submit", command=on_submit)
submit_button.pack()

# Visualization button
visualize_button = tk.Button(root, text="Show Mind Map", command=show_mind_map)
visualize_button.pack()

# Retrieve past session button
retrieve_button = tk.Button(root, text="Retrieve Past Session", command=retrieve_session)
retrieve_button.pack()

# Response area
response_text = scrolledtext.ScrolledText(root, height=10)
response_text.pack()

root.mainloop()
