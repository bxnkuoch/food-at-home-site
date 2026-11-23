# Food at Home website (Next.js + Sanity)

One project that contains both the public website and the Sanity Studio (the editor), served at `/studio`.

- Content types: **Status Post**, **Task** and **Meeting** (each its own document linked to a post, so every teammate adds their own), **Team Member**, **FAQ**, **Privacy Policy**, **Site Settings & Download** (hero text, feature cards, TestFlight / App Store / Play links).
- Studio extras: a **My tasks** list for whoever is logged in, **Tasks by status post**, and new tasks pre-filled with the newest post and you as owner.
- Status post pages compute stat tiles (closed, hours, open, new), hours per person and per category, and show owner avatars on each task.
- Pages: `/` home, `/status`, `/status/<slug>`, `/faq`, `/privacy`, `/download`, `/studio`.
- `seed/seed.ndjson` holds starter content: the 8 team members, the three Framer status posts with their 71 tasks (titles, owners, dates, hours where known, a guessed category) and meeting list, six draft FAQs, a draft privacy policy, and site settings. Regenerate it with `python3 seed/generate_seed.py seed/seed.ndjson`.

See `SETUP.md` for the step-by-step setup.

## Local development
```bash
npm install
cp .env.example .env.local   # fill in your Sanity project ID
npm run dev                  # site: http://localhost:3000  studio: http://localhost:3000/studio
```
Published content shows on the live site within about 60 seconds.
