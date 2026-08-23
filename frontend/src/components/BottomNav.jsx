import { LayoutDashboard, CloudUpload, FolderOpen, MessageSquare } from "lucide-react";

export default function BottomNav({ page, setPage }) {
  const items = [["home","Home",LayoutDashboard],["upload","Upload",CloudUpload],["library","Library",FolderOpen],["chat","Chat",MessageSquare]];
  return <nav className="bottom-nav">{items.map(([id,label,Icon]) =>
    <button key={id} className={page === id ? "active" : ""} onClick={() => setPage(id)} type="button">
      <Icon size={20}/><span>{label}</span>
    </button>
  )}</nav>;
}