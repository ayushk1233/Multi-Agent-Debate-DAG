import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    GROQ_MODEL = os.getenv("GROQ_MODEL", "llama3-8b-8192")
    MAX_ROUNDS = int(os.getenv("MAX_ROUNDS", 8))
    AGENT_A_PERSONA = os.getenv("AGENT_A_PERSONA", "Scientist")
    AGENT_B_PERSONA = os.getenv("AGENT_B_PERSONA", "Philosopher")