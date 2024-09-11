import os
import pyaudio
import speech_recognition as sr
import re
from pydantic import PrivateAttr
from crewai_tools import BaseTool

class ListSoundDevicesTool(BaseTool):
    name: str = "List Sound Devices"
    description: str = "Lists all available sound devices on the machine."

    def _run(self, argument: str) -> str:
        """
        Lists all available sound devices on the machine.
        """
        p = pyaudio.PyAudio()
        devices = [p.get_device_info_by_index(i) for i in range(p.get_device_count())]
        device_list = [f"{device['name']} - {device['index']}" for device in devices]
        return "\n".join(device_list)

class SelectAndTapSoundDeviceTool(BaseTool):
    name: str = "Select and Tap Sound Device"
    description: str = "Selects a sound device and taps into its incoming sound."

    def _run(self, argument: str) -> str:
        """
        Selects a sound device and taps into its incoming sound.
        """
        p = pyaudio.PyAudio()
        device_index = int(argument)
        stream = p.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, input_device_index=device_index)
        return "Sound device selected and tapped successfully."

class RealTimeTranscriptionTool(BaseTool):
    name: str = "Real-Time Transcription"
    description: str = "Transcribes incoming sound in real-time."

    def _run(self, argument: str) -> str:
        """
        Transcribes incoming sound in real-time.
        """
        r = sr.Recognizer()
        with sr.Microphone() as source:
            audio = r.listen(source)
            try:
                transcription = r.recognize_google(audio, language="en-US")
                return transcription
            except sr.UnknownValueError:
                return "Could not understand audio"
            except sr.RequestError as e:
                return f"Error: {e}"

class FindAndAnswerQuestionsTool(BaseTool):
    name: str = "Find and Answer Questions"
    description: str = "Finds questions in the transcribed text and answers them."

    def _run(self, argument: str) -> str:
        """
        Finds questions in the transcribed text and answers them.
        """
        questions = re.findall(r'\b(what|where|when|who|why|how)\b.*?\?', argument, re.IGNORECASE)
        answers = ["Answer to the question"] * len(questions)
        return "\n".join(f"Question: {q}\nAnswer: {a}" for q, a in zip(questions, answers))

class UniversalAudioCapture(BaseTool):
    name: str = "Universal Audio Capture"
    description: str = "Captures audio from the selected sound device."

    _audio: pyaudio.PyAudio = PrivateAttr(default_factory=pyaudio.PyAudio)
    device_index: int = None

    def _run(self, argument: str) -> bytes:
        """
        Captures audio from the selected sound device.
        """
        return self.capture_audio()

    def list_audio_devices(self) -> str:
        device_list = []
        for i in range(self._audio.get_device_count()):
            device_info = self._audio.get_device_info_by_index(i)
            if device_info['maxInputChannels'] > 0:
                device_list.append(f"{i}: {device_info['name']}")
        return "\n".join(device_list)

    def select_audio_device(self, device_index: int) -> str:
        self.device_index = device_index
        return f"Selected device index: {self.device_index}"

    def capture_audio(self) -> bytes:
        if self.device_index is None:
            return b"No audio device selected. Please select an audio device first."

        stream = self._audio.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True,
                                  input_device_index=self.device_index, frames_per_buffer=1024)
        frames = []
        for i in range(0, int(44100 / 1024 * 5)):  # Capture 5 seconds of audio
            data = stream.read(1024)
            frames.append(data)

        stream.stop_stream()
        stream.close()
        return b''.join(frames)

class UniversalAudioToText(BaseTool):
    name: str = "Universal Audio to Text"
    description: str = "Transcribes the captured audio."

    _recognizer: sr.Recognizer = PrivateAttr(default_factory=sr.Recognizer)

    def _run(self, audio_data: bytes) -> str:
        """
        Transcribes the captured audio.
        """
        return self.transcribe_audio(audio_data)

    def transcribe_audio(self, audio_data: bytes) -> str:
        with sr.AudioFile(audio_data) as source:
            audio = self._recognizer.record(source)

        try:
            transcription = self._recognizer.recognize_google(audio)
            return transcription
        except sr.UnknownValueError:
            return "Could not understand audio"
        except sr.RequestError as e:
            return f"Error: {e}"
