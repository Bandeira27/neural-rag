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

### Seção 3: User Stories e Acceptance Criteria

**User Story: Extração de Grafo com LLM**

Como sistema de backend (Python),
Quero extrair entidades e relações de arquivos Markdown utilizando um LLM,
Para gerar um JSON estruturado de nós e arestas (grafo) que será renderizado pelo frontend.

#### Critérios de Aceite (BDD)

**Cenário 1: Caminho Feliz (JSON Perfeito)**
*   **Given** que o backend processa um arquivo Markdown da pasta `data/` enviando-o ao LLM
*   **When** o LLM retorna uma resposta contendo exclusivamente um JSON bem formatado (com chaves `nodes` e `edges`)
*   **Then** o sistema deve validar a estrutura com sucesso através do Pydantic
*   **And** salvar o payload resultante na pasta `output/` como um arquivo JSON válido.

**Cenário 2: Resiliência (LLM insere texto indesejado antes/depois do JSON)**
*   **Given** que o backend processa um arquivo Markdown da pasta `data/` enviando-o ao LLM
*   **When** o LLM retorna o JSON válido encapsulado em blocos de código markdown ou com texto introdutório (ex: "Aqui está o JSON gerado:\n```json\n...")
*   **Then** o sistema deve extrair e isolar apenas o conteúdo JSON válido, ignorando o lixo em volta
*   **And** validar a estrutura extraída com sucesso através do Pydantic
*   **And** salvar o payload resultante na pasta `output/` como um arquivo JSON válido.
