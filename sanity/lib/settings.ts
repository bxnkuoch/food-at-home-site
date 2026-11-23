import { sanityFetch } from "./client";
import { settingsQuery } from "./queries";
import { defaultSettings, type Settings } from "./types";

export async function getSettings(): Promise<Settings> {
  const s = await sanityFetch<Settings | null>(settingsQuery, {}, null);
  return { ...defaultSettings, ...(s ?? {}) };
}
