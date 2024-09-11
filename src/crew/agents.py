'''from crewai import Agent
from textwrap import dedent
from .tools import UniversalAudioToText, UniversalAudioCapture
import wandb  # Import wandb for logging
class AudioTranscriptionAgents():
    def __init__(self):
        self.audio_tool = UniversalAudioToText()
        self.audio_capture_tool = UniversalAudioCapture()

    def audio_capture_agent(self):
        return Agent(
            role='Audio Capture Specialist',
            goal='Capture live audio and send it for transcription.',
            backstory=dedent("""\
                You are an expert in capturing real-time audio input, ensuring that all incoming audio is 
                processed in a timely manner for further transcription and response.
            """),
            tools=[self.audio_capture_tool.capture_audio],
            verbose=True,
            allow_delegation=False
        )
 
    def audio_transcription_agent(self):
        return Agent(
            role='Audio Transcriber',
            goal='Transcribe live audio input in real-time and convert it into text.',
            backstory=dedent("""\
                You are a highly skilled Audio Transcriber specializing in converting real-time audio into text
                with accuracy and efficiency.
            """),
            tools=[self.audio_tool.transcribe_audio],
            verbose=True,
            allow_delegation=False
        )

    def answer_generation_agent(self):
        return Agent(
            role='Question Answering Specialist',
            goal='Generate accurate and concise responses to the transcribed questions.',
            backstory=dedent("""\
                You are a highly skilled Question Answering Specialist. Your job is to provide clear, concise, 
                and helpful answers based on the transcribed text input.
            """),
            verbose=True,
            allow_delegation=False
        )
'''
from crewai import Agent
from textwrap import dedent
from .tools import UniversalAudioToText, UniversalAudioCapture

class AudioTranscriptionAgents():
    def __init__(self):
        self.audio_tool = UniversalAudioToText()
        self.audio_capture_tool = UniversalAudioCapture()

    def audio_capture_agent(self):
        # Fix: Ensure tools are passed as a list
        return Agent(
            role='Audio Capture Specialist',
            goal='Capture live audio and send it for transcription.',
            backstory=dedent("""\
                You are an expert in capturing real-time audio input, ensuring that all incoming audio is 
                processed in a timely manner for further transcription and response.
            """),
            tools=[{'name': 'audio_capture_tool', 'tool': self.audio_capture_tool.capture_audio}],
            verbose=True,
            allow_delegation=False
        )

    def audio_transcription_agent(self):
        # Fix: Ensure tools are passed as a list
        return Agent(
            role='Audio Transcriber',
            goal='Transcribe live audio input in real-time and convert it into text.',
            backstory=dedent("""\
                You are a highly skilled Audio Transcriber specializing in converting real-time audio into text
                with accuracy and efficiency.
            """),
            tools=[{'name': 'audio_transcription_tool', 'tool': self.audio_tool.transcribe_audio}],
            verbose=True,
            allow_delegation=False
        )

    def answer_generation_agent(self):
        # No tools required for answer generation agent in this case
        return Agent(
            role='Question Answering Specialist',
            goal='Generate accurate and concise responses to the transcribed questions.',
            backstory=dedent("""\
                You are a highly skilled Question Answering Specialist. Your job is to provide clear, concise, 
                and helpful answers based on the transcribed text input.
            """),
            tools=[],  # No tools here, but you can add if necessary
            verbose=True,
            allow_delegation=False
        )
