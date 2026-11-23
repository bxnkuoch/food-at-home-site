import { RichText } from "./RichText";
import type { Faq } from "@/sanity/lib/types";

export function FaqList({ faqs }: { faqs: Faq[] }) {
  if (!faqs.length) return <p className="muted">No questions yet. Add some in the Studio under FAQs.</p>;
  return (
    <div className="faq">
      {faqs.map((f) => (
        <details key={f._id}>
          <summary>{f.question}</summary>
          <RichText value={f.answer} />
        </details>
      ))}
    </div>
  );
}
