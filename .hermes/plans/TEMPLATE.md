# Hermes Plan Mode - Template

## 1. Meta
- [ ] **ID:** 
- [ ] **Autor:** 
- [ ] **Data:** 

## 2. Contexto/Auditoria
- [ ] Definir contexto e propósito da alteração.
- [ ] Estrutura de Pastas e Nomenclatura definidas.
- [ ] Auditoria concluída e impactos no sistema mapeados.

## 3. User Stories e Critérios de Aceite (BDD)
- [ ] Cenários BDD (Given / When / Then) escritos.
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