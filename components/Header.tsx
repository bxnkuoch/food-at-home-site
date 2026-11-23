import Link from "next/link";
import type { Settings } from "@/sanity/lib/types";

export function Header({ s }: { s: Settings }) {
  return (
    <header className="site-header">
      <div className="wrap header-inner">
        <Link href="/" className="brand"><span className="brand-dot" aria-hidden />{s.appName}</Link>
        <input type="checkbox" id="nav-toggle" className="nav-toggle" aria-label="Open menu" />
        <label htmlFor="nav-toggle" className="nav-burger" aria-hidden>☰</label>
        <nav className="nav">
          <Link href="/#features">Features</Link>
          <Link href="/#team">Team</Link>
          <Link href="/status">Status Posts</Link>
          <Link href="/faq">FAQ</Link>
          <Link href="/privacy">Privacy</Link>
          <Link href="/download" className="btn btn-small">Download</Link>
        </nav>
      </div>
    </header>
  );
}

export function Footer({ s }: { s: Settings }) {
  return (
    <footer className="site-footer">
      <div className="wrap footer-grid">
        <div>
          <div className="brand"><span className="brand-dot" aria-hidden />{s.appName}</div>
          <p className="muted">{s.tagline}</p>
          <p className="muted small">A Drexel senior design project by {s.teamName}.</p>
        </div>
        <div>
          <h4>App</h4>
          <Link href="/#features">Features</Link>
          <Link href="/download">Download</Link>
          <Link href="/faq">FAQ</Link>
        </div>
        <div>
          <h4>Project</h4>
          <Link href="/status">Status Posts</Link>
          {s.instagramUrl && <a href={s.instagramUrl} target="_blank" rel="noopener noreferrer">Instagram</a>}
          {s.contactEmail && <a href={`mailto:${s.contactEmail}`}>Contact</a>}
        </div>
        <div>
          <h4>Legal</h4>
          <Link href="/privacy">Privacy Policy</Link>
        </div>
      </div>
      <div className="wrap small muted copyright">© {new Date().getFullYear()} {s.teamName}</div>
    </footer>
  );
}
