import { createClient } from "next-sanity";
import { apiVersion, dataset, isConfigured, projectId } from "../env";

export const client = createClient({ projectId, dataset, apiVersion, useCdn: true });

/** Fetch with ISR (pages refresh at most every 60s). Returns fallback until Sanity is configured. */
export async function sanityFetch<T>(query: string, params: Record<string, unknown> = {}, fallback: T): Promise<T> {
  if (!isConfigured) return fallback;
  try {
    return (await client.fetch<T>(query, params, { next: { revalidate: 60 } })) ?? fallback;
  } catch (err) {
    console.error("Sanity fetch failed", err);
    return fallback;
  }
}
