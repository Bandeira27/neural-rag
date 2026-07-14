# Night Watch - UI/UX & Design Manifesto

This manifesto dictates the "Gold Standard" UI requirements for Night Watch.

## 1. Aesthetic & Theme
- **Theme:** Strict Tailwind Dark Mode.
- **Translucency & Polish:** UI must feature translucent hovers, explicit anomalies, and "Pixel Perfecting". Minute details (like 32x32px icon crispness and aliasing) matter. Prepare for aggressive asset optimization.
- **Vibe:** The app must feel like it's "watching" (SecResearcher UX). 

## 2. Component Architecture
- **Shadcn/ui ONLY:** BANNED: ANY interactive native HTML (buttons, inputs MUST be Shadcn). You are strictly forbidden from using native HTML elements for complex controls. For example, NEVER use `<select>`; you MUST use Shadcn Combobox/Select.
- **CSS Strictness:** BANNED: CSS `!important` and hardcoded hex colors.
- **Accessibility (a11y):** Mandatory keyboard navigation and ARIA roles for all components.
- **Virtualization:** For mass data handling, you MUST use virtualization (e.g., TanStack Virtual).
- **Graph & Node UX:** For the SecResearcher UX, NEVER omit nodes/jumps in graphs. Visual anomalies must be classified explicitly.

## 3. Error Handling
- **Graceful Failures:** Errors must be handled gracefully via Shadcn Toasts and Empty States.
- **Workarounds:** Prefer parking features over settling for CSS workarounds if proper design assets are missing.
