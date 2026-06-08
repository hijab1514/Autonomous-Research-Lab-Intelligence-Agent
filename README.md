# Lacuna

Find the gaps, not just the papers.

Lacuna reads recent literature on any research topic, synthesizes the field's current state, and surfaces **grounded research gaps** — the open questions and underexplored directions worth pursuing. It is not a search engine.

[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18-61DAFB?style=flat-square&logo=react&logoColor=black)](https://react.dev)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](LICENSE)

---

## How it works

1. **Retrieve** — pulls papers from OpenAlex and arXiv with relevance gating
2. **Brief** — synthesizes consensus claims, active fronts, and contested questions
3. **Gap** — identifies what the field has *not yet addressed*, anchored to real papers

The full pipeline runs as a single `POST /api/analyze` call. Works with no API key out of the box; connect Gemini, Groq, or Ollama to upgrade from computed-signal gaps to written synthesis.

---

## Project structure

```
agents/
  literature_agent.py   relevance-gated retrieval (OpenAlex + arXiv)
  research_llm.py       LLM abstraction (Gemini · Groq · Ollama · none)
  gap_agent.py          gap & research direction engine

server/
  main.py               FastAPI — /api/health, /api/analyze
  requirements.txt

web/
  src/
    App.jsx
    components/
    styles.css          design tokens
```

---

## Getting started

**Requirements:** Python 3.10+, Node.js 18+

```bash
# Backend
pip install -r server/requirements.txt
uvicorn server.main:app --reload --port 8000

# Frontend (separate terminal)
cd web && npm install && npm run dev
```

Open `http://localhost:5173`. No API key needed.

---

## Configuration

Copy `.env.example` to `.env` and add one key to enable AI synthesis. All three are free-tier compatible.

```env
GEMINI_API_KEY=...   # or
GROQ_API_KEY=...     # or
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3
```

Without a key, gap detection runs in computed-signal mode — structurally grounded, no external calls.

---

## API

### `GET /api/health`
```json
{ "status": "ok" }
```

### `POST /api/analyze`

```json
// Request
{ "query": "transformer models in low-resource clinical NLP", "max_papers": 20 }

// Response
{
  "papers":   [ { "title": "...", "year": 2024, "source": "openalex", "url": "..." } ],
  "briefing": { "consensus": "...", "active_fronts": "...", "contested": "..." },
  "gaps":     [ { "title": "...", "description": "...", "opportunity_score": 0.84 } ],
  "mode":     "computed_signal"
}
```

---

## Known limitations

- **No persistence.** Reading list and recent queries live in React state — they reset on refresh. `localStorage` support is the next planned milestone.
- **Free AI tier limits.** Gemini and Groq free tiers are fine for demos; not suitable for sustained production traffic.
- **Bundle size.** Recharts triggers Vite's >500 kB chunk advisory. Harmless locally; code-split before deploying.

---

## Roadmap

- [ ] `localStorage` / `/api/store` persistence
- [ ] Export gap report as Markdown or PDF
- [ ] Semantic Scholar as a third retrieval source
- [ ] Topic clustering across retrieved papers
- [ ] Docker image

---

## Contributing

Issues and pull requests are welcome. Open an issue first for anything significant so we can align on direction.

---

## License

[MIT](LICENSE)
