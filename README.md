# Lacuna (full-stack) — find the gaps, not just the papers

React + FastAPI build. Same engine as the Streamlit version, now behind a real
API with a React frontend that can reach a production dashboard look.

```
agents/                 the engine (unchanged, stack-independent)
  literature_agent.py   relevance-gated retrieval (OpenAlex + arXiv)
  research_llm.py        free LLM layer (Gemini / Groq / Ollama / none)
  gap_agent.py           grounded gap & direction engine
server/
  main.py                FastAPI: /api/health, /api/analyze
  requirements.txt
web/                     React (Vite) — 3-panel workspace + dashboard
  src/App.jsx, src/components/*, src/styles.css (design system)
```

## Run it — two terminals, from the project root

**1. Backend**
```bash
pip install -r server/requirements.txt
uvicorn server.main:app --reload --port 8000
```

**2. Frontend**
```bash
cd web
npm install
npm run dev          # opens http://localhost:5173
```
The dev server proxies `/api` to the backend on :8000, so it's same-origin —
no CORS fuss in normal use.

Works with **no API key** (computed-signal gap mode). To turn on grounded AI,
copy `.env.example` to `.env` in the project root and add one free key; the
server loads it on startup and the gap panel switches to written synthesis.

## What's verified
- Backend: `/api/analyze` returns papers + field briefing + grounded gaps in one
  call (tested end-to-end, offline with mocked retrieval).
- Frontend: production build compiles clean (2331 modules, `npm run build`).

## Honest limits
- Recent topics + reading list live in React state — they reset on refresh.
  Persistence (localStorage or a `/api` store) is the next step.
- Free AI tiers are for prototyping/demo load, not production traffic.
- The recharts bundle triggers Vite's >500 kB chunk advisory; harmless for a
  local app — code-split if you deploy.

## Design
Dark "research instrument" aesthetic: Fraunces (display) + Hanken Grotesk (body),
deep-ink background with a faint gradient mesh + grain, glass panels, one accent.
Tokens live in `web/src/styles.css`.
