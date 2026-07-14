# Plano de Hotfix: 01 Graph UI and Payload

## 1. Visão Geral
Este plano aborda a correção de bugs críticos identificados no Graph UI e no payload recebido pelo Backend, assegurando a estabilidade visual e a integridade dos dados renderizados.

## 2. Contexto
O usuário rejeitou a UI do MVP devido aos seguintes bugs críticos reportados:
1. Nós sumindo no drag (erro matemático no node.fx).
2. Ligações (edges) invisíveis (erro no linkCanvasObject ou ID mismatch).
3. Nomes numéricos ilegíveis (falha de payload do Backend, erro no prompt do LLM ou parsing).

## 3. Objetivos
- Restabelecer a interação de drag-and-drop sem perda de nós.
- Garantir a visibilidade correta das arestas (edges) conectando as entidades.
- Corrigir a nomenclatura das entidades para exibir os nomes reais em vez de IDs numéricos.

## 4. Dev Checklist
- [ ] **Backend:** DEVE forçar a propriedade 'id' ou 'label' do JSON a conter o NOME real da entidade (não um número).
- [ ] **Frontend:** DEVE corrigir a renderização do canvas sem quebrar as arestas.

## 5. Próximos Passos
1. Revisar as alterações propostas.
2. Implementar as correções no Backend para o payload.
3. Implementar as correções no Frontend (node.fx e linkCanvasObject).
4. Executar testes de QA e E2E.
