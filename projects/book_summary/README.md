# Multi-Agent Book Summarizer
A LangGraph-powered application that transforms PDF books into structured 
synopses through a coordinated pipeline of specialized AI agents.

## Architecture
This project implements a multi-agent workflow where each agent has a 
distinct role, orchestrated by LangGraph's state machine:

- **Planner**: Analyzes full book text to generate a hierarchical outline
- **Researcher**: Extracts key definitions, arguments, and quotes per section
- **Writer**: Synthesizes research into a coherent first draft
- **Critic**: Reviews drafts against source material for gaps and weaknesses
- **Revision Loop**: Conditional edge routes back to Writer when critique exists

Unlike single-prompt summarization, this architecture separates concerns 
across specialized roles, producing more faithful and structurally sound outputs.

## Tech Stack
| Component | Technology | Purpose |
|---|---|---|
| Orchestration | LangGraph | Stateful multi-agent workflow |
| LLM Integration | LangChain | Model abstraction, message handling |
| Models | GPT-6 Luna / GPT-6.1 Terra | Configurable cost-quality tradeoff |
| UI | Streamlit | Real-time streaming progress display |
| Document Loading | PyPDFLoader | PDF ingestion |

## Setup & Run

### Prerequisites
- Python 3.10+
- An OpenAI API key

### Installation

1. Clone the repository
   ```bash
   git clone https://github.com/Palaiologan/AI_sandbox.git
   cd projects/book_summary

2. Create and activate a virtual environment
    ```bash
    python -m venv venv
    # Windows:
    venv\Scripts\activate
    # Mac/Linux:
    source venv/bin/activate

3. Install dependencies
    ```bash
    pip install -r requirements.txt

4. Set your API key
    ```bash
    # Windows:
    set OPENAI_API_KEY=your-key-here
    # Mac/Linux:
    export OPENAI_API_KEY=your-key-here

### Running the book-summary app
```bash
streamlit run launcher_simple.py
```
This will open a localhost in your browser, where you can upload a PDF, select a model and generate the answer.

## Design Decisions
- No vector database: For fixed-document analysis, sequential reading preserves narrative structure better than semantic retrieval
- Environment-based model config: Allows runtime model switching without modifying graph code
- Conditional revision loop: Bounded by revision_count to prevent infinite loops while allowing quality iteration

## Project Structure

```text
book-summarizer/
├── README.me             # this current README Markdown file
├── launcher_simple.py    # Streamlit UI
├── graph_logic.py        # LangGraph nodes, edges, state
├── book_prompts.py       # Agent system prompts and templates
└── requirements.txt      # modules required to successfully launch
```

### Licence
Alejandro Hernandez