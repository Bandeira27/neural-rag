# Plan: Hotfix 08 - Massive Ingestion and Entity Resolution

## 1. Objective
Implement massive ingestion of source code and resolve entity duplication (Entity Disambiguation) to ensure a high-quality Knowledge Graph.

## 2. Context & Bug Report
*   **Bug "Ilhas Duplicadas":** Atualmente, o sistema cria nós de entidades duplicadas ou desconectadas para a mesma entidade conceitual (ex: "Porteiro QA" vs "Equipe QA"). Isso fragmenta o grafo e cria "ilhas" de informações desconectadas.
*   **Source Code Parsing:** Há uma necessidade crítica de parsear o código-fonte real do repositório para extrair entidades arquiteturais e relacionamentos precisos.

## 3. Approach
Enhance the crawler to handle source code extensions and reimplement the resolver to perform robust entity disambiguation before graph insertion.

## 4. Dev Checklist
- [ ] 1) O `crawler.py` DEVE ler arquivos `.tsx`, `.ts` e `package.json` do Night Watch.
- [ ] 2) Para evitar estouro de tokens de código na API Groq, o crawler DEVE fazer um 'chunking' inteligente ou enviar uma versão estritamente resumida.
- [ ] 3) O `resolver.py` DEVE ser reimplementado: antes de salvar no SQLite, ele deve identificar sinônimos textuais (Entity Disambiguation) de forma robusta e FUNDIR os nós (e seus links).
