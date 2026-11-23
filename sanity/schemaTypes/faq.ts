import { defineField, defineType } from "sanity";

export const faq = defineType({
  name: "faq",
  title: "FAQ",
  type: "document",
  fields: [
    defineField({ name: "question", type: "string", validation: (r) => r.required() }),
    defineField({ name: "answer", type: "richText", validation: (r) => r.required() }),
    defineField({ name: "showOnHome", title: "Show on home page", type: "boolean", initialValue: false }),
    defineField({ name: "order", type: "number", description: "Lower numbers show first" }),
  ],
  orderings: [{ title: "Order", name: "orderAsc", by: [{ field: "order", direction: "asc" }] }],
  preview: { select: { title: "question", subtitle: "order" } },
});
