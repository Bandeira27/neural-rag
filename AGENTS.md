# Night Watch - AI Agents Global Directive

This file establishes the immutable physics of the Night Watch project for any AI agent interacting with the codebase. If you are reading this, YOU MUST OBEY THESE RULES.

## 1. Role & Workflow Constraints
- **Hermes is the Orchestrator/Architect.** Hermes DOES NOT edit code manually. All execution must be delegated.
- **Workflow Pipeline:**
  1. **Auditor / Tech Lead: Identifies impact, defines EXACT folder structure/scaffolding, and performs strict static Code Review before QA.**
  2. **Documentation (Planning Phase):** Drafts User Stories, Use Cases, and Acceptance Criteria (BDD style) before execution begins, ensuring Dev and QA have clear business rules.
  3. **DevOps & SecOps:** Manages CI/CD, pre-commit hooks, and environment compatibility (Kali Linux/Webkit2GTK). Enforces pipeline security (mandatory anti-XSS rules and CVE scanning).
  4. **Execution (Dev):** Follow the audit plan and User Stories strictly. Writes Tests BEFORE Code.
  5. **Gatekeeper (QA/Red Team):** Audit UI/UX and tests before any PR. Attempts to break the UI based on Acceptance Criteria.
  6. **Documentation (Release Phase):** Maintains ADRs (Architectural Decision Records), updates i18n keys, ensures 100% Portuguese technical documentation, and mandatorily injects/indexes new ADRs, rules, and User Stories into the local RAG vector database.
- **Test-Before-Merge (TDD):** You MUST write Unit Tests and E2E (Playwright) before or alongside implementation. NO EXCEPTIONS. 1:1 Traceability between BDD Scenarios and Playwright tests is mandatory.

## 2. Technical Strictness
- **Secret Protection (Gitignore First): É TERMINANTEMENTE PROIBIDO criar chaves, senhas, ou arquivos .env sem antes declarar o rastreio no .gitignore. O DevOps deve atestar a blindagem antes de qualquer commit.**
- **Binary/Executable Testing:** All resolution of bugs and features MUST be tested against extensionless binary files in the Linux environment (e.g., `/bin/ls`, `/usr/bin/sudo`) and symlinks.
- **I18n:** Do NOT use raw string keys. Everything must go through `react-i18next`. 100% Portuguese.
- **Stability:** Out-of-Memory (OOM) errors or crashes equal an automatic FAIL of the PR.
- **Clean Trees:** Strict PR hygiene. Do not commit temporary hacks.
- **Environment:** The host environment uses Kali Linux (Webkit2GTK). Assume trackpad navigation for complex UIs (like React Flow). Avoid native OS shortcuts that conflict with X11/Wayland (e.g., Ctrl+Wheel); prioritize web-physics pan/zoom.
- **No Native HTML for Complex Data:** Never use native tags like `<select>` for data sets. See DESIGN.md.