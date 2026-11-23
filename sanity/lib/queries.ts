import { groq } from "next-sanity";

export const settingsQuery = groq`*[_id == "siteSettings"][0]`;

const taskFields = `_id, title, status, category, dueDate, finishedDate, estimateHours, description, deliverables, takeaways, images,
  "contributors": contributors[]{ _key, hours, "member": member->{ _id, name, photo } }`;

export const postsQuery = groq`*[_type == "statusPost" && defined(slug.current)] | order(publishedAt desc){
  _id, title, "slug": slug.current, publishedAt, summary, heroImage,
  "closedCount": count(*[_type == "task" && references(^._id) && status == "closed"]),
  "openCount": count(*[_type == "task" && references(^._id) && status == "open"]),
  "newCount": count(*[_type == "task" && references(^._id) && status == "new"])
}`;

export const postQuery = groq`*[_type == "statusPost" && slug.current == $slug][0]{
  ...,
  "tasks": *[_type == "task" && references(^._id)] | order(coalesce(finishedDate, dueDate) asc){ ${taskFields} },
  "meetings": *[_type == "meeting" && references(^._id)] | order(date asc){
    _id, title, date, duration, location, guests, agenda, takeaways, "attendees": attendees[]->{ _id, name }
  },
  "prev": *[_type == "statusPost" && publishedAt < ^.publishedAt] | order(publishedAt desc)[0]{title, "slug": slug.current},
  "next": *[_type == "statusPost" && publishedAt > ^.publishedAt] | order(publishedAt asc)[0]{title, "slug": slug.current}
}`;

export const teamQuery = groq`*[_type == "teamMember"] | order(order asc, name asc){ _id, name, roles, photo }`;

export const postSlugsQuery = groq`*[_type == "statusPost" && defined(slug.current)].slug.current`;

export const faqsQuery = groq`*[_type == "faq"] | order(order asc, _createdAt asc)`;
export const homeFaqsQuery = groq`*[_type == "faq" && showOnHome == true] | order(order asc)[0...5]`;

export const privacyQuery = groq`*[_id == "privacyPolicy"][0]`;
