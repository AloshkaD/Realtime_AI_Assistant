import time
from .tools import UniversalAudioToText, UniversalAudioCapture

class Nodes():
    def __init__(self):
        self.transcriber = UniversalAudioToText()
        self.audio_capture = UniversalAudioCapture()

    def capture_audio(self, state):
        print("# Capturing live audio")
        audio_data = self.audio_capture.capture_audio()
        print(f"### Captured Audio: {audio_data}")
        return {**state, "captured_audio": audio_data}

    def transcribe_audio(self, state):
        print("# Transcribing live audio")
        transcription = self.transcriber.transcribe_audio(state['captured_audio'])
        print(f"### Transcription: {transcription}")
        return {**state, "transcription": transcription}

    def wait_next_run(self, state):
        print("## Waiting for 30 seconds")
        time.sleep(30)
        return state

    def display_response(self, state):
        if 'responses' in state and len(state['responses']) > 0:
            print(f"## Response: {state['responses']}")
        else:
            print("## No response generated.")
        return state

    def new_question(self, state):
        if 'transcription' not in state or len(state['transcription']) == 0:
            print("## No new transcriptions")
            return "end"
        else:
            print("## New transcription detected")
            return "continue"
