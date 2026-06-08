"""
server/main.py — Lacuna API (FastAPI).

A thin HTTP layer over the SAME engine the Streamlit build used:
  agents/literature_agent.py  — relevance-gated retrieval (OpenAlex + arXiv)
  agents/research_llm.py       — free LLM layer (Gemini / Groq / Ollama / none)
  agents/gap_agent.py          — grounded gap & direction engine

Endpoints:
  GET  /api/health            -> { llm_backend }
  POST /api/analyze           -> { papers, briefing, gaps, directions }

Run:  uvicorn server.main:app --reload --port 8000   (from project root)
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def _load_env() -> None:
    f = ROOT / ".env"
    if not f.exists():
        return
    for line in f.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            k, v = k.strip(), v.strip().strip('"').strip("'")
            if k and v and k not in os.environ:
                os.environ[k] = v


_load_env()

from fastapi import FastAPI  # noqa: E402
from fastapi.middleware.cors import CORSMiddleware  # noqa: E402
from pydantic import BaseModel  # noqa: E402

from agents.literature_agent import LiteratureAgent, Paper  # noqa: E402
from agents.research_llm import ResearchLLM  # noqa: E402
from agents.gap_agent import GapAgent  # noqa: E402

app = FastAPI(title="Lacuna API", version="1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["*"], allow_headers=["*"],
)


class AnalyzeRequest(BaseModel):
    topic: str
    limit: int = 15
    source: str = "journals"
    sort: str = "best"
    year_from: int | None = None
    open_access_only: bool = False
    min_citations: int = 0
    strictness: float = 0.45


def _paper_dict(p: Paper) -> dict:
    return {
        "title": p.title, "authors": p.authors, "author_str": p.author_str,
        "year": p.year, "venue": p.venue, "citations": p.citations,
        "abstract": p.abstract, "url": p.url, "pdf_url": p.pdf_url,
        "is_open_access": p.is_open_access, "source": p.source,
        "relevance": round(p.relevance, 3),
    }


@app.get("/api/health")
def health() -> dict:
    return {"llm_backend": ResearchLLM().backend}


@app.post("/api/analyze")
def analyze(req: AnalyzeRequest) -> dict:
    lit = LiteratureAgent()
    papers = lit.find_top_papers(
        topic=req.topic, limit=req.limit, source=req.source, sort=req.sort,
        year_from=req.year_from, open_access_only=req.open_access_only,
        min_citations=req.min_citations, strictness=req.strictness)

    briefing = lit.field_briefing(papers, req.topic) if papers else {}
    # field_briefing returns Paper objects for seminal/newest; trim to safe fields
    if briefing.get("seminal"):
        briefing["seminal"] = {"title": briefing["seminal"].title,
                               "citations": briefing["seminal"].citations,
                               "year": briefing["seminal"].year}
    if briefing.get("newest"):
        briefing["newest"] = {"title": briefing["newest"].title, "year": briefing["newest"].year}

    report = GapAgent().analyze(req.topic, papers)
    gaps = [{
        "title": g.title, "rationale": g.rationale, "type": g.gap_type,
        "confidence": round(g.confidence, 2), "evidence": g.evidence_titles(papers),
    } for g in report.gaps]
    directions = [{"question": d.question, "why": d.why, "related_gap": d.related_gap}
                  for d in report.directions]

    return {
        "topic": req.topic,
        "papers": [_paper_dict(p) for p in papers],
        "briefing": briefing,
        "gap_backend": report.backend,
        "is_ai": report.is_ai,
        "field_summary": report.field_summary,
        "gaps": gaps,
        "directions": directions,
    }
