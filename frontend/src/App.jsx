import { useState } from "react";
import Header from "./components/Header";
import Sidebar from "./components/Sidebar";
import BottomNav from "./components/BottomNav";
import Home from "./pages/Home";
import Upload from "./pages/Upload";
import Library from "./pages/Library";
import Chat from "./pages/Chat";

export default function App() {
  const [page, setPage] = useState("home");
  const [mobileOpen, setMobileOpen] = useState(false);

  return (
    <div className="app-shell">
      <Sidebar page={page} setPage={setPage} mobileOpen={mobileOpen}
        closeMobile={() => setMobileOpen(false)} />
      <div className="app-main">
        <Header setPage={setPage} openMobile={() => setMobileOpen(true)} />
        <main className="content">
          {page === "home" && <Home setPage={setPage} />}
          {page === "upload" && <Upload setPage={setPage} />}
          {page === "library" && <Library />}
          {page === "chat" && <Chat />}
        </main>
      </div>
      <BottomNav page={page} setPage={setPage} />
    </div>
  );
}