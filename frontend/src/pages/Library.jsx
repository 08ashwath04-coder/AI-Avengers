import { Search, SlidersHorizontal } from "lucide-react";
import { useState } from "react";
import { documents } from "../data/mockData";
import FileCard from "../components/FileCard";

export default function Library() {
  const [items,setItems] = useState(documents);
  const [query,setQuery] = useState("");
  const filtered = items.filter(x => x.name.toLowerCase().includes(query.toLowerCase()) || x.type.toLowerCase().includes(query.toLowerCase()));
  return <div className="page library-page">
    <div className="page-title"><h1>Document Library</h1><p>Manage and search through your uploaded knowledge base.</p></div>
    <div className="library-search"><Search size={25}/><input value={query} onChange={e=>setQuery(e.target.value)} placeholder="Search documents by name, type, or content..."/><button type="button"><SlidersHorizontal size={22}/></button></div>
    <div className="table-head"><span>FILE NAME</span><span>TYPE</span><span>UPLOAD DATE</span><span>STATUS</span><span>ACTION</span></div>
    <div className="library-list">{filtered.map(f => <FileCard key={f.id} file={f} onDelete={x=>setItems(p=>p.filter(y=>y.id!==x.id))}/>)}</div>
  </div>;
}