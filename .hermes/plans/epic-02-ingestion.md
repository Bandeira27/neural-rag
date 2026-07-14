# Hermes Plan Mode - Epic 02: Ingestion Pipeline

## 1. Meta
- [ ] **ID:** epic-02-ingestion
- [ ] **Autor:** Tech Lead / Auditor
- [ ] **Data:** 2026-07-14

## 2. Contexto/Auditoria
- [ ] Definir contexto e propósito da alteração: Pipeline de ingestão, crawling de repositórios, resolução de entidades e persistência.
- [ ] Estrutura de Pastas e Nomenclatura definidas: `src/crawler`, `src/ingestion`, `src/persistence`.
- [ ] Auditoria concluída e impactos no sistema mapeados.
- [ ] **Arquitetura Técnica Estabelecida:**
  - **1. Crawler Parametrizado:** O crawler de repositório deve obrigatoriamente extrair o caminho alvo via argumentos de CLI (CLI args) ou variáveis de ambiente (`.env`). NUNCA deixar o diretório alvo (ex: 'night-watch') hardcoded.
  - **2. Resolução de Entidades (Entity Resolution):** Lógica robusta para merging de nós (nodes) similares. Identificação de entidades redundantes ou sinônimas (ex: arquivos duplicados, conceitos de negócio repetidos) consolidando suas arestas e metadados.
  - **3. Persistência de Dados:** Configuração dual de armazenamento usando ChromaDB para embeddings de RAG, e SQLite para estado relacional e armazenamento persistente de metadados das entidades e progresso do crawler.

## 3. User Stories e Critérios de Aceite (BDD)
- [ ] Cenários BDD (Given / When / Then) escritos:
  - *Given* um caminho de repositório parametrizado via `.env` *When* o crawler inicia *Then* ele processa o repositório correto dinamicamente.
  - *Given* duas entidades conceitualmente idênticas extraídas *When* a resolução de entidades roda *Then* as entidades sofrem merge em um único nó.
- [ ] Critérios de aceite definidos e alinhados.

## 4. Dev Checklist
- [ ] **Obrigatório:** Testes unitários (TDD) e E2E (Playwright) escritos *antes* do código de produção.
- [ ] Implementação do código-fonte atende a todos os testes.
- [ ] Revisão de código e lint concluídos.

## 5. Tech Lead / Code Review Checklist
- [ ] Clean Code.
- [ ] Princípios SOLID.
- [ ] Respeito à arquitetura.

## 6. QA/Gatekeeper Checklist
- [ ] **Testes de OOM (Out of Memory):** Profiling de memória executado e sem memory leaks (Baseline: testar carga com 10.000 registros/nós).
- [ ] **Rastreabilidade E2E:** 1:1 entre cenários BDD e testes Playwright.
- [ ] **Segurança e A11y:** Verificações anti-XSS/CVE scanning executadas e validação de acessibilidade (teclado/ARIA).
- [ ] **Análise de Binários:** Verificação de tamanho, dependências e integridade de compilação.
- [ ] **UI/UX:** Validação visual focada nos componentes Shadcn, acessibilidade e responsividade.
- [ ] **Documentação e Memória:** A documentação gerada foi indexada no motor de RAG local.
