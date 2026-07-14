# Hotfix 03 System Recovery Plan

## 1. Contexto
A aplicação sofreu um "Total Meltdown" (Hotfix 02). O Auditor/Tech Lead iniciou a investigação de root causes no frontend.

## 2. Root Causes Encontrados (RCA)

### 2.1. `frontend/public/graph.json`
- **Estrutura:** O arquivo JSON **não** está malformado do ponto de vista sintático (possui as chaves `"nodes"` e `"links"` corretamente mapeadas). Não há chaves em português como "nós" ou conversa fiada.
- **Problema de Dados:** Os IDs (`id`) das chaves em `"nodes"` são strings de texto longas/frases completas (ex: `"Auditor / Tech Lead: Identifies impact..."`). A propriedade `"name"` (esperada pelo frontend para a prop `nodeLabel`) não existe nos objetos. 

### 2.2. `frontend/src/components/NeuralGraph.jsx`
- **Imports:** A importação de `useRef` **NÃO** faltou (está presente na linha 1: `import React, { useRef, useCallback, useState, useEffect } from 'react';`).
- **Problemas no Componente:** 
  1. A prop `nodeLabel="name"` busca a chave `name`, que não existe no `graph.json`.
  2. No `nodeCanvasObject`, a renderização do texto acessa `node.label` (que não existe) e faz fallback para `node.id` (que é um texto imenso e quebra o canvas).
  3. No `onNodeDragEnd`, a chamada `fgRef.current.d3ReheatSimulation()` é feita, que na v2 é correto, mas a desativação de físicas no `fx`/`fy` e a animação do canvas podem estar desestabilizando o d3Force (falta verificação de null safety no acesso ao current da ref durante inicializações rápidas).

## 3. Checklist de Correção OBRIGATÓRIA (Frontend e Backend)

### Backend (BDD)
- **Cenário: Geração do Grafo**
  - **Dado** que o sistema RAG gera os nós do grafo
  - **Então** o JSON gerado DEVE ter um `id` (formato curto/slug)
  - **E** DEVE ter um `label` (Texto descritivo em PT-BR, máx 3 palavras)

### Frontend (BDD)
- **Cenário: Renderização Segura do Grafo**
  - **Dado** que o componente `NeuralGraph.jsx` é montado
  - **Então** ele DEVE implementar null safety explícito nas interações físicas (ex: `fgRef.current?.d3ReheatSimulation()`)
  - **E** DEVE pintar APENAS a propriedade `label` no canvas, evitando estourar o limite de exibição do nó

### Frontend (Checklist Original)
- [ ] Atualizar `graph.json` com IDs únicos curtos (ex: `"id": "node_1"`) e adicionar propriedades `"label"` ou `"name"` para os textos descritivos.
- [ ] Em `NeuralGraph.jsx`, corrigir o mapeamento da propriedade de texto (alterar `nodeLabel` para bater com os dados).
- [ ] Adicionar null safety (`if (!fgRef.current) return;`) nas chamadas dentro de `useEffect` (especialmente no `setTimeout`) e em `onNodeDragEnd`.
- [ ] Tratar quebras de linha ou truncamento de texto no canvas (o texto atual nos `ids` extrapola a tela).

### Backend
- [ ] Se o JSON for gerado dinamicamente pelo backend, corrigir o serializador/DTO para exportar um formato compatível e tipado (com `id` limpo, e sem injetar frases inteiras na chave primária de relacionamento D3).
- [ ] Adicionar teste unitário validando o payload da estrutura de grafo (`nodes` e `links`) contra o schema esperado pelo frontend.
