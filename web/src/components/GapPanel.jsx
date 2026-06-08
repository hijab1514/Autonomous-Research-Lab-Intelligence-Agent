import { GapTypeBadge } from "./Bits.jsx";
import { BarChart, Bar, ResponsiveContainer, XAxis, Tooltip } from "recharts";

export default function GapPanel({ data }) {
  const years = {};
  data.papers.forEach((p) => { if (p.year) years[p.year] = (years[p.year] || 0) + 1; });
  const chart = Object.entries(years).map(([year, papers]) => ({ year, papers })).sort((a, b) => a.year - b.year);
  const b = data.briefing || {};

  return (
    <>
      <div className="panel pad fade-in">
        <div className="section-label">State of the field</div>
        <span className="badge" style={{
          background: data.is_ai ? "rgba(70,211,154,0.18)" : "var(--surface-2)",
          color: data.is_ai ? "var(--good)" : "var(--muted)" }}>
          {data.is_ai ? `AI · ${data.gap_backend}` : "computed signals"}
        </span>
        <p className="muted" style={{ fontSize: 13.5, lineHeight: 1.55, marginTop: 10, marginBottom: 0 }}>
          {data.field_summary}
        </p>
      </div>

      <div className="panel pad">
        <div className="section-label">Research gaps</div>
        {data.gaps.length === 0 && <div className="muted" style={{ fontSize: 13 }}>No clear gaps surfaced.</div>}
        {data.gaps.map((g, i) => (
          <div className="gap" key={i}>
            <div style={{ display: "flex", gap: 8, alignItems: "center" }}>
              <GapTypeBadge type={g.type} />
              <span className="faint" style={{ fontSize: 12 }}>confidence {g.confidence.toFixed(2)}</span>
            </div>
            <div className="gtitle">{g.title}</div>
            <div className="gtext">{g.rationale}</div>
            {g.evidence?.length > 0 && (
              <details>
                <summary>Grounded in {g.evidence.length} paper(s)</summary>
                <ul>{g.evidence.map((t, j) => <li key={j}>{t}</li>)}</ul>
              </details>
            )}
          </div>
        ))}
        {data.is_ai && <div className="faint" style={{ fontSize: 11.5, marginTop: 4 }}>
          Every gap cites real papers above; ungrounded claims are dropped.</div>}
      </div>

      {data.directions?.length > 0 && (
        <div className="panel pad">
          <div className="section-label">Suggested directions</div>
          {data.directions.map((d, i) => (
            <div className="dir" key={i}>
              <div className="q">{d.question}</div>
              {d.why && <div className="why">{d.why}</div>}
            </div>
          ))}
        </div>
      )}

      <div className="panel pad">
        <div className="section-label">Themes & trends</div>
        <div style={{ marginBottom: chart.length ? 14 : 0 }}>
          {(b.themes || []).slice(0, 10).map((t, i) => <span className="chip" key={i}>{t}</span>)}
        </div>
        {chart.length > 0 && (
          <ResponsiveContainer width="100%" height={130}>
            <BarChart data={chart}>
              <XAxis dataKey="year" tick={{ fill: "var(--faint)", fontSize: 11 }} axisLine={false} tickLine={false} />
              <Tooltip cursor={{ fill: "rgba(255,255,255,0.04)" }}
                contentStyle={{ background: "var(--ink-2)", border: "1px solid var(--border)", borderRadius: 8, fontSize: 12 }} />
              <Bar dataKey="papers" fill="var(--accent)" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        )}
      </div>
    </>
  );
}
