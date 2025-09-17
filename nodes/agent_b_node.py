from groq import Groq
from utils.state import DebateState, AgentType
from utils.config import Config
from utils.logger import DebateLogger

class AgentBNode:
    def __init__(self, logger: DebateLogger):
        self.logger = logger
        self.client = Groq(api_key=Config.GROQ_API_KEY)
        self.persona = Config.AGENT_B_PERSONA
        
    def execute(self, state: DebateState) -> DebateState:
        """Execute Philosopher agent turn"""
        # Check if it's this agent's turn
        if state["current_agent"] != AgentType.PHILOSOPHER:
            return state  # Not this agent's turn
            
        # Check if debate is complete
        if state["current_round"] > Config.MAX_ROUNDS or state["is_complete"]:
            return state
            
        # Generate argument
        argument = self._generate_argument(state)
        
        # Add to debate history
        debate_entry = {
            "round": state["current_round"],
            "agent": self.persona,
            "argument": argument
        }
        state["debate_history"].append(debate_entry)
        
        # Add to agent's own memory
        state["agent_b_memory"].append(f"Round {state['current_round']}: {argument}")
        
        # Log the argument
        self.logger.log_step(f"ROUND_{state['current_round']}_PHILOSOPHER", argument)
        
        # Print to console
        print(f"[Round {state['current_round']}] {self.persona}: {argument}\n")
        
        return state
    
    def _generate_argument(self, state: DebateState) -> str:
        """Generate philosophical argument using Groq"""
        
        # Build context from previous arguments
        context = ""
        if state["debate_history"]:
            context = "Previous arguments in this debate:\n"
            for entry in state["debate_history"][-3:]:  # Last 3 arguments for context
                context += f"- {entry['agent']}: {entry['argument']}\n"
            context += "\n"
        
        # Create prompt for philosopher persona
        prompt = f"""You are a {self.persona} participating in a formal debate.
Topic: {state["topic"]}

{context}Your role: Present philosophical and ethical arguments.
- Consider ethical implications and human values
- Question assumptions and underlying principles
- Use philosophical frameworks and reasoning
- Keep response to 2-3 sentences maximum
- Be respectful but firm in your philosophical position

Your argument (Round {state["current_round"]}/8):"""

        try:
            response = self.client.chat.completions.create(
                model=Config.GROQ_MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=150
            )
            
            argument = response.choices[0].message.content.strip()
            return argument
            
        except Exception as e:
            self.logger.log_step("ERROR_PHILOSOPHER", f"Failed to generate argument: {str(e)}")
            return f"[Error generating philosophical argument: {str(e)}]"