import Link from "next/link";
import { fmtDate } from "@/components/format";
import { sanityFetch } from "@/sanity/lib/client";
import { postsQuery } from "@/sanity/lib/queries";
import type { PostListItem } from "@/sanity/lib/types";

export const metadata = { title: "Status Posts" };

export default async function StatusIndex() {
  const posts = await sanityFetch<PostListItem[]>(postsQuery, {}, []);
  return (
    <section className="section">
      <div className="wrap narrow">
        <span className="pill">Project updates</span>
        <h1>Status Posts</h1>
        <p className="lead">Every two weeks we post what we finished, what's in progress, and what we learned.</p>
        <ul className="post-list">
          {posts.map((p) => (
            <li key={p._id}>
              <Link href={`/status/${p.slug}`}>
                <span className="date">{fmtDate(p.publishedAt)}</span>
                <span className="post-title">{p.title}</span>
                <span className="counts muted small">
                  {p.closedCount ?? 0} closed · {p.openCount ?? 0} open · {p.newCount ?? 0} new
                </span>
              </Link>
            </li>
          ))}
        </ul>
        {!posts.length && <p className="muted">No posts yet. Create one in the Studio at /studio.</p>}
      </div>
    </section>
  );
}
