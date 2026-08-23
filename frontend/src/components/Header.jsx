import { Menu, Box } from "lucide-react";

export default function Header({ setPage, openMobile }) {
  return (
    <header className="topbar">
      <button className="mobile-menu" onClick={openMobile} type="button"><Menu size={23}/></button>
      <button className="mobile-brand" onClick={() => setPage("home")} type="button">
        <span className="logo-small"><Box size={18}/></span>
        <b>AI Avengers</b>
      </button>
      <div className="desktop-top-spacer"/>
      <div className="profile-circle">A</div>
    </header>
  );
}