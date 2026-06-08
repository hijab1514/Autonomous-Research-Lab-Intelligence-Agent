<div align="center">

<h1>Lacuna</h1>

<p><strong>Find the gaps, not just the papers.</strong></p>

<p>A research intelligence platform that reads the literature, maps the field,<br/>and surfaces the unexplored opportunities worth pursuing.</p>

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18-61DAFB?style=flat-square&logo=react&logoColor=black)](https://react.dev)
[![Vite](https://img.shields.io/badge/Vite-5-646CFF?style=flat-square&logo=vite&logoColor=white)](https://vitejs.dev)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](LICENSE)
[![No Key Required](https://img.shields.io/badge/No%20API%20Key-Required-blueviolet?style=flat-square)]()

<br/>

[Quick Start](#quick-start) · [How It Works](#how-it-works) · [API](#api-reference) · [Roadmap](#roadmap)

</div>

---

## What is Lacuna?

Most research tools solve the wrong problem. You search a topic, get a list of papers, read them — and still aren't sure what to *do next*.

**Lacuna is different.** It doesn't just find what's been done — it identifies what *hasn't*. It retrieves recent literature, synthesizes the field's current state, and surfaces **grounded research gaps**: open questions, underexplored directions, and overlooked intersections that represent real opportunities for original contribution.

---

## Key Features

- 🔍 **Relevance-Gated Retrieval** — searches OpenAlex (250M+ works) and arXiv in parallel, filtering noise before it reaches analysis
- 📋 **Field Briefing Engine** — generates a structured overview: dominant methods, active fronts, key debates, and emerging directions
- 🕳️ **Grounded Gap Detection** — identifies what the field hasn't addressed yet, anchored to real papers — not hallucinated
- 🤖 **Flexible AI Layer** — optionally deepen synthesis with Gemini, Groq, or a local Ollama model
- ⚡ **Zero-Config Default** — fully functional gap detection with no API keys, no accounts, no setup beyond `pip install`

---

## Architecture

```
lacuna/
├── agents/
│   ├── literature_agent.py   # Relevance-gated retrieval (OpenAlex + arXiv)
│   ├── research_llm.py       # LLM abstraction (Gemini · Groq · Ollama · none)
│   └── gap_agent.py          # Grounded gap & research direction engine
│
├── server/
│   ├── main.py               # FastAPI: /api/health, /api/analyze
│   └── requirements.txt
│
└── web/
    └── src/
        ├── App.jsx
        ├── components/       # Search, Briefing, Gap panels
        └── styles.css        # Design system tokens
```

### Pipeline

```
Query → Literature Agent → Relevance Filter → Research LLM (optional)
                                                      ↓
                                               Gap Agent Engine
                                          ┌─────────┴──────────┐
                                   Computed Signals       LLM Synthesis
                                   (no API key)          (with API key)
                                          └─────────┬──────────┘
                                                     ↓
                                     Field Briefing + Gap Report
                                       delivered via /api/analyze
```

---

## Quick Start

**Requirements:** Python 3.10+, Node.js 18+

```bash
# 1. Clone
git clone https://github.com/your-username/lacuna.git
cd lacuna

# 2. Backend
pip install -r server/requirements.txt
uvicorn server.main:app --reload --port 8000

# 3. Frontend (new terminal)
cd web && npm install && npm run dev
```

Open **http://localhost:5173** — no API key needed.

---

## Configuration

Lacuna runs in **computed-signal mode** by default. To enable written AI synthesis, add one free key:

```bash
cp .env.example .env
```

```env
GEMINI_API_KEY=...        # Google Gemini (free tier)
GROQ_API_KEY=...          # Groq (free tier, fast)
OLLAMA_BASE_URL=http://localhost:11434   # Local Ollama
OLLAMA_MODEL=llama3
```

| Mode | Key Required | Output |
|---|---|---|
| Computed Signal | None | Structural gaps from pattern analysis |
| Gemini / Groq | One free key | Written, contextualized synthesis |
| Ollama | Local install | Full synthesis, fully private |

The server auto-detects which key is present at startup. No code changes needed.

---

## How It Works

**Stage 1 — Retrieval**
`LiteratureAgent` queries OpenAlex and arXiv in parallel, scores results for relevance, and discards noise before anything reaches synthesis.

**Stage 2 — Field Briefing**
The retained papers are analyzed for consensus claims, active research fronts, contested questions, and dominant methodologies.

**Stage 3 — Gap Detection**
`GapAgent` scans the briefing for structural absence — patterns, populations, or methods consistently *unaddressed* in the literature. In computed-signal mode this is statistical; with an LLM key, gaps are written out as structured research directions with grounding.

Everything runs as a single `POST /api/analyze` call.

---

## API Reference

### `GET /api/health`
```json
{ "status": "ok" }
```

### `POST /api/analyze`

```json
// Request
{
  "query": "transformer models in low-resource clinical NLP",
  "max_papers": 20
}
```

```json
// Response
{
  "papers": [
    { "title": "...", "authors": ["..."], "year": 2024, "source": "openalex", "url": "..." }
  ],
  "briefing": {
    "consensus": "...",
    "active_fronts": "...",
    "contested": "...",
    "methods": "..."
  },
  "gaps": [
    { "title": "...", "description": "...", "grounding": "...", "opportunity_score": 0.84 }
  ],
  "mode": "computed_signal"
}
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React 18 + Vite |
| Charts | Recharts |
| Backend | FastAPI + Uvicorn |
| Retrieval | OpenAlex API, arXiv API |
| AI (optional) | Gemini · Groq · Ollama |
| Validation | Pydantic v2 |

---

## Roadmap

- [ ] `localStorage` / `/api/store` persistence for reading list and recent queries
- [ ] Export gap report as Markdown or PDF
- [ ] Semantic Scholar as a third retrieval source
- [ ] Topic clustering across retrieved papers
- [ ] Docker image for one-command deployment
- [ ] Hosted demo environment

---

## Known Limitations

| | |
|---|---|
| **No persistence** | Reading list and recent queries reset on page refresh. Planned for next milestone. |
| **Free tier limits** | Gemini and Groq free tiers suit demos and prototyping — not sustained production traffic. |
| **Bundle size** | Recharts triggers Vite's >500 kB chunk advisory. Harmless locally; code-split before deploying. |

---

## Contributing

Issues and PRs are welcome. Please open an issue before starting significant work so we can align on direction.

```bash
git checkout -b feature/your-feature
# make changes
# open pull request
```

---

## License

[MIT](LICENSE)
