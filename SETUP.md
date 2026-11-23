# Setting up the new status-post site on Sanity

Sanity is a "headless" CMS: it stores and edits content, but it doesn't host a website.
This project pairs it with a Next.js site (already built here) that you host for free on Vercel.

Time needed: about 30 minutes. Free tiers cover everything.

## 1. Put the code on GitHub (Ben)
1. Create an empty repo, e.g. `team-cronch/food-at-home-site` (or a `website/` folder in your app repo).
2. Copy this folder in, then:
   ```bash
   git init && git add . && git commit -m "Website scaffold" && git branch -M main
   git remote add origin https://github.com/<you>/<repo>.git && git push -u origin main
   ```

## 2. Create the Sanity project (Ben)
1. Sign up / log in at https://www.sanity.io (GitHub or Google login is fine).
2. In the folder run `npm install`, then `npx sanity init --env .env.local`.
   Choose **Create new project**, name it "Food at Home", dataset **production** (public).
   This writes `NEXT_PUBLIC_SANITY_PROJECT_ID` and `NEXT_PUBLIC_SANITY_DATASET` into `.env.local`.
   (Or create the project at https://www.sanity.io/manage and copy the ID into `.env.local` by hand, using `.env.example` as the template.)
3. Load the starter content: `npm run seed`
4. `npm run dev`, open http://localhost:3000/studio, and log in. You should see the three status posts.

## 3. Invite the team (Ben)
1. https://www.sanity.io/manage → your project → **Members** → invite all 8 teammates as **Editors**.
   The free plan includes up to 20 seats, so everyone can edit (unlike Framer's 3-editor limit).
2. In the Studio → **Team**, open each person and set their **email** to the one they log in to Sanity with.
   That powers **My tasks** and auto-fills them as the owner when they add a task. Add photos and roles too;
   they show in the "Meet the team" section and on task cards.

## 4. Deploy the website (Ben)
1. Go to https://vercel.com, sign in with GitHub, **Add New → Project**, pick the repo.
2. Add the environment variables `NEXT_PUBLIC_SANITY_PROJECT_ID` and `NEXT_PUBLIC_SANITY_DATASET`.
3. Deploy. You get a URL like `food-at-home.vercel.app`.
4. Back in Sanity Manage → **API → CORS origins**, add that URL (and `http://localhost:3000`) with **Allow credentials** checked, so the Studio works at `<your-url>/studio`.

## 5. Fill in the real content (team)
- **Status posts:** the seed has each post's tasks, owners and dates. Paste the full descriptions, deliverable links, takeaways, meeting notes and images from Framer into each task.
- **Site Settings & Download:** add the public TestFlight link (App Store Connect → TestFlight → External testing → Public link), logo and hero image.
- **Privacy Policy:** every section is marked DRAFT. Rewrite it to match what the app really collects (phone number, receipts sent to an AI parser, Supabase storage) before you publish.
- **FAQs:** edit the drafts; tick "Show on home page" for up to 5.

## 6. Optional
- Custom domain: Vercel → Project → Settings → Domains.
- Switch the Framer link in your syllabus/Discord to the new URL, then retire the Framer page.

## How a status post gets written (every two weeks)
Tasks and meetings are their own documents that point at a status post, so everyone can add theirs at the
same time without overwriting each other.

1. **PM creates the post:** Studio → Status Posts → **+** → Title ("Status Post 04"), *Generate* slug, date,
   the date range it covers, summary → **Publish**.
2. **Everyone adds their tasks:** Studio → **My tasks** → **+**. The new task is already linked to the newest
   status post with you as the owner. Pick Closed / Open / New, a category, add your hours, description,
   deliverable links, takeaways and images. Add teammates under "Who worked on it" with their own hours → **Publish**.
   - Task carried over from last post (e.g. Open → Closed)? Create a new task in the new post rather than
     editing the old one, so the old post stays accurate. (Use the "Duplicate" action from the ⋯ menu to save typing.)
3. **Meeting notes:** Studio → Meetings → **+** (also defaults to the newest post).
4. The post page totals everything automatically: tasks closed, hours logged, hours per person and per category.
   It's live about a minute after each Publish.

To see or edit everything in one post: Studio → **Tasks by status post** → pick the post.
