#Task level LLM
'''
import wandb
import openai  # Import OpenAI for LLM interactions
from crewai import Crew
from .agents import AudioTranscriptionAgents
from .tasks import AudioTranscriptionTasks

class AudioTranscriptionCrew():
    def __init__(self):
        agents = AudioTranscriptionAgents()
        self.audio_capture_agent = agents.audio_capture_agent()
        self.transcriber_agent = agents.audio_transcription_agent()
        self.answer_agent = agents.answer_generation_agent()

        # Initialize LLM
        self.llm = self.initialize_llm()

    def initialize_llm(self):
        openai.api_key = os.getenv("OPENAI_API_KEY")
        return openai

    def kickoff(self, state):
        print("### Capturing, Transcribing, and Generating Responses")
        tasks = AudioTranscriptionTasks()

        # Initialize Weave (wandb) logging
        wandb.init(project="real-time-ai-question-answering")

        crew = Crew(
            agents=[self.audio_capture_agent, self.transcriber_agent, self.answer_agent],
            tasks=[
                tasks.capture_audio_task(self.audio_capture_agent),
                tasks.transcribe_audio_task(self.transcriber_agent),
                tasks.generate_answer_task(self.answer_agent, llm=self.llm)  # Passing LLM explicitly
            ],
            verbose=True
        )        # Initialize the LLM at the crew level
        self.llm = ChatOpenAI(model_name="gpt-3.5-turbo")

        result = crew.kickoff()

        # Log captured audio, transcription, and response
        wandb.log({
            "captured_audio_length": len(result['captured_audio']),
            "transcription_text": result['transcriptions'],
            "response_generated": result['responses']
        })
        
        # Return both the captured audio, transcription, and response
        return {
            **state, 
            "captured_audio": result['captured_audio'],
            "transcriptions": result['transcriptions'],
            "responses": result['responses']
        }


'''
#crew level llm
import wandb  # Import Weave (wandb) for logging
from crewai import Crew
from langchain_community.chat_models import ChatOpenAI
#from langchain.chat_models import ChatOpenAI  # Importing the OpenAI model for LLM
from .agents import AudioTranscriptionAgents
from .tasks import AudioTranscriptionTasks

class AudioTranscriptionCrew():
    def __init__(self):
        agents = AudioTranscriptionAgents()
        self.audio_capture_agent = agents.audio_capture_agent()
        self.transcriber_agent = agents.audio_transcription_agent()
        self.answer_agent = agents.answer_generation_agent()

        # Initialize Weave (wandb) for logging
        wandb.init(project="audio-transcription-crew")
        # Initialize the LLM at the crew level
        #self.llm = ChatOpenAI(model_name="gpt-3.5-turbo")

    def kickoff(self, state):
        print("### Capturing, Transcribing, and Generating Responses")
        tasks = AudioTranscriptionTasks()

        # Use a shared LLM (such as GPT-3.5 or GPT-4) for the entire crew
        crew = Crew(
            agents=[self.audio_capture_agent, self.transcriber_agent, self.answer_agent],
            tasks=[
                tasks.capture_audio_task(self.audio_capture_agent),
                tasks.transcribe_audio_task(self.transcriber_agent),
                tasks.generate_answer_task(self.answer_agent)
            ],
            verbose=True,
            # Assign the LLM for the entire crew at the crew level
            function_calling_llm=ChatOpenAI(model_name="gpt-3.5-turbo")
        )

        # Kickoff crew and start logging the task completion
        result = crew.kickoff()

        # Log relevant events from the crew execution
        wandb.log({
            "audio_captured": result['captured_audio'],
            "transcriptions": result['transcriptions'],
            "responses": result['responses']
        })
        
        # Return both the captured audio, transcription, and response
        return {
            **state, 
            "captured_audio": result['captured_audio'],
            "transcriptions": result['transcriptions'],
            "responses": result['responses']
        }
