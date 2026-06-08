import { MatchBadge } from "./Bits.jsx";
import { ArrowLeft } from "lucide-react";

export default function PaperDetail({ p, onBack, onSave }) {
  return (
    <div className="panel pad fade-in">
      <button className="btn sm" onClick={onBack} style={{ display: "inline-flex", gap: 6, alignItems: "center" }}>
        <ArrowLeft size={14} /> Back to results
      </button>
      <h2 style={{ fontSize: 22, margin: "16px 0 8px", lineHeight: 1.3 }}>{p.title}</h2>
      <div className="meta">
        {p.author_str} — {p.venue || p.source}, {p.year || "n.d."}
        {p.citations != null ? ` · ${p.citations.toLocaleString()} citations` : " · preprint"}
      </div>
      <div style={{ margin: "12px 0" }}><MatchBadge rel={p.relevance} /></div>
      <p style={{ lineHeight: 1.65, color: "var(--text)" }}>{p.abstract || "No abstract available."}</p>
      <div className="row" style={{ marginTop: 8 }}>
        <button className="btn primary sm" onClick={() => onSave(p)}>＋ Save to reading list</button>
        {p.url && <a className="btn sm" href={p.url} target="_blank" rel="noreferrer">Source</a>}
        {p.pdf_url && <a className="btn sm" href={p.pdf_url} target="_blank" rel="noreferrer">PDF</a>}
      </div>
    </div>
  );
}
