import { LayoutDashboard, Telescope, BookMarked } from "lucide-react";

export default function Sidebar({ view, setView, backend, savedCount }) {
  const on = backend && backend !== "none";
  const items = [
    { id: "workspace", label: "Workspace", icon: Telescope },
    { id: "dashboard", label: "Dashboard", icon: LayoutDashboard },
  ];
  return (
    <aside className="sidebar">
      <div className="brand">
        <div className="mark">L</div>
        <div className="name">Lacuna</div>
      </div>
      {items.map(({ id, label, icon: Icon }) => (
        <div key={id} className={`navitem ${view === id ? "active" : ""}`} onClick={() => setView(id)}>
          <Icon size={17} /> {label}
        </div>
      ))}
      <div className="navitem" style={{ cursor: "default" }}>
        <BookMarked size={17} /> Reading list
        <span className="badge" style={{ marginLeft: "auto", background: "var(--surface-2)", color: "var(--muted)" }}>
          {savedCount}
        </span>
      </div>
      <div className="spacer" />
      <span className={`aibadge ${on ? "on" : ""}`}>
        <span className="dot" />
        {on ? `Grounded AI · ${backend}` : "AI off · computed signals"}
      </span>
    </aside>
  );
}
