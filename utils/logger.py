import os
from datetime import datetime
from typing import Dict, Any

class DebateLogger:
    def __init__(self, log_file: str = "debate_log.txt"):
        self.log_file = log_file
        self._initialize_log()
    
    def _initialize_log(self):
        with open(self.log_file, 'w') as f:
            f.write(f"=== MULTI-AGENT DEBATE LOG ===\n")
            f.write(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 50 + "\n\n")
    
    def log_step(self, step_name: str, content: str):
        with open(self.log_file, 'a') as f:
            f.write(f"[{step_name}] {datetime.now().strftime('%H:%M:%S')}\n")
            f.write(f"{content}\n")
            f.write("-" * 30 + "\n\n")