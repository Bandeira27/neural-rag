# Plano de Ação: Hotfix 05 - Code Crawler e UX (Node Tooltips)

Este documento define as etapas para a extração de código e captura de descrições dos nós no Neural RAG.

## 1. Expansão do Crawler (`src/crawler.py`)
- O crawler deve ser expandido para aceitar e processar as seguintes extensões/arquivos:
  - `.tsx`
  - `.ts`
  - `package.json`

## 2. Ajuste do Payload no Backend (`main.py`)
- O payload de requisição e parsing de resposta no `main.py` precisa ser atualizado.
- O JSON de resposta da Groq **DEVE** conter um novo campo `description` (em português - `pt-br`) para cada nó.
- Esta `description` deve explicar de forma concisa o componente, sua finalidade ou a regra de negócio aplicada.

## 3. Implementação no Frontend
- Implementar o evento `onNodeClick` no grafo de nós.
- Ao clicar em um nó, exibir o conteúdo do campo `description` em um painel estilizado (tooltip ou side-panel) para melhorar a experiência do usuário.

## 4. Quality Assurance (QA)
- O QA avaliará a sanidade estrutural e semântica do parsing de código executado pelo crawler.
- Garantir que a integração ponta a ponta (Crawler -> LLM/Groq -> Frontend) esteja exibindo as descrições em pt-br corretamente.
