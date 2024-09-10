from crewai import Crew
from .agents import AudioTranscriptionAgents
from .tasks import AudioTranscriptionTasks

class AudioTranscriptionCrew():
    def __init__(self):
        agents = AudioTranscriptionAgents()
        self.audio_capture_agent = agents.audio_capture_agent()
        self.transcriber_agent = agents.audio_transcription_agent()
        self.answer_agent = agents.answer_generation_agent()

    def kickoff(self, state):
        print("### Capturing, Transcribing, and Generating Responses")
        tasks = AudioTranscriptionTasks()
        crew = Crew(
            agents=[self.audio_capture_agent, self.transcriber_agent, self.answer_agent],
            tasks=[
                tasks.capture_audio_task(self.audio_capture_agent),
                tasks.transcribe_audio_task(self.transcriber_agent),
                tasks.generate_answer_task(self.answer_agent)
            ],
            verbose=True
        )
        result = crew.kickoff()
        
        # Return both the captured audio, transcription, and response
        return {
            **state, 
            "captured_audio": result['captured_audio'],
            "transcriptions": result['transcriptions'],
            "responses": result['responses']
        }
