// Left panel: the search refinements.
export default function Filters({ f, setF }) {
  const set = (k) => (e) => {
    const v = e.target.type === "checkbox" ? e.target.checked
      : e.target.type === "number" || e.target.type === "range" ? Number(e.target.value)
      : e.target.value;
    setF({ ...f, [k]: v });
  };
  return (
    <div className="panel pad">
      <div className="section-label">Refine</div>
      <div className="field">
        <label>Source</label>
        <select value={f.source} onChange={set("source")}>
          <option value="journals">Journals</option>
          <option value="both">Journals + arXiv</option>
          <option value="preprints">arXiv</option>
        </select>
      </div>
      <div className="field">
        <label>Rank by</label>
        <select value={f.sort} onChange={set("sort")}>
          <option value="best">Best match</option>
          <option value="citations">Most cited</option>
          <option value="recent">Newest</option>
        </select>
      </div>
      <div className="field">
        <label>On-topic strictness · {f.strictness.toFixed(2)}</label>
        <input type="range" min="0.25" max="0.85" step="0.05" value={f.strictness} onChange={set("strictness")} />
      </div>
      <div className="field">
        <label>From year (0 = any)</label>
        <input type="number" min="0" max="2026" value={f.year_from} onChange={set("year_from")} />
      </div>
      <div className="field">
        <label>Min citations</label>
        <input type="number" min="0" step="10" value={f.min_citations} onChange={set("min_citations")} />
      </div>
      <div className="field switch">
        <label style={{ margin: 0 }}>Open access only</label>
        <input type="checkbox" checked={f.open_access_only} onChange={set("open_access_only")} />
      </div>
      <div className="field">
        <label>Results · {f.limit}</label>
        <input type="range" min="5" max="40" step="5" value={f.limit} onChange={set("limit")} />
      </div>
    </div>
  );
}
