import { useRef, useState } from "react";
import { CloudUpload, FileText, CheckCircle, X } from "lucide-react";

export default function Upload({ setPage }) {
  const input = useRef(null);
  const [files,setFiles] = useState([
    {name:"Q3_Financials.pdf", meta:"Extracting tables...", progress:45, processing:true},
    {name:"Policy_Manual.docx", meta:"Added just now • 2.4 MB", progress:100},
    {name:"Old_Notes.txt", meta:"Added yesterday • 12 KB", progress:100}
  ]);
  const addFiles = e => setFiles(p => [...p, ...Array.from(e.target.files).map(f => ({name:f.name,meta:`Added just now • ${(f.size/1024/1024).toFixed(1)} MB`,progress:100}))]);

  return <div className="page upload-page">
    <div className="page-title"><h1>Upload Documents</h1><p>Enhance the AI's knowledge base by providing new context files.</p></div>
    <section className="drop-zone" onClick={() => input.current?.click()}>
      <input ref={input} type="file" hidden multiple accept=".pdf,.ppt,.pptx,.doc,.docx,.txt" onChange={addFiles}/>
      <div className="upload-round"><CloudUpload size={38}/></div>
      <h3>Tap or drag files here</h3>
      <p>Supports PDF, PPT, DOCX, TXT up to 50MB</p>
      <button className="green-btn compact" type="button">Browse Files</button>
    </section>
    <h2 className="section-label">PROCESSING & READY</h2>
    <div className="upload-list">{files.map((f,i) =>
      <div className="upload-row" key={f.name+i}>
        <div className="file-type-icon"><FileText size={23}/></div>
        <div className="upload-info"><strong>{f.name}</strong><span>{f.meta}</span>{f.processing && <div className="progress"><i style={{width:`${f.progress}%`}}/></div>}</div>
        {f.processing ? <b className="progress-text">{f.progress}%</b> : <CheckCircle className="ready-check" size={25}/>}
        <button className="upload-remove" onClick={() => setFiles(p=>p.filter((_,x)=>x!==i))} type="button"><X size={18}/></button>
      </div>)}</div>
    <button className="outline-btn bottom-action" onClick={() => setPage("library")}>View Document Library</button>
  </div>;
}