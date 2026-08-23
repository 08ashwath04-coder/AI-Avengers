import { Box, LayoutDashboard, CloudUpload, FolderOpen, MessageSquare, X } from "lucide-react";

const links = [
  ["home","Home",LayoutDashboard],
  ["upload","Upload",CloudUpload],
  ["library","Library",FolderOpen],
  ["chat","Chat",MessageSquare]
];

export default function Sidebar({ page, setPage, mobileOpen, closeMobile }) {
  return <>
    {mobileOpen && <div className="mobile-overlay" onClick={closeMobile}/>}
    <aside className={`sidebar ${mobileOpen ? "mobile-visible" : ""}`}>
      <div className="sidebar-inner">
        <div className="sidebar-brand">
          <span className="logo-box"><Box size={23}/></span>
          <span>AI Avengers</span>
        </div>
        <button className="close-sidebar" onClick={closeMobile} type="button"><X size={21}/></button>
        <nav className="side-nav">
          {links.map(([id,label,Icon]) => (
            <button key={id} onClick={() => {setPage(id); closeMobile();}}
              className={`side-link ${page === id ? "selected" : ""}`} type="button">
              <Icon size={21}/><span>{label}</span>
            </button>
          ))}
        </nav>
      </div>
      <div className="sidebar-user">
        <div className="user-photo">A</div>
        <div><strong>Alex Mercer</strong><span>Admin</span></div>
      </div>
    </aside>
  </>;
}