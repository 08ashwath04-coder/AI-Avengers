import { useRef, useState } from "react";
import { Bot, Send, Paperclip, Plus, User } from "lucide-react";
import { messages as initial } from "../data/mockData";
import SourceCard from "../components/SourceCard";

export default function Chat() {
  const [msgs,setMsgs]=useState(initial), [q,setQ]=useState(""), [sending,setSending]=useState(false);
  const fileInput = useRef(null);
  const [attachmentName, setAttachmentName] = useState("");
  const uploadAttachment = async (event) => {
    const file = event.target.files?.[0];
    if (!file) return;

    setAttachmentName(file.name);
    const body = new FormData();
    body.append("file", file);
    try {
      const response = await fetch("/api/upload", { method: "POST", body });
      if (!response.ok) setAttachmentName(`${file.name} (upload failed)`);
    } catch {
      setAttachmentName(`${file.name} (upload failed)`);
    }
  };
  const send=async()=>{
    const text=q.trim();
    if(!text || sending)return;
    const id=Date.now();
    setMsgs(p=>[...p,{id,role:"user",text}]);
    setQ("");
    setSending(true);
    try {
      const response=await fetch("/api/ask",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({question:text})});
      const data=await response.json();
      if(!response.ok) throw new Error(data.error||"Unable to get an answer.");
      const first=data.retrieved_chunks?.[0];
      setMsgs(p=>[...p,{id:id+1,role:"ai",text:data.answer,source:first?{name:first.source,excerpt:first.text}:null}]);
    } catch(error) {
      setMsgs(p=>[...p,{id:id+1,role:"ai",text:error.message}]);
    } finally { setSending(false); }
  };
  return <div className="chat-layout">
    <aside className="chat-history-panel"><button className="green-btn new-chat"><Plus size={18}/>New Chat</button><h4>RECENT CHATS</h4>{["Attendance requirements","Academic rules","Course structure"].map(x=><button className="history-item" key={x}>{x}</button>)}</aside>
    <section className="chat-window"><div className="chat-heading"><div className="chat-avatar"><Bot size={23}/></div><div><h2>AI Knowledge Assistant</h2><span>Answers grounded in your documents</span></div></div>
      <div className="chat-messages">{msgs.map(m=><div key={m.id} className={`chat-message ${m.role}`}>
        <div className="message-avatar">{m.role==="ai"?<Bot size={18}/>:<User size={18}/>}</div>
        <div className="message-body"><p>{m.text}</p>{m.source&&<SourceCard source={m.source}/>}</div>
      </div>)}</div>
      <div className="chat-composer"><input ref={fileInput} type="file" hidden accept=".pdf,.docx,.txt,.csv,.xls,.xlsx,application/pdf,application/vnd.openxmlformats-officedocument.wordprocessingml.document,text/plain,text/csv,application/vnd.ms-excel,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" onChange={uploadAttachment}/><button type="button" onClick={() => fileInput.current?.click()} aria-label="Attach a file"><Paperclip size={20}/></button><input disabled={sending} value={q} onChange={e=>setQ(e.target.value)} onKeyDown={e=>e.key==="Enter"&&send()} placeholder="Ask a question about your documents..."/><button className="send" disabled={sending} onClick={send} type="button"><Send size={19}/></button></div>
      {attachmentName && <small className="chat-note">Attached: {attachmentName}</small>}
      <small className="chat-note">AI answers are based on your uploaded knowledge base. Verify important information.</small>
    </section>
  </div>;
}
