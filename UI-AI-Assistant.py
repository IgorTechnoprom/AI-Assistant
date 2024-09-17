import tkinter as tk
from tkinter import scrolledtext
import threading
from init_AI_Assistant import chat_with_ai, create_new_session, retrieve_past_session
from mind_map_visualization import visualize_mind_map

class AIAssistantApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Assistant")

        # Create a new session
        self.session_id = create_new_session()
        self.parent_thought_id = None  # Initialize with no parent thought

        # Input area
        self.input_label = tk.Label(root, text="Enter your thought:")
        self.input_label.pack()
        self.input_text = scrolledtext.ScrolledText(root, height=5)
        self.input_text.pack()

        # Buttons frame
        self.buttons_frame = tk.Frame(root)
        self.buttons_frame.pack()

        # Submit button
        self.submit_button = tk.Button(self.buttons_frame, text="Submit", command=self.on_submit)
        self.submit_button.pack(side=tk.LEFT)

        # Visualization button
        self.visualize_button = tk.Button(self.buttons_frame, text="Show Mind Map", command=self.show_mind_map)
        self.visualize_button.pack(side=tk.LEFT)

        # Retrieve past session button
        self.retrieve_button = tk.Button(self.buttons_frame, text="Retrieve Past Session", command=self.retrieve_session)
        self.retrieve_button.pack(side=tk.LEFT)

        # Response area
        self.response_text = scrolledtext.ScrolledText(root, height=10)
        self.response_text.pack()

    def on_submit(self):
        threading.Thread(target=self.process_user_input).start()

    def process_user_input(self):
        user_input = self.input_text.get("1.0", tk.END).strip()
        if user_input:
            # Disable the submit button to prevent multiple clicks
            self.submit_button.config(state=tk.DISABLED)
            try:
                # Get AI response and log thought relationship
                ai_response, user_thought_id = chat_with_ai(user_input, self.session_id, self.parent_thought_id)

                # Update conversation in the GUI
                self.root.after(0, self.update_conversation, user_input, ai_response)

                # Set the parent thought for the next input
                self.parent_thought_id = user_thought_id
            except Exception as e:
                self.root.after(0, self.response_text.insert, tk.END, f"Error: {e}\n")
            finally:
                # Re-enable the submit button
                self.root.after(0, self.submit_button.config, {'state': tk.NORMAL})
                # Clear the input text box
                self.root.after(0, self.input_text.delete, "1.0", tk.END)

    def update_conversation(self, user_input, ai_response):
        self.response_text.insert(tk.END, "You: " + user_input + "\n")
        self.response_text.insert(tk.END, "AI: " + ai_response + "\n\n")
        self.response_text.see(tk.END)  # Scroll to the end

    def show_mind_map(self):
        try:
            visualize_mind_map()
        except Exception as e:
            self.response_text.insert(tk.END, f"Error displaying mind map: {e}\n")

    def retrieve_session(self):
        try:
            session_data = retrieve_past_session(self.session_id)
            if session_data:
                self.response_text.insert(tk.END, "\n--- Previous Session ---\n")
                for thought in session_data:
                    thought_id, session_id, thought_text, sender, date = thought
                    sender_label = "You" if sender == "user" else "AI"
                    self.response_text.insert(tk.END, f"{sender_label}: {thought_text}\n")
                self.response_text.insert(tk.END, "\n")
            else:
                self.response_text.insert(tk.END, "No previous session data found.\n")
        except Exception as e:
            self.response_text.insert(tk.END, f"Error retrieving session: {e}\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = AIAssistantApp(root)
    root.mainloop()
