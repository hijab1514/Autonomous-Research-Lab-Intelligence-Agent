"""
agents/gap_agent.py — Research Gap & Direction engine.

This is the product's reason to exist. Google Scholar finds papers; this reads
the top relevance-gated papers for a topic and reasons about what is THIN,
STAGNATING, CONTRADICTED, or NEVER COMBINED — then proposes concrete research
directions a student or researcher could actually pursue.

Two modes, identical output shape so the UI never branches:
  • LLM mode (free backend via research_llm) — reasons across the corpus.
  • Extractive mode (no key, no network beyond the search itself) — derives
    gaps from measurable signals (coverage, recency, citations, venue spread).

ANTI-HALLUCINATION (the honest part): in LLM mode every gap must cite specific
papers from the provided set by index. Gaps that cite nothing real are dropped.
The model reasons only over abstracts we actually pass it — it cannot invent a
paper, because we validate every citation against the input list.
"""

from __future__ import annotations

import logging
import re
from collections import Counter
from dataclasses import dataclass, field
from typing import Any

from agents.research_llm import ResearchLLM, extract_json

logger = logging.getLogger(__name__)

_STOP = {
    "the", "a", "an", "of", "for", "and", "or", "to", "in", "on", "with", "using",
    "based", "via", "by", "from", "at", "is", "are", "study", "approach", "method",
    "methods", "analysis", "system", "systems", "model", "models", "new", "novel",
    "paper", "research", "towards", "toward", "use", "used", "data", "results",
    "we", "this", "our", "their", "these", "that", "can", "such", "more", "than",
}

GAP_TYPES = ("underexplored", "stagnation", "contradiction", "methodological", "replication")


def _toks(text: str) -> list[str]:
    return [t for t in re.findall(r"[a-z0-9]+", (text or "").lower())
            if len(t) >= 3 and t not in _STOP]


@dataclass
class Gap:
    title: str
    rationale: str
    gap_type: str = "underexplored"
    evidence_idx: list[int] = field(default_factory=list)   # 1-based into the paper list
    confidence: float = 0.5

    def evidence_titles(self, papers: list) -> list[str]:
        out = []
        for i in self.evidence_idx:
            if 1 <= i <= len(papers):
                out.append(getattr(papers[i - 1], "title", f"[{i}]"))
        return out


@dataclass
class Direction:
    question: str
    why: str = ""
    related_gap: str = ""


@dataclass
class GapReport:
    topic: str
    backend: str                       # gemini | groq | ollama | extractive
    field_summary: str
    gaps: list[Gap] = field(default_factory=list)
    directions: list[Direction] = field(default_factory=list)

    @property
    def is_ai(self) -> bool:
        return self.backend in ("gemini", "groq", "ollama")

    def to_markdown(self, papers: list | None = None) -> str:
        papers = papers or []
        tag = f"AI synthesis ({self.backend})" if self.is_ai else "Computed signals (no LLM)"
        out = [f"# Research gaps: {self.topic}".rstrip(), f"_{tag}_", "",
               "## State of the field", self.field_summary or "—", "", "## Gaps", ""]
        for i, g in enumerate(self.gaps, 1):
            out.append(f"### {i}. {g.title}  ·  `{g.gap_type}`  ·  confidence {g.confidence:.2f}")
            out.append(g.rationale)
            ev = g.evidence_titles(papers)
            if ev:
                out.append("\n**Grounded in:**")
                out += [f"- {t}" for t in ev]
            out.append("")
        if self.directions:
            out += ["## Suggested directions", ""]
            for i, d in enumerate(self.directions, 1):
                out.append(f"{i}. **{d.question}**" + (f"  \n   {d.why}" if d.why else ""))
        return "\n".join(out)


