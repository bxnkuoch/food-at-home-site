import Link from "next/link";
import { RichText } from "@/components/RichText";
import { fmtDate } from "@/components/format";
import { sanityFetch } from "@/sanity/lib/client";
import { privacyQuery } from "@/sanity/lib/queries";
import type { Privacy } from "@/sanity/lib/types";

export const metadata = { title: "Privacy Policy" };

export default async function PrivacyPage() {
  const p = await sanityFetch<Privacy | null>(privacyQuery, {}, null);
  return (
    <section className="section">
      <div className="wrap narrow prose">
        <nav className="crumbs small"><Link href="/">Home</Link> / Privacy Policy</nav>
        <h1>{p?.title ?? "Privacy Policy"}</h1>
        {p?.effectiveDate && <p className="date">Effective {fmtDate(p.effectiveDate)}</p>}
        {!p && <p className="muted">The privacy policy hasn't been published yet.</p>}
        <RichText value={p?.intro} />
        {p?.sections?.map((sec, i) => (
          <section key={sec._key}>
            <h2>{i + 1}. {sec.heading}</h2>
            <RichText value={sec.body} />
          </section>
        ))}
        {p?.contactEmail && <p>Questions? Email <a href={`mailto:${p.contactEmail}`}>{p.contactEmail}</a>.</p>}
      </div>
    </section>
  );
}
