import type { Metadata } from "next";
import { Inter, Montserrat } from "next/font/google";
import "./globals.css";
import { Footer, Header } from "@/components/Header";
import { getSettings } from "@/sanity/lib/settings";
import { urlFor } from "@/sanity/lib/image";

const inter = Inter({ subsets: ["latin"], variable: "--font-inter" });
const montserrat = Montserrat({ subsets: ["latin"], weight: ["400", "700", "900"], variable: "--font-montserrat" });

export async function generateMetadata(): Promise<Metadata> {
  const s = await getSettings();
  const icon = s.logo?.asset ? urlFor(s.logo).width(64).height(64).fit("max").format("png").url() : undefined;
  return {
    title: { default: s.appName!, template: `%s · ${s.appName}` },
    description: s.tagline,
    ...(icon ? { icons: { icon, apple: icon } } : {}),
  };
}

export default async function SiteLayout({ children }: { children: React.ReactNode }) {
  const s = await getSettings();
  return (
    <html lang="en" className={`${inter.variable} ${montserrat.variable}`}>
      <body>
        <Header s={s} />
        <main>{children}</main>
        <Footer s={s} />
      </body>
    </html>
  );
}
