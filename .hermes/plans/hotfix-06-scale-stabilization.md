# Plan: Hotfix 06 Scale Stabilization

## 1. Objetivo
Estabilizar o comportamento de zoom e escala no NeuralGraph.

## 2. Contexto
*   **Falha Identificada:** Zoom monstruoso e incontrolável; nós ficam imensos.
*   **Root Cause:** Conflito entre o `nodeCanvasObject` fixo (alteração no tamanho da fonte no Hotfix 02 descalibrou o `globalScale`) e as câmeras e raios nativos do D3, resultando em cálculos de caixa de colisão errados e ampliação bizarra do canvas.

## 3. Escopo
Frontend (Componente NeuralGraph.jsx).

## 4. Dev Checklist
Solução Definitiva para o Frontend:
*   [ ] 1. **DEVE** usar o parâmetro oficial `nodeRelSize={6}` no componente.
*   [ ] 2. **DEVE** reimplementar a lógica de texto dentro do `nodeCanvasObject` multiplicando a fonte estritamente por `12/globalScale` ou um valor dinâmico simples, garantindo que o texto escale junto com o zoom sem bugar os raios.
*   [ ] 3. **REMOVER** os códigos experimentais do Hotfix anterior de `centerAt/zoom` no `onNodeClick` se causarem loops (deixar a câmera fluir nativamente).
