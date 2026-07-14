# Plano de Hotfix: 01 Graph UI and Payload

## 1. Visão Geral
Este plano aborda a correção de bugs críticos identificados no Graph UI e no payload recebido pelo Backend, assegurando a estabilidade visual e a integridade dos dados renderizados.

## 2. Contexto
O usuário rejeitou a UI do MVP devido aos seguintes bugs críticos reportados:
1. Nós sumindo no drag (erro matemático no node.fx).
2. Ligações (edges) invisíveis (erro no linkCanvasObject ou ID mismatch).
3. Nomes numéricos ilegíveis (falha de payload do Backend, erro no prompt do LLM ou parsing).

## 3. User Stories e BDDs
1. **Cenário para o Backend:** Dado que o crawler/export_to_ui roda, Quando gera o graph.json, Então o campo 'id' (ou 'label') dos nós DEVE ser o nome textual extraído da entidade e NÃO um UUID numérico opaco.
2. **Cenário para o Frontend:** Dado que o usuário clica e arrasta um nó, Quando solta o botão (dragEnd), Então o nó não deve desaparecer da tela e deve manter suas arestas visíveis conectadas.

## 4. Dev Checklist
- [ ] **Backend:** DEVE forçar a propriedade 'id' ou 'label' do JSON a conter o NOME real da entidade (não um número).
- [ ] **Frontend:** DEVE corrigir a renderização do canvas sem quebrar as arestas.

## 5. Próximos Passos
1. Revisar as alterações propostas.
2. Implementar as correções no Backend para o payload.
3. Implementar as correções no Frontend (node.fx e linkCanvasObject).
4. Executar testes de QA e E2E.
