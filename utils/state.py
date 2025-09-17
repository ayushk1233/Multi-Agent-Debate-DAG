from typing import Dict, List, Optional, TypedDict
from enum import Enum

class AgentType(Enum):
    SCIENTIST = "Scientist"
    PHILOSOPHER = "Philosopher"

class DebateState(TypedDict):
    topic: str
    current_round: int
    current_agent: Optional[AgentType]
    debate_history: List[Dict[str, str]]
    agent_a_memory: List[str]
    agent_b_memory: List[str]
    is_complete: bool
    winner: Optional[str]
    judgment: str

def create_initial_state() -> DebateState:
    return {
        "topic": "",
        "current_round": 0,
        "current_agent": None,
        "debate_history": [],
        "agent_a_memory": [],
        "agent_b_memory": [],
        "is_complete": False,
        "winner": None,
        "judgment": ""
    }