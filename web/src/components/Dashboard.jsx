import { Clock, BookMarked } from "lucide-react";

export default function Dashboard({ recents, saved, onPick, onUnsave }) {
  return (
    <div className="work" style={{ gridTemplateColumns: "1fr 1fr" }}>
      <div className="col">
        <div className="panel pad">
          <div className="section-label"><Clock size={13} style={{ verticalAlign: "-2px" }} /> Recent topics</div>
          {recents.length === 0 && <div className="muted" style={{ fontSize: 13 }}>Topics you explore appear here.</div>}
          {recents.map((t, i) => (
            <div key={i} className="navitem" onClick={() => onPick(t)} style={{ marginBottom: 4 }}>↻ {t}</div>
          ))}
        </div>
      </div>
      <div className="col">
        <div className="panel pad">
          <div className="section-label"><BookMarked size={13} style={{ verticalAlign: "-2px" }} /> Reading list · {saved.length}</div>
          {saved.length === 0 && <div className="muted" style={{ fontSize: 13 }}>Save papers from the workspace.</div>}
          {saved.map((p, i) => (
            <div className="paper" key={i} style={{ marginBottom: 10 }}>
              <div className="title" style={{ fontSize: 14 }}>{p.title}</div>
              <div className="meta">{p.venue || p.source}, {p.year || "n.d."}</div>
              <div className="row"><button className="btn sm" onClick={() => onUnsave(i)}>Remove</button></div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
