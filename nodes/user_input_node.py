from utils.state import DebateState, AgentType
from utils.logger import DebateLogger

class UserInputNode:
    def __init__(self, logger: DebateLogger):
        self.logger = logger
    
    def execute(self, state: DebateState) -> DebateState:
        """Get debate topic from user input"""
        print("\n=== MULTI-AGENT DEBATE SYSTEM ===")
        print("Two AI agents will debate on your chosen topic.")
        print("Agent A: Scientist | Agent B: Philosopher")
        print("8 rounds total (4 arguments per agent)\n")
        
        # Get topic from user
        while not state["topic"]:
            topic = input("Enter topic for debate: ").strip()
            if topic:
                state["topic"] = topic
            else:
                print("Please enter a valid topic.")
        
        # Initialize debate state
        state["current_round"] = 1
        state["current_agent"] = AgentType.SCIENTIST  # Scientist goes first
        
        # Log the initialization
        self.logger.log_step("USER_INPUT", f"Debate Topic: {state['topic']}")
        self.logger.log_step("INITIALIZATION", 
                           f"Starting debate between {AgentType.SCIENTIST.value} and {AgentType.PHILOSOPHER.value}")
        
        print(f"\nStarting debate on: '{state['topic']}'")
        print(f"Round 1 - {state['current_agent'].value} will go first...\n")
        
        return state