# Architecture: Neural RAG

Este documento detalha o ciclo de vida dos dados e a arquitetura técnica do projeto Neural RAG, descrevendo cada etapa do pipeline desde a extração de dados brutos até a renderização topológica.

## Ciclo de Vida do RAG (Pipeline de Dados)

### 1. Crawler (Extração Leve)
O módulo de crawler e extração é o ponto de entrada do sistema. É responsável por varrer arquivos e fontes locais, focando predominantemente em `TypeScript` e `Markdown`.
- **Mecanismo:** Emprega expressões regulares (Regex) e heurísticas de extração leve para fragmentar o conteúdo sem a sobrecarga de parsers complexos (AST).
- **Objetivo:** Converter o código-fonte e documentos textuais em blocos (chunks) estruturados e filtrados, prontos para a etapa de análise semântica.

### 2. Ingestão Groq (LLM Processing)
Os chunks textuais brutos são enviados ao modelo hospedado no Groq para extração de informações, entidades e relações.
- **Prompting Restrito:** O LLM é induzido por prompts rigorosos que impõem restrições de formatação de IDs alfanuméricos.
- **Localização:** Exige explicitamente que todos os atributos de `labels` extraídos sejam classificados e gerados em **Português (PT-BR)**, garantindo a coesão léxica.
- **Saída:** Objetos estruturados em JSON delineando nós e ligações contextuais.

### 3. Entity Disambiguation
Como o LLM pode gerar entidades semanticamente idênticas com nomenclaturas distintas, uma etapa de normalização é obrigatória.
- **Resolução (`resolver.py`):** Realiza a fusão de sinônimos (ex: "Base de Dados", "BD", e "Banco de Dados" se tornam um só nó).
- **Consolidação:** Mescla propriedades e realinha as arestas (edges) conectadas, garantindo que o grafo resultante não tenha duplicações, assegurando alta densidade e precisão de conexão.

### 4. Persistência
A arquitetura adota um modelo de armazenamento poliglota para suportar diferentes padrões de consulta:
- **SQLite:** Banco de dados relacional que atua como a "Single Source of Truth" (SSOT) para o grafo de conhecimento (relacionamentos explícitos, nós consolidados e metadados estruturados).
- **ChromaDB:** Armazenamento vetorial nativo, encarregado de manter os embeddings dos chunks originais, viabilizando buscas semânticas eficientes por similaridade de cosseno para operações puras de RAG.

### 5. Frontend (React Flow DAG)
A camada de apresentação (UI) proporciona um ambiente interativo para a exploração do conhecimento extraído.
- **Consumo de JSON:** A interface cliente consome a estrutura consolidada em formato JSON originada do backend.
- **Renderização Topológica:** Emprega o **React Flow** para plotar um Directed Acyclic Graph (DAG) iterável. Os nós e arestas recebem layouts automáticos (frequentemente com auxílio de Dagre/ELK) para que o usuário analise o fluxo semântico, clusters de entidades e trilhas lógicas.
