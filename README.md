 
# **This repository is actively maintained and updated. GRAG, LORA, and database support are in progress and will be added soon. Stay tuned for upcoming features!**
# **Real-Time AI Question-Answering Application**

This project is an AI-driven application designed to transcribe audio from any input source, identify questions, and provide real-time responses. The responses are generated by AI agents based on the transcribed questions. The answers are displayed in a graphical interface using Tkinter.

### **Table of Contents**
- [Overview](#overview)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Code Explanation](#code-explanation)
- [Future Enhancements](#future-enhancements)
- [License](#license)

---

### **Overview**

This project consists of an AI system that listens to any incoming audio, transcribes it, and identifies questions from the transcribed text. The AI then provides real-time answers, which are displayed in a Tkinter-based graphical interface. The project is designed to handle Zoom meetings, webinars, or any situation where real-time interaction with audio input is needed.

The system comprises AI agents for listening, transcribing, and answering the questions. It runs in a continuous loop to detect and respond to questions as they come in.

---
![image](321198319-3baa3752-8222-4857-a64c-c046693d6315.png)
[Source:https://github.com/lamm-mit/GraphReasoning/assets/101393859/3baa3752-8222-4857-a64c-c046693d6315]
### **Features**
- **Real-Time Transcription**: Captures and transcribes audio from any source.
- **AI Question-Answering**: Uses a trained AI model to generate responses based on transcribed questions.
- **Graphical Interface**: Displays the transcription and corresponding AI responses in a Tkinter window.
- **Extensible Agents**: Modular agent architecture for future AI agents or tools.
- **Continuous Listening**: The application continuously listens for questions and provides responses in real-time.

---

### **Requirements**
- **Python 3.7+**
- **Packages:**
  - `openai`
  - `pyaudio`
  - `tkinter`
  - `speech_recognition`
  - `langchain_community`
  - `crewai`
  - `sounddevice`
  - `torch`

You can install the dependencies via `pip`:
```bash
pip install openai pyaudio tkinter speech_recognition langchain_community crewai sounddevice torch
```

---

### **Installation**

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/your-username/real-time-ai-qa.git
   cd real-time-ai-qa
   ```

2. **Set up your Python environment:**
   If you're using `venv` or `conda`, create and activate your virtual environment.
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure OpenAI API key:**
   Ensure that you have your OpenAI API key set up as an environment variable. You can create a `.env` file in the root directory of the project and add:
   ```bash
   OPENAI_API_KEY=<your-openai-api-key>
   ```

---

### **Usage**

1. **Run the Application:**
   Execute the `main.py` file to start the application:
   ```bash
   python main.py
   ```

2. **Graphical User Interface:**
   - A Tkinter window will open, displaying transcribed questions and AI-generated responses.
   - The application will continuously listen for questions and provide responses in real-time.

---

### **Project Structure**

```
real-time-ai-qa/
├── src/
│   ├── agents.py             # AI agents for analyzing, identifying, and responding to questions
│   ├── crew.py               # Manages the crew of agents and coordinates task completion
│   ├── tasks.py              # Defines specific tasks for the agents (e.g., analyzing text, drafting responses)
│   ├── tools.py              # Custom tools for transcription, speech-to-text, etc.
├── graph.py                  # Defines the workflow for the transcription and question-answering process
├── nodes.py                  # Handles audio capture, transcription, and question detection
├── state.py                  # Manages application state (stores transcriptions, responses, etc.)
├── main.py                   # Main entry point that initializes and runs the application
├── requirements.txt          # Project dependencies
├── README.md                 # Project documentation
├── .env                      # Environment variables for API keys
```

```
[Capture Audio] ---> [Transcribe Audio] ---> [Identify Question] ---> [Generate Response]
      ^                                                            |
      |                                                            |
      +---------------------- [Listen for New Question] <----------+

```

---

### **Code Explanation**

#### **1. `main.py`**
- The main entry point for the application. It initializes the Tkinter window, starts the workflow process, and manages response display using threads.

#### **2. `graph.py`**
- The core of the application logic. Defines the workflow for checking transcribed questions, drafting responses, and updating the state.

#### **3. `nodes.py`**
- Handles audio capture and transcription. Includes methods to capture audio, transcribe it to text, and detect questions. It also manages real-time input processing.

#### **4. `agents.py`**
- Contains the AI agents that analyze the transcribed text and generate responses. Agents include:
  - `QuestionIdentificationAgent`: Identifies questions from transcribed text.
  - `ResponseAgent`: Generates responses using the OpenAI model.

#### **5. `crew.py`**
- Manages the crew of AI agents responsible for listening, answering, and managing tasks in a coordinated manner.

#### **6. `tasks.py`**
- Defines tasks for the agents to accomplish, such as transcribing audio, identifying key points, and generating answers.

#### **7. `state.py`**
- Manages the application's state, including the current transcription, questions, and AI responses. It also stores the status of active audio processing.

#### **8. `tools.py`**
- Provides custom tools such as audio transcription. The transcription tool uses the `speech_recognition` library to transcribe audio to text.

---

The code I provided outlines the structure for real-time question detection, transcription, and response generation. You can integrate this into your existing project by modifying your current files. Here's a breakdown of where each part of the code should go:

### 1. **Main Application (main.py)**
This will initialize and start the workflow, including real-time audio capture and response generation. Place this code inside your `main.py` file.

**main.py:**

```python
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
```

### 2. **Graph Logic (graph.py)**
This is where the overall workflow logic is set up. You’ll invoke the listening process, transcription, and passing it to agents for responses.

**graph.py:**

Ensure `WorkFlow` correctly integrates the tools for transcription and response. You’ll want to make sure that the nodes handling transcription and responses are properly linked:

```python
from dotenv import load_dotenv
load_dotenv()

from langgraph.graph import StateGraph
from .state import RealTimeAudioState
from .nodes import Nodes
from .crew import RealTimeQuestionCrew

class WorkFlow():
    def __init__(self):
        nodes = Nodes()
        workflow = StateGraph(RealTimeAudioState)

        workflow.add_node("transcribe_audio", nodes.transcribe_audio)
        workflow.add_node("process_response", RealTimeQuestionCrew().kickoff)

        workflow.set_entry_point("transcribe_audio")
        workflow.add_edge('transcribe_audio', 'process_response')
        workflow.add_edge('process_response', 'transcribe_audio')
        
        self.app = workflow.compile()
```

### 3. **Nodes Logic (nodes.py)**
This handles the logic for audio capture, transcription, and detection of questions. The `transcribe_audio` node will capture real-time audio and pass it to the agents.

**nodes.py:**

```python
import time
from .tools import transcribe_audio

class Nodes():
    def __init__(self):
        pass  # No Gmail API, just handling real-time transcription

    def transcribe_audio(self, state):
        print("# Transcribing audio in real-time")
        # Capture and transcribe audio in real-time
        transcribed_text = transcribe_audio()

        if transcribed_text:
            state['current_question'] = transcribed_text
        return state
```

### 4. **Crew Logic (crew.py)**
This handles the process where the agents analyze the transcribed question and generate a response.

**crew.py:**

```python
from crewai import Crew
from .agents import RealTimeAgents
from .tasks import RealTimeTasks

class RealTimeQuestionCrew():
    def __init__(self):
        agents = RealTimeAgents()
        self.response_agent = agents.question_response_agent()

    def kickoff(self, state):
        print("### Processing response for the transcribed question")
        tasks = RealTimeTasks()
        crew = Crew(
            agents=[self.response_agent],
            tasks=[
                tasks.answer_question_task(self.response_agent, state['current_question'])
            ],
            verbose=True
        )
        result = crew.kickoff()
        state["current_response"] = result['response']  # Store response
        return state
```

### 5. **Agent Logic (agents.py)**
This defines the agent responsible for analyzing the question and generating a response.

**agents.py:**

```python
from crewai import Agent
from .tools import question_response_tool

class RealTimeAgents():
    def __init__(self):
        pass  # No Gmail tools required

    def question_response_agent(self):
        return Agent(
            role='AI Assistant',
            goal='Answer real-time transcribed questions from audio.',
            backstory="You are an AI assistant tasked with answering real-time questions during a meeting.",
            tools=[question_response_tool],
            verbose=True,
            allow_delegation=False
        )
```

### 6. **Task Logic (tasks.py)**
This defines the specific tasks for the agents, including how they analyze the question and generate a response.

**tasks.py:**

```python
from crewai import Task
from textwrap import dedent

class RealTimeTasks:
    def answer_question_task(self, agent, question):
        return Task(
            description=dedent(f"""\
                Analyze the transcribed question and generate a relevant, concise response.
                QUESTION:
                -------
                {question}

                Your final answer MUST be a well-formed response to the question.
                """),
            agent=agent
        )
```

### 7. **State Logic (state.py)**
This keeps track of the app's state, including transcribed questions and responses.

**state.py:**

```python
from typing import TypedDict

class RealTimeAudioState(TypedDict):
    transcribed_text: str
    question_queue: list[str]
    response_queue: list[str]
    current_question: str
    current_response: str
    last_transcribed: str
    last_response: str
```

### 8. **Tools Logic (tools.py)**
You should already have your transcription tool here to capture audio and convert it to text, which was discussed earlier.

---


- Continuously listen for audio.
- Transcribe the detected questions in real-time.
- Process and answer the question using AI agents.
- Display the response in real time.
- Loop back to listen for new questions.

 
---

### **Future Enhancements**
- **Voice Command Detection**: Add the ability to recognize commands like "repeat last response" or "pause transcription."
- **Enhanced UI**: Implement a more sophisticated user interface with real-time indicators and controls for adjusting audio capture.
- **Multilingual Support**: Add support for transcription and responses in multiple languages.
- **Custom AI Models**: Integrate custom-trained models for better domain-specific responses.

---

### **License**

This project is licensed under the [MIT License](LICENSE). You are free to modify, distribute, and use this software in your own projects.

---

### **Conclusion**

This project demonstrates the use of real-time AI-driven systems to interact with live audio, transcribe it into text, and generate intelligent responses in real-time. The modularity of the AI agents allows for easy expansion of functionality, and the integration of a user-friendly interface ensures that the system can be effectively used in various live scenarios such as meetings, webinars, and other audio-based interactions.

### ***Readings***
1- GraphReasoning: Scientific Discovery through Knowledge Extraction and Multimodal Graph-based Representation and Reasoning
Markus J. Buehler, MIT, 2024 mbuehler@MIT.EDU

2- https://github.com/lamm-mit/GraphReasoning.git