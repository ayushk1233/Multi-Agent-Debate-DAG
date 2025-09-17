from utils.config import Config
from utils.state import DebateState, AgentType
from utils.logger import DebateLogger
from typing import Dict, List

class MemoryNode:
    def __init__(self, logger: DebateLogger):
        self.logger = logger
    
    def execute(self, state: DebateState) -> DebateState:
        """Update and manage memory for agents"""
        
        # Update structured memory based on recent arguments
        self._update_agent_memories(state)
        
        # Log memory state
        self._log_memory_state(state)
        
        # Generate memory summary for agents
        self._generate_memory_summaries(state)
        
        return state
    
    def _update_agent_memories(self, state: DebateState):
        """Update each agent's memory with relevant information"""
        
        if not state["debate_history"]:
            return
        
        # Get the most recent argument
        latest_entry = state["debate_history"][-1]
        
        # Update memories based on who spoke
        if latest_entry['agent'] == Config.AGENT_A_PERSONA:
            # Scientist's argument - add to their memory
            if len(state["agent_a_memory"]) == 0 or state["agent_a_memory"][-1] != f"Round {latest_entry['round']}: {latest_entry['argument']}":
                state["agent_a_memory"].append(f"Round {latest_entry['round']}: {latest_entry['argument']}")
        
        elif latest_entry['agent'] == Config.AGENT_B_PERSONA:
            # Philosopher's argument - add to their memory
            if len(state["agent_b_memory"]) == 0 or state["agent_b_memory"][-1] != f"Round {latest_entry['round']}: {latest_entry['argument']}":
                state["agent_b_memory"].append(f"Round {latest_entry['round']}: {latest_entry['argument']}")
    
    def _generate_memory_summaries(self, state: DebateState) -> Dict[str, str]:
        """Generate concise summaries of each agent's memory"""
        
        summaries = {
            "scientist_summary": self._summarize_memory(state["agent_a_memory"], "Scientist"),
            "philosopher_summary": self._summarize_memory(state["agent_b_memory"], "Philosopher")
        }
        
        return summaries
    
    def _summarize_memory(self, memory: List[str], agent_type: str) -> str:
        """Create a summary of an agent's memory"""
        
        if not memory:
            return f"No arguments yet from {agent_type}"
        
        if len(memory) <= 2:
            return f"{agent_type} arguments: " + "; ".join(memory)
        
        # For longer memories, create a structured summary
        recent_args = memory[-2:] if len(memory) >= 2 else memory
        summary = f"{agent_type} recent arguments: " + "; ".join(recent_args)
        
        return summary
    
    def _log_memory_state(self, state: DebateState):
        """Log current memory state"""
        
        memory_info = f"""Memory State Update:

Scientist Memory ({len(state["agent_a_memory"])} entries):
{chr(10).join(state["agent_a_memory"][-3:]) if state["agent_a_memory"] else "No entries"}

Philosopher Memory ({len(state["agent_b_memory"])} entries):
{chr(10).join(state["agent_b_memory"][-3:]) if state["agent_b_memory"] else "No entries"}

Total Debate History: {len(state["debate_history"])} entries"""
        
        self.logger.log_step("MEMORY_UPDATE", memory_info.strip())