# Epic 01: MVP - Neural RAG

## Architectural Planning & Scaffolding

This document outlines the exact scaffolding and architectural plan for the Neural RAG MVP. The project is strictly separated into a Python backend for data processing and a React/Vite frontend for visualization.

### EXATO Scaffolding

```text
neural-rag/
├── backend/
│   ├── requirements.txt      # Python dependencies
│   ├── main.py               # Main LLM/Prompt script for processing
│   ├── data/                 # Input Markdown files
│   └── output/               # Output JSON graph files (nodes/edges)
├── frontend/
│   ├── package.json          # Node dependencies
│   ├── vite.config.js        # Vite config
│   ├── index.html            # Web entry point
│   ├── src/
│   │   ├── main.jsx          # React bootstrap
│   │   ├── App.jsx           # Main application component
│   │   └── components/
│   │       └── NeuralGraph.jsx # Neural physics renderer component
│   └── public/
├── .hermes/
│   └── plans/
│       └── epic-01-mvp.md    # This planning document (Architecture)
└── README.md
```

### Key Dependencies

*   **Backend (Python):**
    *   LLM/Prompt Script: Custom Python script responsible for reading Markdown documents and generating a structured JSON representing the graph (nodes and edges) using a local AI or API.
    *   Libraries: `openai` (or equivalent AI SDK), `pydantic` (for JSON structure validation).

*   **Frontend (React/Vite):**
    *   Renderer: `react-force-graph` (Crucial for rendering the physics of the neurons/graph).
    *   Core: `react`, `react-dom`.
    *   Bundler: `vite`.
