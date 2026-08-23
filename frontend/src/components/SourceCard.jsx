import { FileText, ExternalLink } from "lucide-react";
export default function SourceCard({ source }) {
  if (!source) return null;
  return <div className="source-card">
    <div className="source-icon"><FileText size={20}/></div>
    <div><strong>{source.name}</strong><small>{source.page ? `Page ${source.page}` : "Source document"}</small>
      {source.excerpt && <p>{source.excerpt}</p>}</div>
    <button type="button" className="source-open"><ExternalLink size={17}/></button>
  </div>;
}