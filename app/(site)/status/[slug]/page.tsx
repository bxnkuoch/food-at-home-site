import Image from "next/image";
import Link from "next/link";
import { notFound } from "next/navigation";
import { Avatar } from "@/components/Avatar";
import { CATEGORY_LABELS } from "@/components/categories";
import { RichText } from "@/components/RichText";
import { fmtDate } from "@/components/format";
import { sanityFetch } from "@/sanity/lib/client";
import { urlFor } from "@/sanity/lib/image";
import { postQuery, postSlugsQuery } from "@/sanity/lib/queries";
import type { Meeting, Member, Post, Task } from "@/sanity/lib/types";

type Props = { params: Promise<{ slug: string }> };

export async function generateStaticParams() {
  const slugs = await sanityFetch<string[]>(postSlugsQuery, {}, []);
  return slugs.map((slug) => ({ slug }));
}

export async function generateMetadata({ params }: Props) {
  const { slug } = await params;
  const post = await sanityFetch<Post | null>(postQuery, { slug }, null);
  return { title: post?.title ?? "Status Post" };
}

const fmtH = (h: number) => `${Math.round(h * 10) / 10}h`;

function statusLabel(t: Task) {
  if (t.status === "closed") return t.finishedDate ? `Finished ${fmtDate(t.finishedDate)}` : "Finished";
  if (t.status === "open") return t.dueDate ? `In progress · due ${fmtDate(t.dueDate)}` : "In progress";
  return t.dueDate ? `Due ${fmtDate(t.dueDate)}` : "New";
}

function TaskCard({ t }: { t: Task }) {
  return (
    <article className="card task">
      <div className="task-top small">
        {t.category && <span className="tag">{CATEGORY_LABELS[t.category] ?? t.category}</span>}
        <span className={`status status-${t.status}`}>{statusLabel(t)}</span>
        {t.status !== "closed" && t.estimateHours ? <span className="muted">{t.estimateHours}h est.</span> : null}
      </div>
      <h4>{t.title}</h4>
      <RichText value={t.description} />
      {t.deliverables?.length ? (
        <p className="deliverables">
          {t.deliverables.map((d) => (
            <a key={d._key} className="chip" href={d.url} target="_blank" rel="noopener noreferrer">{d.label} ↗</a>
          ))}
        </p>
      ) : null}
      {t.takeaways?.length ? <div className="takeaway"><b>Takeaways</b><RichText value={t.takeaways} /></div> : null}
      {t.images?.map((img, i) => img?.asset && (
        <Image key={i} className="rt-img" src={urlFor(img).width(1200).url()} alt={img.alt || ""} width={1200} height={750} />
      ))}
      {t.contributors?.length ? (
        <div className="owners">
          {t.contributors.filter((c) => c.member).map((c) => (
            <span key={c._key} className="owner">
              <Avatar m={c.member!} size={24} />
              {c.member!.name}{c.hours ? ` ${fmtH(c.hours)}` : ""}
            </span>
          ))}
        </div>
      ) : null}
    </article>
  );
}

function MeetingCard({ m }: { m: Meeting }) {
  const who = [...(m.attendees?.map((a) => a.name) ?? []), ...(m.guests ?? [])];
  return (
    <article className="card task">
      <h4>{m.title}</h4>
      <dl className="meta">
        {m.date && <><dt>When</dt><dd>{fmtDate(m.date)}{m.duration ? ` · ${m.duration}` : ""}{m.location ? ` · ${m.location}` : ""}</dd></>}
        {who.length ? <><dt>Attendees</dt><dd>{who.join(", ")}</dd></> : null}
      </dl>
      <RichText value={m.agenda} />
      {m.takeaways?.length ? <div className="takeaway"><b>Takeaways</b><RichText value={m.takeaways} /></div> : null}
    </article>
  );
}

function Bars({ rows }: { rows: { label: React.ReactNode; key: string; value: number }[] }) {
  const max = Math.max(...rows.map((r) => r.value), 1);
  return (
    <div className="bars">
      {rows.map((r) => (
        <div key={r.key} className="bar-row">
          <span className="bar-label">{r.label}</span>
          <span className="bar-track"><span className="bar-fill" style={{ width: `${(r.value / max) * 100}%` }} /></span>
          <span className="bar-value">{fmtH(r.value)}</span>
        </div>
      ))}
    </div>
  );
}

const SECTIONS = [
  { status: "closed", title: "Closed", id: "closed" },
  { status: "open", title: "Open", id: "open" },
  { status: "new", title: "New", id: "new" },
] as const;

