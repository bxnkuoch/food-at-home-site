import { defineArrayMember, defineField, defineType } from "sanity";

export const CATEGORIES = [
  { title: "🎨 Design", value: "design" },
  { title: "🔎 Research", value: "research" },
  { title: "💻 Development", value: "development" },
  { title: "📣 Marketing", value: "marketing" },
  { title: "🤝 Outreach", value: "outreach" },
  { title: "🗂️ Project Planning", value: "planning" },
];

export const teamMember = defineType({
  name: "teamMember",
  title: "Team Member",
  type: "document",
  fields: [
    defineField({ name: "name", type: "string", validation: (r) => r.required() }),
    defineField({ name: "photo", type: "image", options: { hotspot: true } }),
    defineField({ name: "roles", type: "array", of: [{ type: "string" }], options: { layout: "tags" } }),
    defineField({
      name: "email",
      type: "string",
      description: "The email you log in to Sanity with. Used for “My tasks” and to auto-fill you as owner. Not shown on the site.",
    }),
    defineField({ name: "order", type: "number" }),
  ],
  orderings: [{ title: "Order", name: "orderAsc", by: [{ field: "order", direction: "asc" }] }],
  preview: {
    select: { title: "name", roles: "roles", media: "photo" },
    prepare: ({ title, roles, media }) => ({ title, subtitle: roles?.join(", "), media }),
  },
});

/** Each task is its own document, so teammates can add theirs without editing the same post at once. */
export const task = defineType({
  name: "task",
  title: "Task",
  type: "document",
  fields: [
    defineField({
      name: "statusPost",
      type: "reference",
      to: [{ type: "statusPost" }],
      description: "Which status post this task appears in. Defaults to the newest post.",
      validation: (r) => r.required(),
    }),
    defineField({
      name: "status",
      type: "string",
      options: { list: [
        { title: "Closed (finished)", value: "closed" },
        { title: "Open (in progress)", value: "open" },
        { title: "New", value: "new" },
      ], layout: "radio", direction: "horizontal" },
      initialValue: "closed",
      validation: (r) => r.required(),
    }),
    defineField({ name: "title", type: "string", validation: (r) => r.required() }),
    defineField({ name: "category", type: "string", options: { list: CATEGORIES } }),
    defineField({
      name: "contributors",
      title: "Who worked on it",
      type: "array",
      of: [defineArrayMember({
        type: "object",
        name: "contribution",
        fields: [
          defineField({ name: "member", type: "reference", to: [{ type: "teamMember" }], validation: (r) => r.required() }),
          defineField({ name: "hours", type: "number", description: "Hours this person spent (leave blank if not tracked)" }),
        ],
        preview: {
          select: { title: "member.name", hours: "hours", media: "member.photo" },
          prepare: ({ title, hours, media }) => ({ title, subtitle: hours != null ? `${hours} h` : undefined, media }),
        },
      })],
    }),
    defineField({ name: "dueDate", type: "date" }),
    defineField({ name: "finishedDate", type: "date", hidden: ({ parent }) => parent?.status !== "closed" }),
    defineField({ name: "estimateHours", title: "Estimate (hours)", type: "number", hidden: ({ parent }) => parent?.status === "closed" }),
    defineField({ name: "description", type: "richText" }),
    defineField({ name: "deliverables", type: "array", of: [{ type: "link" }] }),
    defineField({ name: "takeaways", type: "richText" }),
    defineField({ name: "images", type: "array", of: [{ type: "image", options: { hotspot: true }, fields: [{ name: "alt", type: "string", title: "Alt text" }] }] }),
  ],
  initialValue: async (_params, { getClient, currentUser }) => {
    const client = getClient({ apiVersion: "2025-10-01" });
    const { post, me } = await client.fetch(
      `{ "post": *[_type == "statusPost"] | order(publishedAt desc)[0]._id,
         "me": *[_type == "teamMember" && lower(email) == lower($email)][0]._id }`,
      { email: currentUser?.email ?? "" },
    );
    return {
      status: "closed",
      ...(post ? { statusPost: { _type: "reference", _ref: post.replace(/^drafts\./, "") } } : {}),
      ...(me ? { contributors: [{ _type: "contribution", _key: Math.random().toString(36).slice(2, 10), member: { _type: "reference", _ref: me } }] } : {}),
    };
  },
  orderings: [{ title: "Due date", name: "dueAsc", by: [{ field: "dueDate", direction: "asc" }] }],
  preview: {
    select: { title: "title", status: "status", post: "statusPost.title", a: "contributors.0.member.name", b: "contributors.1.member.name" },
    prepare: ({ title, status, post, a, b }) => ({
      title,
      subtitle: [post, status, [a, b].filter(Boolean).join(", ")].filter(Boolean).join(" · "),
    }),
  },
});

export const meeting = defineType({
  name: "meeting",
  title: "Meeting",
  type: "document",
  fields: [
    defineField({ name: "statusPost", type: "reference", to: [{ type: "statusPost" }], validation: (r) => r.required() }),
    defineField({ name: "title", type: "string", description: 'e.g. "All-Hands" or "Design"', validation: (r) => r.required() }),
    defineField({ name: "date", type: "date" }),
    defineField({ name: "duration", type: "string", description: 'e.g. "1.5 hrs"' }),
    defineField({ name: "location", type: "string" }),
    defineField({ name: "attendees", type: "array", of: [{ type: "reference", to: [{ type: "teamMember" }] }] }),
    defineField({ name: "guests", type: "array", of: [{ type: "string" }], options: { layout: "tags" }, description: "People outside the team, e.g. advisors" }),
    defineField({ name: "agenda", type: "richText" }),
    defineField({ name: "takeaways", type: "richText" }),
  ],
  initialValue: async (_p, { getClient }) => {
    const post = await getClient({ apiVersion: "2025-10-01" }).fetch(`*[_type == "statusPost"] | order(publishedAt desc)[0]._id`);
    return post ? { statusPost: { _type: "reference", _ref: post.replace(/^drafts\./, "") } } : {};
  },
  orderings: [{ title: "Date", name: "dateDesc", by: [{ field: "date", direction: "desc" }] }],
  preview: {
    select: { title: "title", date: "date", post: "statusPost.title" },
    prepare: ({ title, date, post }) => ({ title, subtitle: [post, date].filter(Boolean).join(" · ") }),
  },
});
