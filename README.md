# Multi-Agent Debate DAG using LangGraph

##VIDEO WALKTHROUGH LINK :
https://www.loom.com/share/8339ae87b87a430ea58ff6a44b60f417?sid=a6fa1214-33bd-4fe2-979a-2121f6a97d3b

A sophisticated debate system built with LangGraph that enables AI agents to engage in structured debates while maintaining context and memory.

## Overview

This system orchestrates debates between two AI agents with distinct personas (by default, a Scientist and a Philosopher) on user-provided topics. The debate follows a directed acyclic graph (DAG) structure, with each node handling specific aspects of the debate flow:

- Two debating agents present alternating arguments
- Memory preservation ensures coherent discussion
- An impartial judge evaluates and declares a winner

The agent personas are configurable via environment variables, allowing for diverse debate perspectives (e.g., Lawyer vs Economist, Artist vs Critic, etc.).

## Features

- **CLI-based Debate System**: Structured 8-round debates with alternating arguments
- **Memory Management**: Structured storage and recall of previous arguments
- **Intelligent Judging**: Comprehensive debate summary and winner determination
- **Detailed Logging**: All transitions and verdicts saved to `debate_log.txt`
- **Visual DAG Representation**: Auto-generated Mermaid diagram (`debate_dag_diagram.md`)
- **Modular Architecture**: Clean separation of concerns with nodes and utilities

## Folder Structure

```plaintext
debate_dag/
├── nodes/
│   ├── agent_a_node.py
│   ├── agent_b_node.py
│   ├── debate_controller.py
│   ├── judge_node.py
│   ├── memory_node.py
│   └── user_input_node.py
├── utils/
│   ├── config.py
│   ├── logger.py
│   └── state.py
├── scripts/
│   ├── check_models.py
│   ├── generate_dag.py
│   └── test_setup.py
├── logs/
│   ├── debate_log.txt
│   ├── dag_generation.log
│   └── debate_dag_diagram.md
├── main.py
├── requirements.txt
├── .env.example
└── README.md
```

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/debate_dag.git
cd debate_dag
```

1. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

1. Install dependencies:

```bash
pip install -r requirements.txt
```

1. Create a `.env` file with your configurations:

```env
GROQ_API_KEY=your_api_key_here
GROQ_MODEL=llama-3.3-70b-versatile
MAX_ROUNDS=8
AGENT_A_PERSONA=Scientist
AGENT_B_PERSONA=Philosopher
```

## Usage

### Running a Debate

Start a new debate:

```bash
python main.py
```

### Generating the DAG Diagram

Create a visual representation of the debate flow:

```bash
python scripts/generate_dag.py
```

### Viewing Outputs

- **Debate Log**: Open `logs/debate_log.txt` to view the complete debate history
- **DAG Diagram**: Open `logs/debate_dag_diagram.md` in VS Code with Mermaid support or on GitHub

### Customizing the Debate

#### Changing Topics

Run `python main.py` and enter your desired topic when prompted.

#### Modifying Personas

Edit `.env` file to change agent personas:

```env
AGENT_A_PERSONA=Lawyer
AGENT_B_PERSONA=Economist
```

#### Adjusting Rounds

Update `MAX_ROUNDS` in `.env` to change debate length.

### Utility Scripts

- **check_models.py**: Lists available Groq models for potential swapping
- **test_setup.py**: Verifies environment configuration and API connectivity

### Logging and Output

- All debate interactions are logged to `debate_log.txt`
- Final judgment and debate summary appear at the end of each session
- DAG visualization available in `debate_dag_diagram.md`

### DAG Diagram Visualization

The system generates a Mermaid-compatible diagram showing the debate flow:

- View using VS Code's "Markdown Preview Mermaid Support" extension
- Renders automatically on GitHub
- Shows node relationships and data flow

## Contributing / Customization

The system is designed for easy extension:

1. **Adding New Agents**: Create new node files in `nodes/` directory
2. **Modifying Rules**: Update validation logic in `debate_controller.py`
3. **Extending Memory**: Enhance memory structures in `memory_node.py`

## License

MIT License - Feel free to use and modify as needed.