export default async function StatusPost({ params }: Props) {
  const { slug } = await params;
  const post = await sanityFetch<Post | null>(postQuery, { slug }, null);
  if (!post) notFound();

  const tasks = post.tasks ?? [];
  const byStatus = (s: string) => tasks.filter((t) => t.status === s);

  // Hours per person and per category, from each task's contributors
  const people = new Map<string, { m: Member; h: number }>();
  const cats = new Map<string, number>();
  let total = 0;
  for (const t of tasks) {
    for (const c of t.contributors ?? []) {
      if (!c.member) continue;
      const entry = people.get(c.member._id) ?? { m: c.member, h: 0 };
      entry.h += c.hours ?? 0;
      people.set(c.member._id, entry);
      if (c.hours) {
        total += c.hours;
        const cat = t.category ?? "other";
        cats.set(cat, (cats.get(cat) ?? 0) + c.hours);
      }
    }
  }
  const contributors = [...people.values()];
  const loggers = contributors.filter((p) => p.h > 0).sort((a, b) => b.h - a.h);

  return (
    <div className="section">
      <div className="wrap narrow">
        <nav className="crumbs small"><Link href="/status">← Status Posts</Link></nav>
        <h1>{post.title}</h1>
        <p className="date">
          {fmtDate(post.publishedAt)}
          {post.periodStart && post.periodEnd && <> · covers {fmtDate(post.periodStart)} – {fmtDate(post.periodEnd)}</>}
        </p>
        {post.summary && <p className="lead">{post.summary}</p>}
        {contributors.length > 0 && (
          <div className="avatar-row">
            <span className="avatar-stack">{contributors.map((p) => <Avatar key={p.m._id} m={p.m} size={32} />)}</span>
            <span className="muted small">{contributors.length} people contributed</span>
          </div>
        )}
        {post.heroImage?.asset && (
          <Image className="post-hero" src={urlFor(post.heroImage).width(1400).url()} alt={post.heroImage.alt || ""} width={1400} height={800} priority />
        )}

        <div className="stats">
          <div className="stat"><b>{byStatus("closed").length}</b><span>tasks closed</span></div>
          <div className="stat"><b>{total ? fmtH(total) : "–"}</b><span>hours logged</span></div>
          <div className="stat"><b>{byStatus("open").length}</b><span>in progress</span></div>
          <div className="stat"><b>{byStatus("new").length}</b><span>new tasks</span></div>
        </div>

        {total > 0 && (
          <div className="breakdowns">
            <div className="card">
              <h3>Who worked on what</h3>
              <Bars rows={loggers.map((p) => ({ key: p.m._id, value: p.h, label: <><Avatar m={p.m} size={20} /> {p.m.name}</> }))} />
            </div>
            <div className="card">
              <h3>Where the time went</h3>
              <Bars rows={[...cats.entries()].sort((a, b) => b[1] - a[1]).map(([k, v]) => ({ key: k, value: v, label: CATEGORY_LABELS[k] ?? "Other" }))} />
            </div>
          </div>
        )}

        <nav className="tabs">
          {SECTIONS.map((s) => <a key={s.id} href={`#${s.id}`}>{s.title} <span className="count">{byStatus(s.status).length}</span></a>)}
          <a href="#meetings">Meetings <span className="count">{post.meetings?.length ?? 0}</span></a>
        </nav>

        {SECTIONS.map((s) => {
          const list = byStatus(s.status);
          if (!list.length) return null;
          return (
            <section key={s.id} id={s.id} className="post-section">
              <h2>{s.title} tasks</h2>
              <div className="stack">{list.map((t) => <TaskCard key={t._id} t={t} />)}</div>
            </section>
          );
        })}
        {post.meetings?.length ? (
          <section id="meetings" className="post-section">
            <h2>Meetings</h2>
            <div className="stack">{post.meetings.map((m) => <MeetingCard key={m._id} m={m} />)}</div>
          </section>
        ) : null}
        {post.reflections?.length ? (
          <section className="post-section">
            <h2>What we can do more efficiently</h2>
            <RichText value={post.reflections} />
          </section>
        ) : null}

        <nav className="prev-next">
          {post.prev ? <Link href={`/status/${post.prev.slug}`}>← {post.prev.title}</Link> : <span />}
          {post.next ? <Link href={`/status/${post.next.slug}`}>{post.next.title} →</Link> : <span />}
        </nav>
      </div>
    </div>
  );
}
