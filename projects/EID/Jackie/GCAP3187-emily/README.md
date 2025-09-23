# GCAP3187 Emily — Intro + Chat Page

This folder contains a self-contained static page for the course chatbot. It bundles an Intro section and an embedded Chatbot in a single, light-themed HTML file.

- Page: `GCAP3187-emily.html`
- Config: `config.json` (single source of truth for the bot name and URL)
- Notes: `INTRO_SETUP.md` (content ideas and teacher-facing notes)

## How to use

1) Open `config.json` and update these fields:

- `botName`: Displayed heading and browser title
- `slug`: Identifier for your bot (not required by the page, but useful for consistency)
- `chatbotUrl`: Public URL to the chatbot (iframe + “Open in new tab”)
- `contactEmail` (optional): Contact to show in the intro, if desired

2) Open `GCAP3187-emily.html` in a browser.

- The page will read `config.json` at load-time to update the title, heading, and links.
- If the iframe fails due to browser restrictions, click “Open in new tab”.

3) Customise content

- Edit the intro cards (What is this, Before you start, Syllabus & learning focus) as needed.
- Keep the email usage note if you rely on email reports.

## Reuse for another course/bot

- Duplicate this folder, rename it to the new bot slug (e.g., `GCAP3056-mentor/`).
- Rename the HTML file to match (e.g., `GCAP3056-mentor.html`).
- Update `config.json` with the new `botName` and `chatbotUrl`.
- Update intro wording in the HTML.

## Hosting

- Any static host works (GitHub Pages, Netlify, Vercel, S3/CloudFront, local server).
- Ensure `config.json` is served alongside the HTML file (same folder).
- If the config does not load (404), the page still works with default values, but links/titles may be outdated.

======Github repo to host and URL =========

GitHub repo: https://github.com/tesolchina/smartLessons/tree/main/GCAPJackie

URL https://smartlessons.hkbu.tech/GCAPJackie/GCAP3187-emily.html

==========

Note: If you still have older standalone pages (e.g., `projects/Jackie/index.html` or `chatbot_embed.html`), this folder's `GCAP3187-emily.html` supersedes them. Prefer linking to this file so all changes stay in one place.

## Accessibility & privacy

- Tabs use ARIA roles and keyboard focusable buttons.
- Avoid collecting sensitive personal data in free text. The chatbot should request only the minimum needed (e.g., an email to send a report) and disclose purpose.

## Troubleshooting

- Iframe blocked: Use “Open in new tab”. Some campuses block third-party embeds.
- Config not loading: Open DevTools console; check `config.json` path and CORS. Keep it in the same directory as the HTML file.
- Broken link: Confirm `chatbotUrl` in `config.json` is reachable.

---

If you want a darker theme or brand colors, adjust the CSS variables at the top of the HTML file.
