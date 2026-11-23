import { defineField, defineType } from "sanity";

export const privacyPolicy = defineType({
  name: "privacyPolicy",
  title: "Privacy Policy",
  type: "document",
  fields: [
    defineField({ name: "title", type: "string", initialValue: "Privacy Policy" }),
    defineField({ name: "effectiveDate", type: "date", validation: (r) => r.required() }),
    defineField({ name: "intro", type: "richText" }),
    defineField({
      name: "sections",
      type: "array",
      of: [{
        type: "object",
        name: "policySection",
        fields: [
          defineField({ name: "heading", type: "string", validation: (r) => r.required() }),
          defineField({ name: "body", type: "richText" }),
        ],
      }],
    }),
    defineField({ name: "contactEmail", type: "string" }),
  ],
});
