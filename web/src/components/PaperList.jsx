import { MatchBadge } from "./Bits.jsx";
import { ArrowUpRight } from "lucide-react";

export default function PaperList({ data, onOpen, onSave }) {
  return (
    <div className="panel pad fade-in">
      <div className="section-label">{data.papers.length} papers · “{data.topic}”</div>
      <div style={{ display: "flex", flexDirection: "column", gap: 14 }}>
        {data.papers.map((p, i) => (
          <div className="paper" key={i}>
            <div style={{ display: "flex", gap: 10, alignItems: "start" }}>
              <div className="title" style={{ flex: 1 }}>{p.title}</div>
              <MatchBadge rel={p.relevance} />
            </div>
            <div className="meta">
              {p.author_str} — {p.venue || p.source}, {p.year || "n.d."}
              {p.citations != null ? ` · ${p.citations.toLocaleString()} citations` : " · preprint"}
              {p.is_open_access ? " · open access" : ""}
            </div>
            {p.abstract && <div className="abs">{p.abstract.slice(0, 220)}…</div>}
            <div className="row">
              <button className="btn sm" onClick={() => onOpen(i)}>Read</button>
              <button className="btn sm" onClick={() => onSave(p)}>Save</button>
              {p.url && <a className="btn sm" href={p.url} target="_blank" rel="noreferrer"
                          style={{ marginLeft: "auto", display: "inline-flex", gap: 5, alignItems: "center" }}>
                          Source <ArrowUpRight size={14} /></a>}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
