<div align="center">

<br/>

```
██╗      █████╗  ██████╗██╗   ██╗███╗   ██╗ █████╗
██║     ██╔══██╗██╔════╝██║   ██║████╗  ██║██╔══██╗
██║     ███████║██║     ██║   ██║██╔██╗ ██║███████║
██║     ██╔══██║██║     ██║   ██║██║╚██╗██║██╔══██║
███████╗██║  ██║╚██████╗╚██████╔╝██║ ╚████║██║  ██║
╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝
```

### **Find the gaps, not just the papers.**

*A research intelligence platform that reads the literature, maps the field,<br/>and surfaces the unexplored opportunities worth pursuing — not another search engine.*

<br/>

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18+-61DAFB?style=flat-square&logo=react&logoColor=black)](https://react.dev)
[![Vite](https://img.shields.io/badge/Vite-5+-646CFF?style=flat-square&logo=vite&logoColor=white)](https://vitejs.dev)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=flat-square)]()
[![No API Key Required](https://img.shields.io/badge/No%20API%20Key-Required-blueviolet?style=flat-square)]()

<br/>

[**Live Demo**](#demo) · [**Quick Start**](#quick-start) · [**How It Works**](#how-it-works) · [**Roadmap**](#roadmap) · [**Contribute**](#contributing)

<br/>

</div>

---

## The Problem

Most research tools solve the wrong problem.

You search for a topic → you get a list of papers → you read them → you're still not sure what to *do next*.

**Lacuna is different.** It doesn't just find what's been done — it identifies what *hasn't* been done. It reads the recent literature, synthesizes the field's current state, and surfaces **grounded research gaps**: the open questions, underexplored directions, and overlooked intersections that represent real opportunities for original contribution.

Whether you're a researcher, student, or engineer entering a new domain, Lacuna turns hours of literature review into minutes of structured insight.

---

## Table of Contents

1. [Overview](#overview)
2. [Key Features](#key-features)
3. [Architecture](#architecture)
4. [Demo](#demo)
5. [Quick Start](#quick-start)
6. [Installation](#installation)
7. [Configuration](#configuration)
8. [How It Works](#how-it-works)
9. [API Reference](#api-reference)
10. [Technology Stack](#technology-stack)
11. [Roadmap](#roadmap)
12. [Known Limitations](#known-limitations)
13. [Contributing](#contributing)
14. [License](#license)

---

## Overview

Lacuna is a full-stack **research gap discovery platform** built on a React + FastAPI architecture. At its core is a multi-stage pipeline that retrieves papers from OpenAlex and arXiv, constructs a field briefing, and generates grounded research directions — either through computed signal analysis (no API key needed) or via an optional LLM layer.

| Dimension | What Lacuna Does |
|---|---|
| 🔍 **Retrieval** | Searches thousands of scholarly papers from OpenAlex and arXiv with relevance gating |
| 🧠 **Synthesis** | Produces a structured field briefing: consensus, active fronts, contested claims |
| 🕳️ **Gap Detection** | Identifies unexplored angles, missing experiments, and open questions |
| 🤖 **AI Layer** | Optionally deepens synthesis with Gemini, Groq, or a local Ollama model |
| 🔑 **Zero Key Mode** | Runs fully offline-capable gap detection with no API credentials required |

---

## Key Features

### 🕳️ Grounded Gap Detection
Goes beyond keyword matching to map what the field has *not yet addressed*. Gaps are anchored to actual papers — every finding is traceable.

### 📡 Multi-Source Academic Retrieval
Pulls from two of the most comprehensive open scholarly databases — OpenAlex (250M+ works) and arXiv — with built-in relevance filtering so noise stays out.

### 📋 Field Briefing Engine
Automatically generates a structured overview of the domain: dominant methods, recent shifts, key debates, and emerging directions. Land in any field in minutes.

### 🤖 Flexible AI Synthesis (Optional)
Connect any of the major free AI tiers — Google Gemini, Groq, or a local Ollama model — to upgrade from computed signals to full written synthesis. Or skip it entirely.

### 🖥️ 3-Panel Research Workspace
A purpose-built dark UI with a reading list, live analysis panel, and gap dashboard — designed to feel like a research instrument, not a generic SaaS tool.

### ⚡ Zero-Config Default
Clone, install, run. No API keys, no accounts, no environment variables required for the default mode. Grounded gap detection works out of the box.

---

## Architecture

```
lacuna/
│
├── agents/                         # The core engine — stack-independent
│   ├── literature_agent.py         # Relevance-gated retrieval (OpenAlex + arXiv)
│   ├── research_llm.py             # Free LLM abstraction (Gemini · Groq · Ollama · none)
│   └── gap_agent.py                # Grounded gap & research direction engine
│
├── server/                         # FastAPI backend
│   ├── main.py                     # Routes: /api/health, /api/analyze
│   └── requirements.txt
│
├── web/                            # React + Vite frontend
│   └── src/
│       ├── App.jsx                 # Root component + state management
│       ├── components/             # Panel components (Search, Briefing, Gaps)
│       └── styles.css              # Design system tokens
│
├── .env.example                    # Environment variable template
└── README.md
```

### Data Flow

```
User Query
    │
    ▼
Literature Agent ──► OpenAlex API ──┐
                └──► arXiv API    ──┤
                                    │
                                    ▼
                            Relevance Filter
                                    │
                                    ▼
                         Research LLM Layer (optional)
                                    │
                                    ▼
                            Gap Agent Engine
                          ┌─────────┴──────────┐
                          │                    │
                   Computed Signals       LLM Synthesis
                   (no API key)          (with API key)
                          │                    │
                          └─────────┬──────────┘
                                    │
                                    ▼
                    ┌───────────────────────────────┐
                    │  Field Briefing + Gap Report  │
                    │  delivered via /api/analyze   │
                    └───────────────────────────────┘
                                    │
                                    ▼
                          React Frontend (port 5173)
```

---

## Demo

> 📸 *Screenshots and a recorded walkthrough are coming in the next release. See [#contributing](#contributing) if you'd like to help document the UI.*

**Planned demo assets:**
- [ ] Animated GIF of a full analysis run
- [ ] Screenshot: 3-panel workspace
- [ ] Screenshot: Gap detection panel
- [ ] Screenshot: Field briefing output
- [ ] Hosted demo environment

---

## Quick Start

Get Lacuna running locally in under two minutes.

**Prerequisites:** Python 3.10+, Node.js 18+

```bash
# 1. Clone the repository
git clone https://github.com/your-username/lacuna.git
cd lacuna

# 2. Start the backend (Terminal 1)
pip install -r server/requirements.txt
uvicorn server.main:app --reload --port 8000

# 3. Start the frontend (Terminal 2)
cd web
npm install
npm run dev
```

Open **http://localhost:5173** — Lacuna is ready. No API keys needed.

---

## Installation

### Backend

```bash
# From the project root
pip install -r server/requirements.txt
```

**Core dependencies:**

| Package | Purpose |
|---|---|
| `fastapi` | API framework |
| `uvicorn` | ASGI server |
| `httpx` | Async HTTP client for academic APIs |
| `pydantic` | Request/response validation |

### Frontend

```bash
cd web
npm install
```

**Core dependencies:**

| Package | Purpose |
|---|---|
| `react` + `vite` | UI framework + build tooling |
| `recharts` | Gap visualization charts |
| `axios` | HTTP client (proxied to backend) |

> **Note:** The Vite dev server proxies all `/api` requests to the backend on `:8000`, so no CORS configuration is needed in local development.

---

## Configuration

Lacuna works out of the box in **computed-signal mode** with no configuration required. To enable AI-powered synthesis, add one free API key.

### Step 1 — Copy the environment template

```bash
cp .env.example .env
```

### Step 2 — Add one key (choose any)

```env
# Option A: Google Gemini (free tier available)
GEMINI_API_KEY=your_key_here

# Option B: Groq (free tier, fast inference)
GROQ_API_KEY=your_key_here

# Option C: Ollama (fully local, no account needed)
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3
```

The server detects which key is present at startup and switches the gap panel from computed signals to written synthesis automatically. No code changes needed.

| Mode | API Key | Gap Quality | Speed |
|---|---|---|---|
| Computed Signal | None required | Structural gaps from signal analysis | Fast |
| Gemini | `GEMINI_API_KEY` | Written, contextualized synthesis | Moderate |
| Groq | `GROQ_API_KEY` | Written synthesis, very fast inference | Fast |
| Ollama | Local URL | Full synthesis, fully private | Varies |

---

## How It Works

Lacuna runs a **three-stage pipeline** on every query.

### Stage 1 — Relevance-Gated Retrieval

The `LiteratureAgent` queries OpenAlex and arXiv in parallel, then applies a relevance gate — scoring and filtering results so only topically grounded papers proceed. This prevents noisy or tangential results from polluting the downstream analysis.

### Stage 2 — Field Briefing Construction

The retained papers are passed to the synthesis layer, which extracts:
- **Consensus claims** — what the field broadly agrees on
- **Active research fronts** — where current work is concentrated
- **Contested claims** — open debates and unresolved questions
- **Methodological norms** — dominant techniques and their limitations

### Stage 3 — Gap Detection

The `GapAgent` analyzes the briefing for structural absence — patterns, populations, methods, or timeframes that appear consistently *unaddressed* in the literature. In computed-signal mode, this is done through statistical pattern analysis. With an LLM key, the gaps are written out as structured research directions with justification.

The full pipeline runs as a single `POST /api/analyze` call and returns papers, briefing, and gaps together.

---

## API Reference

### `GET /api/health`

Returns server status.

```json
{ "status": "ok" }
```

---

### `POST /api/analyze`

Runs the full Lacuna pipeline on a research query.

**Request**

```json
{
  "query": "transformer models in low-resource clinical NLP",
  "max_papers": 20
}
```

| Field | Type | Required | Description |
|---|---|---|---|
| `query` | `string` | ✅ | Research topic or question |
| `max_papers` | `integer` | ❌ | Max papers to retrieve (default: 20) |

**Response**

```json
{
  "papers": [
    {
      "title": "...",
      "authors": ["..."],
      "year": 2024,
      "source": "openalex",
      "url": "https://..."
    }
  ],
  "briefing": {
    "consensus": "...",
    "active_fronts": "...",
    "contested": "...",
    "methods": "..."
  },
  "gaps": [
    {
      "title": "...",
      "description": "...",
      "grounding": "...",
      "opportunity_score": 0.84
    }
  ],
  "mode": "computed_signal"
}
```

---

## Technology Stack

| Layer | Technology | Role |
|---|---|---|
| **Frontend** | React 18 + Vite | 3-panel research workspace |
| **Visualization** | Recharts | Gap opportunity charts |
| **Backend** | FastAPI | REST API, pipeline orchestration |
| **Server** | Uvicorn (ASGI) | Async Python server |
| **Retrieval** | OpenAlex API | 250M+ scholarly works |
| **Retrieval** | arXiv API | Preprint and CS/STEM papers |
| **AI (optional)** | Google Gemini | Cloud LLM synthesis |
| **AI (optional)** | Groq | Fast cloud LLM inference |
| **AI (optional)** | Ollama | Local LLM, fully private |
| **Validation** | Pydantic v2 | Request/response schemas |
| **Design** | Fraunces + Hanken Grotesk | Research instrument typography |

---

## Roadmap

> Contributions are welcome for any of these. See [Contributing](#contributing).

### Near Term
- [ ] `localStorage` persistence for reading list and recent queries
- [ ] `/api/store` endpoint for server-side session persistence
- [ ] Export gap report as PDF or Markdown
- [ ] Recharts bundle code-splitting (Vite chunk size advisory)

### Medium Term
- [ ] Citation graph visualization
- [ ] Topic clustering across retrieved papers
- [ ] Saved workspaces (user accounts or file-based)
- [ ] Semantic Scholar integration as a third retrieval source

### Long Term
- [ ] Collaborative gap annotation (multi-user)
- [ ] Weekly digest mode: track a topic over time
- [ ] API-first mode for notebook / script integration
- [ ] Plugin architecture for custom retrieval sources

---

## Known Limitations

| Limitation | Detail |
|---|---|
| **No persistence** | Reading lists and recent topics live in React state and reset on page refresh. Planned for next milestone. |
| **Free AI tier limits** | Gemini and Groq free tiers are suited to demo and prototyping workloads, not sustained production traffic. |
| **Bundle size advisory** | The Recharts dependency triggers Vite's >500 kB chunk warning. This is harmless for local use; code-split before deploying publicly. |
| **Retrieval coverage** | OpenAlex and arXiv are comprehensive but not exhaustive — some fields (clinical medicine, proprietary research) have uneven coverage. |
| **Gap quality variance** | Computed-signal gaps are structurally grounded but less nuanced than LLM synthesis. For higher-stakes use, enable an LLM key. |

---

## Contributing

Contributions, issues, and feature requests are welcome.

### Getting Started

```bash
# Fork and clone
git clone https://github.com/your-username/lacuna.git
cd lacuna

# Create a feature branch
git checkout -b feature/your-feature-name

# Make your changes, then open a pull request
```

### Where Help Is Most Needed

| Area | What's Needed |
|---|---|
| 📸 **Documentation** | Screenshots, GIFs, and a recorded demo walkthrough |
| 💾 **Persistence** | `localStorage` or `/api/store` implementation |
| 🧪 **Tests** | Unit tests for `LiteratureAgent` and `GapAgent` |
| 🎨 **Design** | Dark mode refinements, mobile responsiveness |
| 🔌 **Integrations** | Semantic Scholar, PubMed, or CORE retrieval adapters |

Please open an issue before starting significant work so we can coordinate direction.

---

## Open-Source Launch Checklist

Before public launch, the following are recommended:

- [ ] `LICENSE` file in root (MIT suggested)
- [ ] `CONTRIBUTING.md` with detailed workflow
- [ ] `CODE_OF_CONDUCT.md`
- [ ] `CHANGELOG.md`
- [ ] `.github/ISSUE_TEMPLATE/` (bug report + feature request templates)
- [ ] `.github/PULL_REQUEST_TEMPLATE.md`
- [ ] `.github/workflows/` CI pipeline (lint + test on PR)
- [ ] Demo screenshots in `/docs/assets/`
- [ ] Hosted demo (Render, Railway, or HuggingFace Spaces)
- [ ] Project description + topics set on GitHub repo page
- [ ] PyPI package or Docker image (optional, for wider reach)

---

## License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

<div align="center">

Built for researchers who want to ask better questions, not just find more papers.

<br/>

**[⭐ Star this repo](https://github.com/your-username/lacuna)** if Lacuna helps your research.

</div>
