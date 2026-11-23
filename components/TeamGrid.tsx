import { Avatar } from "./Avatar";
import type { Member } from "@/sanity/lib/types";

export function TeamGrid({ team }: { team: Member[] }) {
  if (!team.length) return null;
  return (
    <div className="team-grid">
      {team.map((m) => (
        <div key={m._id} className="member">
          <Avatar m={m} size={88} />
          <h3>{m.name}</h3>
          {m.roles?.length ? <p className="muted small">{m.roles.join(" · ")}</p> : null}
        </div>
      ))}
    </div>
  );
}
