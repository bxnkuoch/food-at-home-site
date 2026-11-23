/* Loose types for query results. Run `npx sanity typegen generate` later for exact ones. */
/* eslint-disable @typescript-eslint/no-explicit-any */
export type RichText = any[];
export type SanityImage = { asset?: { _ref: string }; alt?: string } | undefined;

export interface Member { _id: string; name: string; photo?: SanityImage; roles?: string[] }
export interface Task {
  _id: string; title: string; status: "closed" | "open" | "new"; category?: string;
  dueDate?: string; finishedDate?: string; estimateHours?: number;
  contributors?: { _key: string; hours?: number; member: Member | null }[];
  description?: RichText; deliverables?: { _key: string; label: string; url: string }[];
  takeaways?: RichText; images?: SanityImage[];
}
export interface Meeting {
  _id: string; title: string; date?: string; duration?: string; location?: string;
  attendees?: { _id: string; name: string }[]; guests?: string[]; agenda?: RichText; takeaways?: RichText;
}
export interface PostListItem {
  _id: string; title: string; slug: string; publishedAt: string; summary?: string; heroImage?: SanityImage;
  closedCount?: number; openCount?: number; newCount?: number;
}
export interface Post extends PostListItem {
  periodStart?: string; periodEnd?: string; tasks?: Task[]; meetings?: Meeting[]; reflections?: RichText;
  prev?: { title: string; slug: string } | null; next?: { title: string; slug: string } | null;
}
export interface Faq { _id: string; question: string; answer: RichText }
export interface Privacy {
  title?: string; effectiveDate?: string; intro?: RichText; contactEmail?: string;
  sections?: { _key: string; heading: string; body?: RichText }[];
}
export interface Settings {
  appName?: string; teamName?: string; tagline?: string; logo?: SanityImage; logoHasName?: boolean; contactEmail?: string; instagramUrl?: string;
  heroTitle?: string; heroText?: string; heroImage?: SanityImage;
  features?: { _key: string; title: string; description?: string; image?: SanityImage }[];
  testflightUrl?: string; appStoreUrl?: string; playStoreUrl?: string; downloadNote?: string;
}

export const defaultSettings: Settings = {
  appName: "Food at Home",
  teamName: "Team Cronch",
  tagline: "Spend smarter. Waste less.",
  heroTitle: "Know what's in your kitchen before it goes bad",
  heroText:
    "Food at Home helps young adults and shared households track groceries, catch expiring food in time, and build better food habits.",
  features: [
    { _key: "1", title: "Scan your receipt", description: "Snap a grocery receipt and your items land in your inventory." },
    { _key: "2", title: "Expiration reminders", description: "Shelf-life estimates for 650+ foods, so you use things up in time." },
    { _key: "3", title: "Chomp & Toss metrics", description: "See what you ate, what you tossed, and where your grocery money went." },
    { _key: "4", title: "Shared households", description: "Invite roommates and keep one shared inventory and shopping list." },
  ],
};
