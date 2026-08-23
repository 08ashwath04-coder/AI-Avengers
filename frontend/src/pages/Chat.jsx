import { useState } from "react";
import { Bot, Send, Paperclip, Plus, User } from "lucide-react";
import { messages as initial } from "../data/mockData";
import SourceCard from "../components/SourceCard";

export default function Chat() {
  const [msgs,setMsgs]=useState(initial), [q,setQ]=useState("");
  const send=()=>{const text=q.trim();if(!text)return;setMsgs(p=>[...p,{id:Date.now(),role:"user",text},{id:Date.now()+1,role:"ai",text:"This is the frontend demo response. The backend/LLM can replace this response during integration.",source:{name:"Employee_Handbook_2023.pdf",page:12,excerpt:"Relevant information retrieved from your uploaded knowledge base."}}]);setQ("")};
  return <div className="chat-layout">
    <aside className="chat-history-panel"><button className="green-btn new-chat"><Plus size={18}/>New Chat</button><h4>RECENT CHATS</h4>{["Attendance requirements","Academic rules","Course structure"].map(x=><button className="history-item" key={x}>{x}</button>)}</aside>
    <section className="chat-window"><div className="chat-heading"><div className="chat-avatar"><Bot size={23}/></div><div><h2>AI Knowledge Assistant</h2><span>Answers grounded in your documents</span></div></div>
      <div className="chat-messages">{msgs.map(m=><div key={m.id} className={`chat-message ${m.role}`}>
        <div className="message-avatar">{m.role==="ai"?<Bot size={18}/>:<User size={18}/>}</div>
        <div className="message-body"><p>{m.text}</p>{m.source&&<SourceCard source={m.source}/>}</div>
      </div>)}</div>
      <div className="chat-composer"><button type="button"><Paperclip size={20}/></button><input value={q} onChange={e=>setQ(e.target.value)} onKeyDown={e=>e.key==="Enter"&&send()} placeholder="Ask a question about your documents..."/><button className="send" onClick={send} type="button"><Send size={19}/></button></div>
      <small className="chat-note">AI answers are based on your uploaded knowledge base. Verify important information.</small>
    </section>
  </div>;
}