import Image from "next/image";
import Link from "next/link";
import { DownloadButtons } from "@/components/DownloadButtons";
import { FaqList } from "@/components/FaqList";
import { fmtDate } from "@/components/format";
import { sanityFetch } from "@/sanity/lib/client";
import { urlFor } from "@/sanity/lib/image";
import { homeFaqsQuery, postsQuery, teamQuery } from "@/sanity/lib/queries";
import { TeamGrid } from "@/components/TeamGrid";
import type { Faq, Member, PostListItem } from "@/sanity/lib/types";
import { getSettings } from "@/sanity/lib/settings";

export default async function Home() {
  const [s, posts, faqs, team] = await Promise.all([
    getSettings(),
    sanityFetch<PostListItem[]>(postsQuery, {}, []),
    sanityFetch<Faq[]>(homeFaqsQuery, {}, []),
    sanityFetch<Member[]>(teamQuery, {}, []),
  ]);

  return (
    <>
      <section className="hero">
        <div className="wrap hero-grid">
          <div>
            <span className="pill">Senior design project · iOS beta</span>
            <h1>{s.heroTitle}</h1>
            <p className="lead">{s.heroText}</p>
            <div className="hero-cta">
              <Link href="/download" className="btn">Download the app</Link>
              <Link href="/status" className="btn btn-ghost">Read our progress</Link>
            </div>
          </div>
          <div className="hero-art">
            {s.heroImage?.asset ? (
              <Image src={urlFor(s.heroImage).width(900).url()} alt="" width={900} height={900} priority />
            ) : (
              <div className="phone-mock" aria-hidden>
                <div className="pm-row"><span>🥬 Spinach</span><b className="warn">2 days</b></div>
                <div className="pm-row"><span>🥛 Milk</span><b className="ok">5 days</b></div>
                <div className="pm-row"><span>🍌 Bananas</span><b className="warn">1 day</b></div>
                <div className="pm-row"><span>🧀 Cheddar</span><b className="ok">3 wks</b></div>
              </div>
            )}
          </div>
        </div>
      </section>

      <section id="features" className="section">
        <div className="wrap">
          <h2>What it does</h2>
          <div className="card-grid">
            {s.features?.map((f) => (
              <div key={f._key} className="card">
                {f.image?.asset && <Image src={urlFor(f.image).width(600).url()} alt="" width={600} height={400} className="card-img" />}
                <h3>{f.title}</h3>
                <p className="muted">{f.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {team.length > 0 && (
        <section id="team" className="section">
          <div className="wrap center">
            <h2>Meet the team</h2>
            <p className="muted">{s.teamName} · Drexel senior design, 2026–27</p>
            <TeamGrid team={team} />
          </div>
        </section>
      )}

      <section className="section alt">
        <div className="wrap">
          <div className="section-head">
            <h2>Latest status posts</h2>
            <Link href="/status">All posts →</Link>
          </div>
          <div className="card-grid three">
            {posts.slice(0, 3).map((p) => (
              <Link key={p._id} href={`/status/${p.slug}`} className="card post-card">
                <span className="date">{fmtDate(p.publishedAt)}</span>
                <h3>{p.title}</h3>
                {p.summary && <p className="muted">{p.summary}</p>}
              </Link>
            ))}
            {!posts.length && <p className="muted">No posts yet.</p>}
          </div>
        </div>
      </section>

      <section className="section">
        <div className="wrap narrow">
          <h2>Frequently asked questions</h2>
          <FaqList faqs={faqs} />
          <p><Link href="/faq">See all questions →</Link></p>
        </div>
      </section>

      <section className="section cta">
        <div className="wrap narrow center">
          <h2>Try {s.appName}</h2>
          {s.downloadNote && <p className="muted">{s.downloadNote}</p>}
          <DownloadButtons s={s} />
        </div>
      </section>
    </>
  );
}
