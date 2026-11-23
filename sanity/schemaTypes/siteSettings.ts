import { defineField, defineType } from "sanity";

export const siteSettings = defineType({
  name: "siteSettings",
  title: "Site Settings & Download",
  type: "document",
  groups: [
    { name: "brand", title: "Brand", default: true },
    { name: "home", title: "Home page" },
    { name: "download", title: "Download" },
  ],
  fields: [
    defineField({ name: "appName", type: "string", group: "brand", initialValue: "Food at Home" }),
    defineField({ name: "teamName", type: "string", group: "brand", initialValue: "Team Cronch" }),
    defineField({ name: "tagline", type: "string", group: "brand" }),
    defineField({ name: "logo", type: "image", group: "brand" }),
    defineField({ name: "contactEmail", type: "string", group: "brand" }),
    defineField({ name: "instagramUrl", type: "url", group: "brand" }),
    defineField({ name: "heroTitle", type: "string", group: "home" }),
    defineField({ name: "heroText", type: "text", rows: 3, group: "home" }),
    defineField({ name: "heroImage", type: "image", group: "home", options: { hotspot: true } }),
    defineField({ name: "features", type: "array", of: [{ type: "feature" }], group: "home" }),
    defineField({ name: "testflightUrl", title: "TestFlight public link", type: "url", group: "download", description: "Public beta invite link from App Store Connect" }),
    defineField({ name: "appStoreUrl", title: "App Store link", type: "url", group: "download" }),
    defineField({ name: "playStoreUrl", title: "Google Play link", type: "url", group: "download" }),
    defineField({ name: "downloadNote", type: "text", rows: 2, group: "download", description: 'e.g. "Requires iOS 17+. Free beta."' }),
  ],
});
