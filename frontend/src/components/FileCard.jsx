import { FileText, FileSpreadsheet, Trash2 } from "lucide-react";

export default function FileCard({ file, onDelete }) {
  const Icon = file.type === "CSV" ? FileSpreadsheet : FileText;
  return <div className="library-row">
    <div className="file-type-icon"><Icon size={24}/></div>
    <div className="library-name">{file.name}</div>
    <div className="library-type">{file.type}</div>
    <div className="library-date">{file.date}</div>
    <div><span className={`status-pill ${file.status === "Ready" ? "ready" : "processing"}`}>
      <i/> {file.status}
    </span></div>
    <button className="delete-btn" onClick={() => onDelete?.(file)} type="button"><Trash2 size={21}/></button>
  </div>;
}