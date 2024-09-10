import pyaudio
import speech_recognition as sr
from langchain.tools import tool

class UniversalAudioCapture:
    def __init__(self):
        self.audio = pyaudio.PyAudio()

    def capture_audio(self):
        # Open audio stream (for simplicity, capturing a short buffer)
        stream = self.audio.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)
        frames = []

        print("### Capturing audio...")

        for i in range(0, int(44100 / 1024 * 5)):  # Capture 5 seconds of audio
            data = stream.read(1024)
            frames.append(data)

        stream.stop_stream()
        stream.close()
        return frames  # You can store or process the raw audio here

class UniversalAudioToText:
    def __init__(self):
        self.recognizer = sr.Recognizer()

    def transcribe_audio(self, audio_data):
        # Convert raw audio data to recognizer's format for transcription
        print("### Transcribing audio...")
        with sr.AudioFile(audio_data) as source:
            audio = self.recognizer.record(source)

        try:
            transcription = self.recognizer.recognize_google(audio)
            print(f"### Transcription result: {transcription}")
            return transcription
        except sr.UnknownValueError:
            return "Could not understand audio"
        except sr.RequestError:
            return "Could not request results"
