import { Bolt, CloudUpload, MessageSquare, FileUp, Cpu, FileSearch } from "lucide-react";

export default function Home({ setPage }) {
  return <div className="home-page">
    <section className="hero">
      <div className="assistant-badge"><Bolt size={16}/>Knowledge<br className="mobile-only"/> Assistant</div>
      <h1>Unlock the Power of<br/>Your Data</h1>
      <p>Upload your documents and let AI answer your questions using only your secure data. No hallucinations, just factual insights extracted directly from your knowledge base.</p>
      <div className="hero-actions">
        <button className="green-btn" onClick={() => setPage("upload")}><CloudUpload size={20}/>Upload Documents</button>
        <button className="outline-btn" onClick={() => setPage("chat")}><MessageSquare size={20}/>Ask AI</button>
      </div>
    </section>
    <section className="how">
      <h2>How It Works</h2>
      <div className="how-grid">
        <article className="how-card green-card"><div className="how-icon"><FileUp size={27}/></div><h3>1. Upload Context</h3><p>Securely upload PDFs, Word docs, text files, or connect your existing knowledge bases (Notion, Google Drive).</p><FileUp className="watermark"/></article>
        <article className="how-card blue-card"><div className="how-icon"><Cpu size={27}/></div><h3>2. AI Processing</h3><p>Our secure LLMs parse, index, and vectorize your documents, building a high-speed search index tailored to your specific data.</p><Cpu className="watermark"/></article>
        <article className="how-card purple-card"><div className="how-icon"><FileSearch size={27}/></div><h3>3. Ask & Retrieve</h3><p>Ask complex questions in natural language. Get instant, accurate answers with direct citations to your original source files.</p><FileSearch className="watermark"/></article>
      </div>
    </section>
  </div>;
}