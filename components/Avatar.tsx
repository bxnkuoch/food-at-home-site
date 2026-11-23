import Image from "next/image";
import { urlFor } from "@/sanity/lib/image";
import type { Member } from "@/sanity/lib/types";

// Framer team-card colors, darkened where needed so white initials pass 4.5:1
const PALETTE = ["#0c7aca", "#bd4b97", "#c15600", "#008840", "#937101", "#7c7560", "#3f10cc", "#9241e8"];

export function Avatar({ m, size = 32 }: { m: Member; size?: number }) {
  const color = PALETTE[[...m.name].reduce((a, c) => a + c.charCodeAt(0), 0) % PALETTE.length];
  if (m.photo?.asset) {
    return <Image className="avatar" src={urlFor(m.photo).width(size * 2).height(size * 2).url()} alt={m.name} width={size} height={size} title={m.name} />;
  }
  return (
    <span className="avatar" title={m.name} style={{ width: size, height: size, background: color, fontSize: size * 0.42 }}>
      {m.name.split(/\s+/).map((w) => w[0]).join("").slice(0, 2).toUpperCase()}
    </span>
  );
}
