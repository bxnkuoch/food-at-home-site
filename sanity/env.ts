export const apiVersion = "2025-10-01";
export const dataset = process.env.NEXT_PUBLIC_SANITY_DATASET || "production";
// Falls back to a placeholder so the site can build before the Sanity project exists.
export const projectId = process.env.NEXT_PUBLIC_SANITY_PROJECT_ID || "placeholder";
export const isConfigured = projectId !== "placeholder";
