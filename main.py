'''
import threading
from src.graph import WorkFlow

def process_responses(app, state):
    while True:
        # If a response is available, display it
        if state['current_response']:
            print(f"AI Response: {state['current_response']}")
            state['current_response'] = ""  # Reset after display

def start_application():
    # Initialize the workflow
    app = WorkFlow().app
    
    # State to store transcription, questions, and responses
    state = {
        "transcribed_text": "",
        "question_queue": [],
        "response_queue": [],
        "current_question": "",
        "current_response": "",
        "last_transcribed": None,
        "last_response": None,
    }

    # Start the app (this will handle the continuous listening and question answering)
    app.invoke(state)

if __name__ == "__main__":
    # Start the workflow
    app_thread = threading.Thread(target=start_application)
    app_thread.start()

    # Start the response processing in a separate thread
    process_thread = threading.Thread(target=process_responses, args=(app_thread,))
    process_thread.start()

    # Keep the application running, waiting for new transcriptions and responses
    try:
        while True:
            app_thread.join(1)
            process_thread.join(1)
    except KeyboardInterrupt:
        print("Application interrupted.")
'''
import threading
import tkinter as tk
from src.graph import WorkFlow

class ResponseDisplay:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Real-Time Response")
        
        # Create a text box to display the transcribed questions and answers
        self.text_box = tk.Text(self.root, height=20, width=80)
        self.text_box.pack()

    def update_text(self, message):
        # Insert new message into the text box
        self.text_box.insert(tk.END, message + "\n")
        self.text_box.see(tk.END)  # Scroll to the end of the text box

def process_responses(state, display):
    while True:
        if state['current_response']:
            # Display the response in the Tkinter window
            display.update_text(f"AI Response: {state['current_response']}")
            state['current_response'] = ""  # Reset after display

def start_application(display):
    # Initialize the workflow
    app = WorkFlow().app
    
    # State to store transcription, questions, and responses
    state = {
        "transcribed_text": "",
        "question_queue": [],
        "response_queue": [],
        "current_question": "",
        "current_response": "",
        "last_transcribed": None,
        "last_response": None,
    }

    # Start the app (this will handle the continuous listening and question answering)
    app.invoke(state)

    # Start the response processing in a separate thread
    response_thread = threading.Thread(target=process_responses, args=(state, display))
    response_thread.start()

if __name__ == "__main__":
    # Create Tkinter window
    root = tk.Tk()
    display = ResponseDisplay(root)

    # Start the workflow and processing in a separate thread
    app_thread = threading.Thread(target=start_application, args=(display,))
    app_thread.start()

    # Start the Tkinter main loop
    root.mainloop()
