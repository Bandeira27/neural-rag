# Hotfix 04: Cloud LLM Migration

## Section 1: Overview
Migrate the local LLM generation to a Cloud LLM provider (OpenRouter).

## Section 2: Justification (Phi-3 Collapse)
O modelo Phi-3 local demonstrou colapso estrutural e instabilidade severa durante a geração (alucinações e falhas graves na formatação). A decisão pela migração para a nuvem via OpenRouter foi tomada para garantir resiliência estruturada. Utilizar a infraestrutura Cloud resolve as limitações de recursos locais e assegura o uso de modelos mais robustos e confiáveis na aderência ao formato exigido.

## Section 3: Architecture
- API Provider: OpenRouter
- Auth: Environment Variables

## Section 4: Dev Checklist
- [ ] 1) O script backend deve ler a variável `OPENROUTER_API_KEY` do arquivo `.env`.
- [ ] 2) Deve usar a biblioteca `requests` ou `openai` para fazer POST na API do OpenRouter usando um modelo free (ex: `meta-llama/llama-3-8b-instruct:free`).
- [ ] 3) O prompt rigoroso de JSON deve ser mantido.
