from crewai import Task
from textwrap import dedent

class AudioTranscriptionTasks:
    def capture_audio_task(self, agent):
        return Task(
            description=dedent(f"""\
                Capture the live audio input for transcription.
                Use your skills to capture the audio stream and make it available for transcription.
            """),
            agent=agent,
            output_key="captured_audio"
        )

    def transcribe_audio_task(self, agent):
        return Task(
            description=dedent(f"""\
                Transcribe the captured audio into text.
                Use your expertise to capture spoken words and convert them into readable text accurately.
            """),
            agent=agent,
            output_key="transcriptions"
        )

    def generate_answer_task(self, agent):
        return Task(
            description=dedent(f"""\
                Generate accurate and concise answers based on the transcribed audio.
                You must understand the context and questions posed during the meeting and provide clear responses.
            """),
            agent=agent,
            output_key="responses"
        )
