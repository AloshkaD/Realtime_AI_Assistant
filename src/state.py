import datetime
from typing import TypedDict

class RealTimeAudioState(TypedDict):
    transcribed_text: str  # Captured audio converted to text
    question_queue: list[str]  # Queue of questions from the transcription
    response_queue: list[str]  # Queue of AI-generated responses
    current_question: str  # Current question being processed
    current_response: str  # Current response being generated
    last_transcribed: datetime.datetime  # Timestamp of the last transcription
    last_response: datetime.datetime  # Timestamp of the last generated response
