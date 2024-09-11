from dotenv import load_dotenv
load_dotenv()

from langgraph.graph import StateGraph
from .state import RealTimeAudioState  # Correct import here
from .nodes import Nodes
from .crew.crew import AudioTranscriptionCrew

class WorkFlow():
    def __init__(self):
        nodes = Nodes()
        workflow = StateGraph(RealTimeAudioState)  # Use RealTimeAudioState

        workflow.add_node("capture_audio", nodes.capture_audio)
        workflow.add_node("transcribe_audio", nodes.transcribe_audio)
        workflow.add_node("wait_next_run", nodes.wait_next_run)
        workflow.add_node("generate_responses", AudioTranscriptionCrew().kickoff)
        workflow.add_node("display_response", nodes.display_response)

        workflow.set_entry_point("capture_audio")
        workflow.add_conditional_edges(
            "transcribe_audio",
            nodes.new_question,
            {
                "continue": 'generate_responses',
                "end": 'wait_next_run'
            }
        )
        workflow.add_edge('generate_responses', 'display_response')
        workflow.add_edge('display_response', 'wait_next_run')
        workflow.add_edge('wait_next_run', 'capture_audio')
        self.app = workflow.compile()