class GapAgent:
    def __init__(self, llm: ResearchLLM | None = None, max_papers: int = 25,
                 abstract_chars: int = 480) -> None:
        self.llm = llm or ResearchLLM()
        self.max_papers = max_papers
        self.abstract_chars = abstract_chars

    @property
    def backend(self) -> str:
        return self.llm.backend if self.llm.available() else "extractive"

    # ---- main entry -------------------------------------------------------- #
    def analyze(self, topic: str, papers: list, briefing: dict | None = None) -> GapReport:
        papers = list(papers or [])
        if not papers:
            return GapReport(topic=topic, backend=self.backend,
                             field_summary="No papers to analyze.")
        if self.llm.available():
            report = self._llm_report(topic, papers)
            if report and report.gaps:        # only trust it if grounded gaps survived
                return report
            logger.info("LLM gap analysis empty/failed — using extractive fallback")
        return self._extractive_report(topic, papers, briefing or {})

    # ---- LLM mode (grounded) ---------------------------------------------- #
    def _context(self, papers: list) -> str:
        rows = []
        for i, p in enumerate(papers[:self.max_papers], 1):
            cites = getattr(p, "citations", None)
            cite_s = f"{cites} cites" if cites is not None else "preprint"
            rows.append(
                f"[{i}] {getattr(p,'title','')} ({getattr(p,'year','n.d.')}, "
                f"{getattr(p,'venue','') or 'n/a'}, {cite_s})\n"
                f"    {(getattr(p,'abstract','') or '')[:self.abstract_chars]}"
            )
        return "\n".join(rows)

    def _llm_report(self, topic: str, papers: list) -> GapReport | None:
        sys = ("You are a rigorous research analyst. You identify gaps ONLY from the "
               "papers provided. You never invent papers or findings. Every gap must "
               "reference the bracketed indices of the papers that justify it.")
        prompt = f"""Topic: "{topic}"

Below are the top papers (numbered). Reason ACROSS them and return STRICT JSON only:

{{
  "field_summary": "3-4 sentences on the current state of the field, grounded in these papers",
  "gaps": [
    {{
      "title": "short gap title",
      "rationale": "2-3 sentences. Cite evidence by paper number.",
      "gap_type": "one of: {' | '.join(GAP_TYPES)}",
      "evidence": [paper numbers that support this gap],
      "confidence": 0.0-1.0
    }}
  ],
  "directions": [
    {{"question": "a concrete, testable research question a student could pursue",
      "why": "1 sentence on why it is promising / underexplored",
      "related_gap": "title of the gap it addresses"}}
  ]
}}

Rules: 3-5 gaps, 3-5 directions. Every gap's "evidence" must list at least one
real paper number from the list. Do not propose a gap you cannot ground. No prose
outside the JSON.

Papers:
{self._context(papers)}"""

        raw = self.llm.complete(prompt, system=sys)
        data = extract_json(raw or "")
        if not isinstance(data, dict):
            return None

        n = len(papers)
        gaps: list[Gap] = []
        for g in (data.get("gaps") or []):
            idx = [int(x) for x in (g.get("evidence") or []) if str(x).strip().lstrip("-").isdigit()]
            idx = [i for i in idx if 1 <= i <= n]          # validate against real papers
            if not idx:
                continue                                    # drop ungrounded gap
            gtype = g.get("gap_type", "underexplored")
            gaps.append(Gap(
                title=str(g.get("title", "Untitled gap"))[:120],
                rationale=str(g.get("rationale", "")),
                gap_type=gtype if gtype in GAP_TYPES else "underexplored",
                evidence_idx=idx,
                confidence=_clamp(g.get("confidence", 0.5)),
            ))
        dirs = [Direction(question=str(d.get("question", "")), why=str(d.get("why", "")),
                          related_gap=str(d.get("related_gap", "")))
                for d in (data.get("directions") or []) if d.get("question")]
        return GapReport(topic=topic, backend=self.backend,
                         field_summary=str(data.get("field_summary", "")),
                         gaps=gaps[:5], directions=dirs[:5])

    # ---- extractive mode (no LLM) ----------------------------------------- #
    def _extractive_report(self, topic: str, papers: list, brief: dict) -> GapReport:
        years = [getattr(p, "year", None) for p in papers if getattr(p, "year", None)]
        cited = [getattr(p, "citations", None) for p in papers if getattr(p, "citations", None)]
        oa_pct = brief.get("open_access_pct")
        if oa_pct is None and papers:
            oa_pct = round(100 * sum(bool(getattr(p, "is_open_access", False)) for p in papers) / len(papers))

        # term frequency across the corpus (excluding query words)
        q = set(_toks(topic))
        tf = Counter()
        per_term_papers: dict[str, list[int]] = {}
        for i, p in enumerate(papers, 1):
            seen = set(_toks(getattr(p, "title", "")) + _toks(getattr(p, "abstract", "")))
            for t in seen:
                if t not in q:
                    tf[t] += 1
                    per_term_papers.setdefault(t, []).append(i)

        gaps: list[Gap] = []
        # 1) stagnation
        if years and max(years) <= 2022:
            recent = [i for i, p in enumerate(papers, 1) if (getattr(p, "year", 0) or 0) >= max(years) - 1]
            gaps.append(Gap("Possible stagnation", f"Newest strong work is {max(years)}; "
                            "little recent activity suggests the area may be cooling or ripe for revival.",
                            "stagnation", recent[:4] or [1], 0.55))
        # 2) access / reproducibility
        if oa_pct is not None and oa_pct < 40:
            closed = [i for i, p in enumerate(papers, 1) if not getattr(p, "is_open_access", False)]
            gaps.append(Gap("Access & reproducibility gap", f"Only {oa_pct}% of top work is open access, "
                            "limiting verification and reuse — an opening for open, reproducible contributions.",
                            "methodological", closed[:4] or [1], 0.5))
        # 3) early-stage
        if cited:
            med = sorted(cited)[len(cited) // 2]
            if med < 10:
                gaps.append(Gap("Early-stage / unconsolidated", f"Median citations are low ({med}); "
                                "the area lacks consolidating work — survey or benchmark contributions could anchor it.",
                                "underexplored", list(range(1, min(4, len(papers)) + 1)), 0.5))
        # 4) niche sub-themes mentioned by only one paper (underexplored angles)
        niche = [(t, ps[0]) for t, ps in per_term_papers.items() if len(ps) == 1 and tf[t] == 1]
        niche.sort()
        for t, pi in niche[:2]:
            gaps.append(Gap(f"Underexplored angle: “{t}”",
                            f"“{t}” appears in only one of the top papers — a thin thread that may be "
                            "underexplored relative to the core of the field.",
                            "underexplored", [pi], 0.4))
        if not gaps:
            gaps.append(Gap("Well-covered area", "Strong, recent, well-cited and largely open work is present; "
                            "differentiation will require a sharper sub-question.", "underexplored",
                            list(range(1, min(3, len(papers)) + 1)), 0.4))

        themes = [t for t, _ in tf.most_common(8)]
        summary = (f"Across {len(papers)} top papers"
                   + (f" ({min(years)}–{max(years)})" if years else "")
                   + ", recurring themes include " + ", ".join(themes[:6]) + "."
                   + (f" About {oa_pct}% are open access." if oa_pct is not None else ""))
        dirs = [Direction(f"Can {g.title.lower().replace('possible ','').replace('underexplored angle: ','work on ')} "
                          f"be turned into a focused study in {topic}?",
                          "Derived from a measurable signal in the result set.", g.title)
                for g in gaps[:3]]
        return GapReport(topic=topic, backend="extractive", field_summary=summary,
                         gaps=gaps[:5], directions=dirs)


def _clamp(x: Any) -> float:
    try:
        return max(0.0, min(1.0, float(x)))
    except Exception:
        return 0.5
