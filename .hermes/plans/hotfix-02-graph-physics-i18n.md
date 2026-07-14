# Plan: Hotfix 02 - Graph Physics and i18n

## 1. Objective
Resolve D3 engine physics issues causing nodes to disappear, fix Canvas font sizing, and enforce Portuguese-BR for graph labels.

## 2. Context
1) Nós sumindo ao arrastar (falha na engine D3).
2) Tamanho da fonte abusivo no Canvas.
3) Idioma incorreto dos nós.

## 3. Architecture & Approach
- **Frontend:** Update `NeuralGraph.jsx` to properly manage D3 simulation state and adjust canvas rendering parameters.
- **Backend:** Update the RAG extraction prompt to enforce the correct output language for entity labels.

### BDD Scenarios
1) **Cenário (Backend):** Quando o LLM processa o texto, Então TODOS os labels do JSON extraído devem ser em Português-BR.
2) **Cenário (Frontend):** Quando o usuário solta um nó (dragEnd), Então a simulação D3 DEVE ser reaquecida e o nó volta à orbita, e a fonte deve ser legível/pequena.

## 4. Dev Checklist
- [ ] Frontend DEVE implementar o `fgRef.current.d3ReheatSimulation()` e controlar a física real para impedir o sumiço dos nós, além de diminuir o fontSize no nodeCanvasObject.
- [ ] Backend DEVE alterar o prompt do LLM para forçar a extração dos labels em Português-BR.

## 5. Definition of Done
- Nodes can be dragged without disappearing.
- Font sizes on the canvas are readable and proportionate.
- Node labels are exclusively in Portuguese-BR.
