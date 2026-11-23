import type { StructureResolver } from "sanity/structure";

const API = "2025-10-01";

export const structure: StructureResolver = (S, context) => {
  const email = context.currentUser?.email ?? "";
  return S.list()
    .title("Content")
    .items([
      S.listItem()
        .title("My tasks")
        .id("myTasks")
        .child(
          S.documentList()
            .title("My tasks")
            .apiVersion(API)
            .schemaType("task")
            .filter(`_type == "task" && count(contributors[member->email != null && lower(member->email) == lower($email)]) > 0`)
            .params({ email })
            .defaultOrdering([{ field: "dueDate", direction: "desc" }])
            .initialValueTemplates([S.initialValueTemplateItem("task")]),
        ),
      S.listItem()
        .title("Tasks by status post")
        .id("tasksByPost")
        .child(
          S.documentTypeList("statusPost")
            .title("Pick a status post")
            .defaultOrdering([{ field: "publishedAt", direction: "desc" }])
            .child((postId) =>
              S.documentList()
                .title("Tasks")
                .apiVersion(API)
                .schemaType("task")
                .filter(`_type == "task" && statusPost._ref == $postId`)
                .params({ postId })
                .initialValueTemplates([S.initialValueTemplateItem("task-for-post", { postId })]),
            ),
        ),
      S.documentTypeListItem("task").title("All tasks"),
      S.documentTypeListItem("meeting").title("Meetings"),
      S.divider(),
      S.documentTypeListItem("statusPost").title("Status Posts"),
      S.documentTypeListItem("teamMember").title("Team"),
      S.documentTypeListItem("faq").title("FAQs"),
      S.divider(),
      S.listItem().title("Site Settings & Download").id("siteSettings")
        .child(S.document().schemaType("siteSettings").documentId("siteSettings")),
      S.listItem().title("Privacy Policy").id("privacyPolicy")
        .child(S.document().schemaType("privacyPolicy").documentId("privacyPolicy")),
    ]);
};
