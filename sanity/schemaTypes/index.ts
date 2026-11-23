import { faq } from "./faq";
import { feature, link, richText } from "./objects";
import { privacyPolicy } from "./privacyPolicy";
import { siteSettings } from "./siteSettings";
import { statusPost } from "./statusPost";
import { meeting, task, teamMember } from "./team";

export const schemaTypes = [statusPost, task, meeting, teamMember, faq, privacyPolicy, siteSettings, richText, link, feature];
export const singletonTypes = new Set(["siteSettings", "privacyPolicy"]);
