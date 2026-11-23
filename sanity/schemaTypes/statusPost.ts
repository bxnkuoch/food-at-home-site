import { defineField, defineType } from "sanity";

export const statusPost = defineType({
  name: "statusPost",
  title: "Status Post",
  type: "document",
  fields: [
    defineField({ name: "title", type: "string", description: 'e.g. "Status Post 04"', validation: (r) => r.required() }),
    defineField({ name: "slug", type: "slug", options: { source: "title" }, validation: (r) => r.required() }),
    defineField({ name: "publishedAt", title: "Post date", type: "date", validation: (r) => r.required() }),
    defineField({ name: "periodStart", title: "Covers from", type: "date" }),
    defineField({ name: "periodEnd", title: "Covers to", type: "date" }),
    defineField({ name: "heroImage", type: "image", options: { hotspot: true }, fields: [{ name: "alt", type: "string", title: "Alt text" }] }),
    defineField({ name: "summary", type: "text", rows: 3, description: "Short blurb shown on the status list. Tasks and meetings are added separately (Studio → Tasks / Meetings) and link to this post." }),
    defineField({ name: "reflections", title: "Reflections / what we can do more efficiently", type: "richText" }),
  ],
  orderings: [{ title: "Newest first", name: "dateDesc", by: [{ field: "publishedAt", direction: "desc" }] }],
  preview: { select: { title: "title", subtitle: "publishedAt", media: "heroImage" } },
});
