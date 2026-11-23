import { FaqList } from "@/components/FaqList";
import { sanityFetch } from "@/sanity/lib/client";
import { faqsQuery } from "@/sanity/lib/queries";
import type { Faq } from "@/sanity/lib/types";

export const metadata = { title: "FAQ" };

export default async function FaqPage() {
  const faqs = await sanityFetch<Faq[]>(faqsQuery, {}, []);
  return (
    <section className="section">
      <div className="wrap narrow">
        <h1>Frequently Asked Questions</h1>
        <p className="lead">Quick answers about the app, your data, and the project.</p>
        <FaqList faqs={faqs} />
      </div>
    </section>
  );
}
