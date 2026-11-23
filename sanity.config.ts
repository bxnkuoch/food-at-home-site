"use client";
import { defineConfig, type InitialValueResolverContext } from "sanity";
import { structureTool } from "sanity/structure";
import { visionTool } from "@sanity/vision";
import { apiVersion, dataset, projectId } from "./sanity/env";
import { schemaTypes, singletonTypes } from "./sanity/schemaTypes";
import { structure } from "./sanity/structure";

export default defineConfig({
  name: "cronch",
  title: "Food at Home – Content",
  basePath: "/studio",
  projectId,
  dataset,
  schema: {
    types: schemaTypes,
    // Hide "create new" for one-off documents like Site Settings and Privacy Policy
    templates: (templates) => [
      ...templates.filter(({ schemaType }) => !singletonTypes.has(schemaType)),
      {
        id: "task-for-post",
        title: "Task in this status post",
        schemaType: "task",
        parameters: [{ name: "postId", type: "string" }],
        value: async ({ postId }: { postId: string }, { getClient, currentUser }: InitialValueResolverContext) => {
          const me = await getClient({ apiVersion: "2025-10-01" }).fetch(
            `*[_type == "teamMember" && lower(email) == lower($email)][0]._id`,
            { email: currentUser?.email ?? "" },
          );
          return {
            status: "closed",
            statusPost: { _type: "reference", _ref: postId },
            ...(me ? { contributors: [{ _type: "contribution", _key: Math.random().toString(36).slice(2, 10), member: { _type: "reference", _ref: me } }] } : {}),
          };
        },
      },
    ],
  },
  plugins: [structureTool({ structure }), visionTool({ defaultApiVersion: apiVersion })],
});
