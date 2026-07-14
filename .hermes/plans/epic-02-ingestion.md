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

### US-01: Crawler Parametrizado
**Como** sistema de ingestão
**Quero** receber o caminho alvo do repositório via argumentos de CLI ou variáveis de ambiente
**Para que** o crawler possa processar repositórios dinamicamente sem diretórios hardcoded.

- **Cenário 1: Crawler inicia com caminho fornecido via variável de ambiente**
  - **Dado** que a variável de ambiente `REPO_PATH` está definida como `/caminho/para/repositorio`
  - **Quando** o processo do crawler é iniciado
  - **Então** o crawler deve ler e processar os arquivos do diretório `/caminho/para/repositorio`.

- **Cenário 2: Crawler inicia com caminho via argumento de CLI**
  - **Dado** que o crawler é executado com a flag `--path=/caminho/para/repositorio2`
  - **Quando** o processo do crawler é iniciado
  - **Então** o crawler deve priorizar o argumento de CLI e processar `/caminho/para/repositorio2`.

- **Cenário 3: Falha ao iniciar sem caminho fornecido**
  - **Dado** que nem a variável de ambiente nem o argumento de CLI foram fornecidos
  - **Quando** o processo do crawler é iniciado
  - **Então** o sistema deve retornar um erro claro e abortar a execução imediatamente.

### US-02: Resolução de Entidades (Entity Resolution)
**Como** pipeline de dados
**Quero** utilizar o LLM para resolver e realizar o merge de nós (nodes) duplicados ou sinônimos
**Para que** a base de conhecimento (grafo) mantenha entidades únicas e não redundantes.

- **Cenário 1: Merge de entidades sinônimas**
  - **Dado** que o crawler extraiu duas entidades conceitualmente idênticas (ex: "Autenticação" e "Login")
  - **E** a resposta do LLM indica que elas representam o mesmo conceito
  - **Quando** a rotina de resolução de entidades é executada
  - **Então** as entidades devem sofrer merge em um único nó
  - **E** as arestas e metadados de ambas devem ser consolidados no nó resultante.

- **Cenário 2: Entidades distintas não sofrem merge**
  - **Dado** que o crawler extraiu duas entidades diferentes
  - **E** a avaliação do LLM indica que possuem conceitos distintos
  - **Quando** a rotina de resolução de entidades é executada
  - **Então** ambas devem permanecer como nós separados e independentes no grafo.

### US-03: Persistência Dupla
**Como** módulo de persistência
**Quero** salvar dados em ChromaDB para os embeddings e em SQLite para o estado relacional
**Para que** suporte consultas semânticas no RAG e mantenha integridade de metadados relacionais e controle de crawling.

- **Cenário 1: Inserção síncrona bem-sucedida**
  - **Dado** que uma nova entidade e seus nós foram processados com sucesso
  - **Quando** o sistema salva os dados
  - **Então** os embeddings vetoriais devem ser armazenados no ChromaDB
  - **E** os metadados (IDs, nomes, referências de arquivos) devem ser gravados no SQLite
  - **E** o estado da ingestão deve refletir os dados sincronizados.

- **Cenário 2: Consistência em caso de falha**
  - **Dado** que a persistência de uma entidade está em andamento
  - **Quando** ocorrer uma falha durante a escrita no ChromaDB (ex: timeout) ou no SQLite (ex: lock de banco)
  - **Então** a operação deve falhar atomicamente
  - **E** nenhum dado parcial daquela entidade deve ser persistido em nenhuma das bases (comportamento análogo a rollback/compensação).

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
