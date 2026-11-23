import type { Settings } from "@/sanity/lib/types";

export function DownloadButtons({ s, compact = false }: { s: Settings; compact?: boolean }) {
  const links = [
    s.appStoreUrl && { href: s.appStoreUrl, label: "App Store", kicker: "Download on the" },
    s.testflightUrl && { href: s.testflightUrl, label: "TestFlight beta", kicker: "Join the iOS" },
    s.playStoreUrl && { href: s.playStoreUrl, label: "Google Play", kicker: "Get it on" },
  ].filter(Boolean) as { href: string; label: string; kicker: string }[];

  if (!links.length) {
    return <p className="muted">Download links are coming soon. Follow our status posts for updates.</p>;
  }
  return (
    <div className={`dl-row ${compact ? "compact" : ""}`}>
      {links.map((l) => (
        <a key={l.href} className="dl-btn" href={l.href} target="_blank" rel="noopener noreferrer">
          <span className="dl-kicker">{l.kicker}</span>
          <span className="dl-label">{l.label}</span>
        </a>
      ))}
    </div>
  );
}
