from utils.state import DebateState, AgentType
from utils.config import Config
from utils.logger import DebateLogger

class DebateController:
    def __init__(self, logger: DebateLogger):
        self.logger = logger
    
    def execute(self, state: DebateState) -> DebateState:
        """Control debate flow and turn management"""
        
        # Check if we've reached max rounds - complete the debate
        if len(state["debate_history"]) >= Config.MAX_ROUNDS:
            state["is_complete"] = True
            self.logger.log_step("DEBATE_COMPLETE", 
                               f"Debate completed after {len(state['debate_history'])} arguments")
            print("=== DEBATE COMPLETED ===\n")
            return state
        
        # For the very first call, don't switch - let scientist go first
        if len(state["debate_history"]) == 0:
            return state
            
        # Switch turns after each argument
        if state["current_agent"] == AgentType.SCIENTIST:
            state["current_agent"] = AgentType.PHILOSOPHER
        elif state["current_agent"] == AgentType.PHILOSOPHER:
            state["current_agent"] = AgentType.SCIENTIST
        
        # Update round number based on completed arguments
        state["current_round"] = (len(state["debate_history"]) // 2) + 1
        
        # Log current state
        self.logger.log_step("CONTROLLER", 
                           f"Arguments so far: {len(state['debate_history'])}, Current agent: {state['current_agent'].value}")
        
        return state
    
    def _check_repetition(self, state: DebateState) -> bool:
        """Basic check for argument repetition"""
        if len(state["debate_history"]) < 2:
            return False
        
        # Get last two arguments
        recent_args = [entry['argument'].lower() for entry in state["debate_history"][-2:]]
        
        # Simple repetition check (can be enhanced)
        for i, arg1 in enumerate(recent_args):
            for j, arg2 in enumerate(recent_args[i+1:], i+1):
                # Check if arguments are too similar (basic word overlap)
                words1 = set(arg1.split())
                words2 = set(arg2.split())
                overlap = len(words1.intersection(words2))
                if overlap > len(words1) * 0.7:  # 70% word overlap threshold
                    return True
        
        return False