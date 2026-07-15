# Plan: Hotfix 08 - Massive Ingestion and Entity Resolution

## 1. Objective
Implement massive ingestion of source code and resolve entity duplication (Entity Disambiguation) to ensure a high-quality Knowledge Graph.

## 2. Context & Bug Report
*   **Bug "Ilhas Duplicadas":** Atualmente, o sistema cria nós de entidades duplicadas ou desconectadas para a mesma entidade conceitual (ex: "Porteiro QA" vs "Equipe QA"). Isso fragmenta o grafo e cria "ilhas" de informações desconectadas.
*   **Source Code Parsing:** Há uma necessidade crítica de parsear o código-fonte real do repositório para extrair entidades arquiteturais e relacionamentos precisos.

## 3. BDD (Behavior-Driven Development) Scenarios
1) Cenário (Backend/Resolver): Dado que o parser gera 'Equipe QA' e 'QA Team', Quando passados para o resolver, Então ele DEVE fundir as duas entidades em um único nó centralizando os links.
2) Cenário (Backend/Crawler): Dado que um arquivo tem mais de X tokens (código grande), Quando ele for enviado, Então o crawler deve cortá-lo e enviar apenas importações e assinaturas para o Groq.


## 4. Dev Checklist
- [ ] 1) O `crawler.py` DEVE ler arquivos `.tsx`, `.ts` e `package.json` do Night Watch.
- [ ] 2) Para evitar estouro de tokens de código na API Groq, o crawler DEVE fazer um 'chunking' inteligente ou enviar uma versão estritamente resumida.
- [ ] 3) O `resolver.py` DEVE ser reimplementado: antes de salvar no SQLite, ele deve identificar sinônimos textuais (Entity Disambiguation) de forma robusta e FUNDIR os nós (e seus links).
