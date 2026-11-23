import type { Metadata } from "next";
import "./globals.css";
import { Footer, Header } from "@/components/Header";
import { getSettings } from "@/sanity/lib/settings";

export async function generateMetadata(): Promise<Metadata> {
  const s = await getSettings();
  return { title: { default: s.appName!, template: `%s · ${s.appName}` }, description: s.tagline };
}

export default async function SiteLayout({ children }: { children: React.ReactNode }) {
  const s = await getSettings();
  return (
    <html lang="en">
      <body>
        <Header s={s} />
        <main>{children}</main>
        <Footer s={s} />
      </body>
    </html>
  );
}
