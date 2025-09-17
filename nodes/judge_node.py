from groq import Groq
from utils.state import DebateState
from utils.config import Config
from utils.logger import DebateLogger
from typing import Dict

class JudgeNode:
    def __init__(self, logger: DebateLogger):
        self.logger = logger
        self.client = Groq(api_key=Config.GROQ_API_KEY)
    
    def execute(self, state: DebateState) -> DebateState:
        """Execute judge evaluation of the debate"""
        
        if not state["is_complete"]:
            return state  # Only judge completed debates
        
        print("=== JUDGE EVALUATION ===")
        print("Analyzing debate arguments...")
        
        # Generate debate summary
        summary = self._generate_debate_summary(state)
        
        # Determine winner and justification
        judgment_result = self._evaluate_winner(state)
        
        # Update state with results
        state["judgment"] = summary
        # Determine winner and justification
        judgment_result = self._evaluate_winner(state)
        
        # Update state with results
        state["judgment"] = summary
        state["winner"] = judgment_result['winner']  # Using dictionary access
        
        # Create a combined judgment string for logging
        full_judgment = f"{summary}\n\nWinner: {judgment_result['winner']}\nReason: {judgment_result['reasoning']}"
        
        # Log results
        self.logger.log_step("JUDGE_SUMMARY", summary)
        self.logger.log_step("JUDGE_WINNER", f"Winner: {judgment_result['winner']}")
        self.logger.log_step("JUDGE_REASONING", judgment_result['reasoning'])
        
        # Print results to console
        print(f"\n[Judge] Summary of debate:")
        print(summary)
        print(f"\n[Judge] Winner: {judgment_result['winner']}")
        print(f"Reason: {judgment_result['reasoning']}")
        print("\n" + "="*50)
        
        return state
    
    def _generate_debate_summary(self, state: DebateState) -> str:
        """Generate comprehensive summary of the debate"""
        
        # Build debate transcript
        transcript = f"Debate Topic: {state['topic']}\n\n"
        transcript += "Arguments presented:\n"
        
        for i, entry in enumerate(state["debate_history"], 1):
            transcript += f"{i}. {entry['agent']}: {entry['argument']}\n"
        
        # Create summary prompt
        prompt = f"""Please provide a concise summary of this debate in 3-4 sentences:

{transcript}

Focus on:
- Main arguments from each side
- Key points of contention
- Overall debate quality

Summary:"""

        try:
            response = self.client.chat.completions.create(
                model=Config.GROQ_MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.5,
                max_tokens=200
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            self.logger.log_step("ERROR_SUMMARY", f"Failed to generate summary: {str(e)}")
            return f"Summary generation failed: {str(e)}"
        
    def _evaluate_winner(self, state: DebateState) -> Dict[str, str]:
        """Evaluate debate and determine winner with reasoning"""
        
        # Build evaluation prompt
        transcript = f"Debate Topic: {state['topic']}\n\n"
        
        # Separate arguments by agent
        scientist_args = []
        philosopher_args = []
        
        for entry in state["debate_history"]:
            if entry['agent'] == Config.AGENT_A_PERSONA:
                scientist_args.append(f"Round {entry['round']}: {entry['argument']}")
            else:
                philosopher_args.append(f"Round {entry['round']}: {entry['argument']}")
        
        transcript += f"SCIENTIST ARGUMENTS:\n"
        for arg in scientist_args:
            transcript += f"- {arg}\n"
        
        transcript += f"\nPHILOSOPHER ARGUMENTS:\n"
        for arg in philosopher_args:
            transcript += f"- {arg}\n"
        
        # Create evaluation prompt
        prompt = f"""You are an impartial debate judge. Evaluate this debate and determine the winner.

{transcript}

Evaluation Criteria:
1. Logical consistency and reasoning
2. Evidence quality and relevance  
3. Argument strength and persuasiveness
4. Response to opposing points
5. Overall coherence of position

Provide your decision in this exact format:
WINNER: [Scientist/Philosopher]
REASONING: [2-3 sentences explaining your decision]

Your evaluation:"""

        try:
            response = self.client.chat.completions.create(
                model=Config.GROQ_MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,  # Lower temperature for more consistent judging
                max_tokens=250
            )
            
            evaluation = response.choices[0].message.content.strip()
            
            # Parse the response
            lines = evaluation.split('\n')
            winner = "Tie"
            reasoning = "Unable to determine winner"
            
            for line in lines:
                if line.startswith("WINNER:"):
                    winner = line.split(":", 1)[1].strip()
                elif line.startswith("REASONING:"):
                    reasoning = line.split(":", 1)[1].strip()
            
            return {
                "winner": winner,
                "reasoning": reasoning
            }
            
        except Exception as e:
            self.logger.log_step("ERROR_EVALUATION", f"Failed to evaluate winner: {str(e)}")
            return {
                "winner": "Error",
                "reasoning": f"Evaluation failed: {str(e)}"
            }