// Small shared presentational helpers.
export function MatchBadge({ rel }) {
  const pct = Math.round((rel || 0) * 100);
  const c = rel >= 0.66 ? "var(--good)" : rel >= 0.45 ? "var(--warn)" : "var(--bad)";
  return <span className="badge" style={{ background: `${c}22`, color: c }}>{pct}% match</span>;
}

const GAP_C = {
  underexplored: "var(--accent)", stagnation: "var(--warn)",
  contradiction: "var(--bad)", methodological: "var(--violet)", replication: "var(--good)",
};
export function GapTypeBadge({ type }) {
  const c = GAP_C[type] || "var(--accent)";
  return <span className="badge" style={{ background: `${c}22`, color: c }}>{type}</span>;
}

export function Spinner({ label }) {
  return (
    <span style={{ display: "inline-flex", gap: 9, alignItems: "center", color: "var(--muted)" }}>
      <span className="spinner" /> {label}
    </span>
  );
}
