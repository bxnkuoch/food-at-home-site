import { PortableText, type PortableTextComponents } from "@portabletext/react";
import Image from "next/image";
import { urlFor } from "@/sanity/lib/image";
import type { RichText as RT } from "@/sanity/lib/types";

const components: PortableTextComponents = {
  types: {
    image: ({ value }) =>
      value?.asset ? (
        <Image className="rt-img" src={urlFor(value).width(1200).url()} alt={value.alt || ""} width={1200} height={750} />
      ) : null,
  },
  marks: {
    link: ({ children, value }) => (
      <a href={value?.href} target="_blank" rel="noopener noreferrer">{children}</a>
    ),
  },
};

export function RichText({ value }: { value?: RT }) {
  if (!value?.length) return null;
  return <div className="rt"><PortableText value={value} components={components} /></div>;
}
