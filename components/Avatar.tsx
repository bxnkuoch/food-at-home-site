import Image from "next/image";
import { urlFor } from "@/sanity/lib/image";
import type { Member } from "@/sanity/lib/types";

const PALETTE = ["#2f7d4f", "#ff9f6b", "#7a5cc4", "#d9622b", "#3b8ea5", "#c4527a", "#8a9a2b", "#5c6bc0"];

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
