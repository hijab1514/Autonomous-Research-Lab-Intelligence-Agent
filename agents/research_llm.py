"""
agents/research_llm.py — free, swappable LLM layer.

The whole product can run with NO paid API. This picks whatever free backend is
available, in order, and degrades to None (caller falls back to extractive mode)
if nothing is configured:

    1. Gemini (Google AI Studio)  — set GEMINI_API_KEY (or GOOGLE_API_KEY).
       Best free tier: large context, generous daily quota, no card.
    2. Groq                       — set GROQ_API_KEY. Fast Llama, free tier.
    3. Ollama (local)             — runs at http://localhost:11434, no key, no limit.
    4. None                       — no LLM; caller uses the extractive path.

Force one with RESEARCH_LLM_PROVIDER = gemini | groq | ollama | none.

Pure standard library (urllib). No SDKs, no torch — runs on a locked-down machine.
HTTP is injectable (`transport=`) so the logic is unit-testable without keys.
"""

from __future__ import annotations

import json
import logging
import os
import urllib.request
from typing import Callable

logger = logging.getLogger(__name__)

GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}"
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_TAGS = "http://localhost:11434/api/tags"

# Defaults overridable by env. Gemini 2.5 Flash is the strongest free model;
# if your account doesn't have it, set GEMINI_MODEL=gemini-2.0-flash.
DEF_GEMINI = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
DEF_GROQ = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
DEF_OLLAMA = os.getenv("OLLAMA_MODEL", "llama3.2")


def _post(url: str, payload: dict, headers: dict, timeout: float) -> str:
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json", **headers})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8", errors="replace")


def _ollama_up(timeout: float = 1.5) -> bool:
    try:
        req = urllib.request.Request(OLLAMA_TAGS)
        with urllib.request.urlopen(req, timeout=timeout):
            return True
    except Exception:
        return False


class ResearchLLM:
    """A single .complete(prompt) call over whichever free backend is available."""

    def __init__(
        self,
        provider: str | None = None,
        model: str | None = None,
        transport: Callable[[str, dict, dict, float], str] = _post,
        timeout: float = 60.0,
        ollama_probe: Callable[[], bool] = _ollama_up,
    ) -> None:
        self._post = transport
        self._timeout = timeout
        self._probe = ollama_probe
        self._model = model

        forced = (provider or os.getenv("RESEARCH_LLM_PROVIDER") or "").strip().lower()
        if forced in ("gemini", "groq", "ollama", "none"):
            self._provider = forced
        else:
            self._provider = self._auto_detect()

        self._gemini_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY") or ""
        self._groq_key = os.getenv("GROQ_API_KEY") or ""
        logger.info("ResearchLLM provider=%s model=%s", self._provider, self.model)

    # ---- selection -------------------------------------------------------- #
    def _auto_detect(self) -> str:
        if os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY"):
            return "gemini"
        if os.getenv("GROQ_API_KEY"):
            return "groq"
        if self._probe():
            return "ollama"
        return "none"

    @property
    def backend(self) -> str:
        return self._provider

    @property
    def model(self) -> str:
        if self._model:
            return self._model
        return {"gemini": DEF_GEMINI, "groq": DEF_GROQ, "ollama": DEF_OLLAMA}.get(self._provider, "—")

    def available(self) -> bool:
        return self._provider != "none"

    # ---- one completion --------------------------------------------------- #
    def complete(self, prompt: str, system: str | None = None) -> str | None:
        """Return model text, or None on any failure (caller then degrades)."""
        try:
            if self._provider == "gemini":
                return self._gemini(prompt, system)
            if self._provider == "groq":
                return self._groq(prompt, system)
            if self._provider == "ollama":
                return self._ollama(prompt, system)
        except Exception as exc:
            logger.warning("LLM call failed (%s): %s", self._provider, exc)
        return None

    def _gemini(self, prompt: str, system: str | None) -> str | None:
        if not self._gemini_key:
            return None
        url = GEMINI_URL.format(model=self.model, key=self._gemini_key)
        payload: dict = {"contents": [{"parts": [{"text": prompt}]}]}
        if system:
            payload["systemInstruction"] = {"parts": [{"text": system}]}
        raw = self._post(url, payload, {}, self._timeout)
        data = json.loads(raw)
        return data["candidates"][0]["content"]["parts"][0]["text"]

    def _groq(self, prompt: str, system: str | None) -> str | None:
        if not self._groq_key:
            return None
        msgs = ([{"role": "system", "content": system}] if system else []) + \
               [{"role": "user", "content": prompt}]
        payload = {"model": self.model, "messages": msgs, "temperature": 0.3}
        raw = self._post(GROQ_URL, payload, {"Authorization": f"Bearer {self._groq_key}"}, self._timeout)
        return json.loads(raw)["choices"][0]["message"]["content"]

    def _ollama(self, prompt: str, system: str | None) -> str | None:
        payload = {"model": self.model, "prompt": prompt, "stream": False}
        if system:
            payload["system"] = system
        raw = self._post(OLLAMA_URL, payload, {}, self._timeout)
        return json.loads(raw)["response"]


def extract_json(text: str):
    """Pull the first JSON object/array out of a model response (tolerates fences/prose)."""
    if not text:
        return None
    t = text.strip()
    if t.startswith("```"):
        t = t.split("```")[1]
        if t.lstrip().startswith("json"):
            t = t.lstrip()[4:]
    # find the outermost { } or [ ]
    for open_c, close_c in (("{", "}"), ("[", "]")):
        i, j = t.find(open_c), t.rfind(close_c)
        if 0 <= i < j:
            try:
                return json.loads(t[i:j + 1])
            except Exception:
                continue
    try:
        return json.loads(t)
    except Exception:
        return None
