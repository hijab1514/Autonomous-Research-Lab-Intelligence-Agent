<<<<<<< HEAD
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
=======
<div align="center">

# Lacuna

### Find the gaps, not just the papers.

A full-stack research instrument that reads the literature, briefs the field,
and surfaces the **grounded gaps** worth pursuing — built on a React + FastAPI stack.

<br/>

![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-API-009688?logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-frontend-61DAFB?logo=react&logoColor=black)
![Vite](https://img.shields.io/badge/Vite-build-646CFF?logo=vite&logoColor=white)

</div>

---

## Overview

Lacuna is the full-stack evolution of the original Streamlit prototype. The
**engine is unchanged and stack-independent** — it now runs behind a real API,
with a React frontend that reaches a production-grade dashboard look.

| | |
|---|---|
| **Retrieval** | Relevance-gated search across OpenAlex + arXiv |
| **Synthesis** | Optional free LLM layer (Gemini · Groq · Ollama · none) |
| **Output** | Grounded gaps and research directions — not just a paper list |
| **Default mode** | Runs with **no API key** via computed-signal gap detection |

---

## Architecture

```
agents/                   the engine (unchanged, stack-independent)
├── literature_agent.py   relevance-gated retrieval (OpenAlex + arXiv)
├── research_llm.py       free LLM layer (Gemini / Groq / Ollama / none)
└── gap_agent.py          grounded gap & direction engine

server/
├── main.py               FastAPI: /api/health, /api/analyze
└── requirements.txt

web/                      React (Vite) — 3-panel workspace + dashboard
└── src/
    ├── App.jsx
    ├── components/*
    └── styles.css        design system
```

---

## Quick Start

Run two terminals from the project root.

### 1 · Backend

>>>>>>> 9c698ff8cfe148bd43c41905c081b1d2655a910b
```bash
pip install -r server/requirements.txt
uvicorn server.main:app --reload --port 8000
```

<<<<<<< HEAD
**2. Frontend**
=======
### 2 · Frontend

>>>>>>> 9c698ff8cfe148bd43c41905c081b1d2655a910b
```bash
cd web
npm install
npm run dev          # opens http://localhost:5173
```
<<<<<<< HEAD
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
=======

> **Same-origin by design** — the dev server proxies `/api` to the backend on
> `:8000`, so there's no CORS fuss in normal use.

### Enabling grounded AI (optional)

Lacuna works out of the box in **computed-signal gap mode** with no key. To turn
on grounded AI synthesis:

```bash
cp .env.example .env     # in the project root
# then add one free API key
```

The server loads the key on startup and the gap panel switches from computed
signals to written synthesis.

---

## What's Verified

- **Backend** — `/api/analyze` returns papers, a field briefing, and grounded
  gaps in a single call. Tested end-to-end, offline, with mocked retrieval.
- **Frontend** — production build compiles clean (2,331 modules, `npm run build`).

---

## Honest Limits

- **No persistence yet.** Recent topics and the reading list live in React state
  and reset on refresh. Adding `localStorage` or an `/api` store is the next step.
- **Free AI tiers** are for prototyping and demo load — not production traffic.
- **Bundle advisory.** The recharts bundle trips Vite's >500 kB chunk warning.
  Harmless for a local app; code-split before deploying.

---

## Design

A dark **"research instrument"** aesthetic:

- **Type** — Fraunces (display) + Hanken Grotesk (body)
- **Surface** — deep-ink background with a faint gradient mesh and grain
- **Components** — glass panels, a single accent color
- **Tokens** — all live in `web/src/styles.css`
>>>>>>> 9c698ff8cfe148bd43c41905c081b1d2655a910b
