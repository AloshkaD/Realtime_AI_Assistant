import time
from .crew.tools import UniversalAudioToText, UniversalAudioCapture

class Nodes:
    def __init__(self):
        self.transcriber = UniversalAudioToText()
        self.audio_capture = UniversalAudioCapture()

    def capture_audio(self, state):
        print("# Selecting and Capturing live audio")
        devices = self.audio_capture.list_audio_devices()
        print("Available audio devices:")
        print(devices)
        device_index = int(input("Enter the index of the device you want to use: "))
        self.audio_capture.select_audio_device(device_index)
        audio_data = self.audio_capture._run("")  # Use _run method to capture audio
        print(f"### Captured Audio: {len(audio_data)} bytes")
        return {**state, "captured_audio": audio_data}

    def transcribe_audio(self, state):
        print("# Transcribing live audio")
        transcription = self.transcriber._run(state['captured_audio'])  # Use _run method to transcribe
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