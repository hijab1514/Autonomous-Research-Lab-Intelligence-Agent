import { useEffect, useState } from "react";
import Sidebar from "./components/Sidebar.jsx";
import Filters from "./components/Filters.jsx";
import PaperList from "./components/PaperList.jsx";
import PaperDetail from "./components/PaperDetail.jsx";
import GapPanel from "./components/GapPanel.jsx";
import Dashboard from "./components/Dashboard.jsx";
import { Spinner } from "./components/Bits.jsx";
import { analyze, getHealth } from "./api.js";

const DEFAULTS = {
  source: "journals", sort: "best", strictness: 0.45,
  year_from: 0, min_citations: 0, open_access_only: false, limit: 15,
};

export default function App() {
  const [view, setView] = useState("workspace");
  const [backend, setBackend] = useState(null);
  const [topic, setTopic] = useState("");
  const [filters, setFilters] = useState(DEFAULTS);
  const [data, setData] = useState(null);
  const [selected, setSelected] = useState(null);
  const [loading, setLoading] = useState(false);
  const [err, setErr] = useState("");
  const [recents, setRecents] = useState([]);
  const [saved, setSaved] = useState([]);

  useEffect(() => { getHealth().then((h) => setBackend(h.llm_backend)).catch(() => setBackend("none")); }, []);

  async function run(t) {
    const q = (t ?? topic).trim();
    if (!q) return;
    setTopic(q); setLoading(true); setErr(""); setSelected(null);
    setRecents((r) => [q, ...r.filter((x) => x !== q)].slice(0, 8));
    try {
      const params = { topic: q, ...filters, year_from: filters.year_from || null };
      setData(await analyze(params));
    } catch (e) {
      setErr(String(e.message || e)); setData(null);
    } finally { setLoading(false); }
  }

  function save(p) { setSaved((s) => (s.some((x) => x.title === p.title) ? s : [...s, p])); }

  return (
    <div className="shell">
      <Sidebar view={view} setView={setView} backend={backend} savedCount={saved.length} />
      <div className="main">
        <div className="topbar">
          <div className="kicker">Lacuna · Research gap finder</div>
          <h1>{view === "workspace" ? "Gap intelligence" : "Dashboard"}</h1>
        </div>

        {view === "workspace" && (
          <>
            <div className="searchbar">
              <input value={topic} onChange={(e) => setTopic(e.target.value)}
                     onKeyDown={(e) => e.key === "Enter" && run()}
                     placeholder="A research topic — e.g. aircraft defect detection" />
              <button className="btn primary" onClick={() => run()} disabled={loading}>
                {loading ? <Spinner label="Mapping…" /> : "Explore"}
              </button>
            </div>

            <div className="work">
              <div className="col"><Filters f={filters} setF={setFilters} /></div>

              <div className="col">
                {err && <div className="panel pad" style={{ color: "var(--bad)" }}>Search failed: {err}</div>}
                {!data && !err && (
                  <div className="panel pad empty">
                    <div>
                      <div className="big">Start exploring</div>
                      <div className="muted" style={{ maxWidth: 380 }}>
                        Lacuna pulls the top relevance-gated papers, then maps the gaps in the panel on the right.
                      </div>
                    </div>
                  </div>
                )}
                {data && selected != null && (
                  <PaperDetail p={data.papers[selected]} onBack={() => setSelected(null)} onSave={save} />
                )}
                {data && selected == null && (
                  <PaperList data={data} onOpen={setSelected} onSave={save} />
                )}
              </div>

              <div className="col">
                {!data && <div className="panel pad"><div className="section-label">Gap intelligence</div>
                  <div className="muted" style={{ fontSize: 13 }}>The field map appears after a search.</div></div>}
                {data && <GapPanel data={data} />}
              </div>
            </div>
          </>
        )}

        {view === "dashboard" && (
          <Dashboard recents={recents} saved={saved}
                     onPick={(t) => { setView("workspace"); run(t); }}
                     onUnsave={(i) => setSaved((s) => s.filter((_, j) => j !== i))} />
        )}
      </div>
    </div>
  );
}
