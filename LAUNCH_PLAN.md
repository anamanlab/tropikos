# Launch Plan — Trópikos Arquitetos (Website)

> Prepared using the `launch`, `cro`, `conversion-tracking`, and `site-launch-qa` skills.
> Primary conversion: WhatsApp inquiry (G-7KB6VK4D5Y). Goal: public launch of the new site.

## 0. Readiness Gate (SLC)

Before any announcement, confirm the site is a complete, lovable, single experience — not a stub.

- [ ] **Simple** — one clear job: showcase projects + studio + services + contact. Done.
- [ ] **Lovable** — a visitor would choose to browse it (typography, photography, motion all on-brand). Verify on mobile + Safari + in-app browsers (Instagram, WhatsApp).
- [ ] **Complete** — no "TBD", lorem ipsum, or placeholder photography in production. ⚠️ README flags mock Unsplash photography and a placeholder studio still — **replace with confirmed project/studio photography before public launch** (sources in `src/assets/projects/CREDITS.md`).
- [ ] Not polishing past the bar (Stealth Mode) and not still adding scope ("Just One More Feature").

**Blockers to clear before launch:**
- Replace placeholder photography (CREDITS.md).
- Set `SITE_URL` in `astro.config.mjs` + `public/robots.txt` to `https://tropikos.com.br` (currently set — verify).
- Legal pages: privacy policy (LGPD) + cookie notice if using GA4 — **missing, add before launch**.
- OG image final (`/og-image.png`).

## 1. Channels (ORB)

### Owned
- **Instagram** `@tropikosarq` — primary rented→owned funnel. Every post links to site.
- **Email list** — currently none. Decision: start a small list (studio updates + new projects) OR rely on Instagram DMs. Recommendation: capture emails via a simple "receba novos projetos" on contato page (lead magnet: project lookbook PDF).
- **Website itself** — the portfolio IS the asset.

### Rented
- Instagram (primary), LinkedIn (optional, for B2B/real-estate developers).

### Borrowed
- Architecture/design blogs (ArchDaily BR, Casa Vogue, Casa Cláudia) — pitch a project feature.
- Local press (Diário de Pernambuco, JC) — "estúdio recifense".
- Influencer/creator partnerships with interior-design accounts.
- Podcast guest spots on architecture/entrepreneurship shows.

## 2. Five-Phase Launch

### Phase 1 — Internal (done-ish)
- [x] Site built, deployed, GA4 live.
- [ ] Stakeholders (Bruno Ícaro, Sílvio Melo Jr.) review final copy + photography.
- [ ] Internal bug list cleared.

### Phase 2 — Alpha (soft launch, current)
- [ ] Share workers.dev / staging link with 5–10 trusted clients/peers for feedback.
- [ ] Collect feedback on navigation, project pages, contact flow.
- [ ] Fix critical issues.

### Phase 3 — Beta (teasers)
- [ ] Instagram teasers: 3 posts over 2 weeks (sneak peeks of new site, "em breve", behind-the-scenes of studio).
- [ ] Story polls: "qual projeto você quer ver primeiro?".
- [ ] Email/DM to past clients: "novo site, venha ver".

### Phase 4 — Early access
- [ ] Leak screenshots + a 30s reel of the site (hero video + project bands).
- [ ] Publish a "making of" post (design system, photography).
- [ ] Invite early-access list (if email list exists) to view before public.

### Phase 5 — Full launch (launch day)
See checklist below.

## 3. Site Launch QA (from site-launch-qa reference)

### Before the switch
- [ ] Every page exists with final copy (index, projetos, [id], estudio, servicos, contato, 404).
- [ ] Crawl for broken internal links + missing images (`pnpm build` already validates assets).
- [ ] Legal pages present: **privacy policy (LGPD) + cookie notice** — ❗ missing, add.
- [ ] Contact details match (email, phone, address, hours) — verified in `site.config.ts`.
- [ ] Forms: no forms (WhatsApp CTA) — conversion = WhatsApp click. Test: click "Falar no WhatsApp" → opens wa.me with pre-filled message. ✅
- [ ] Conversion tracking fires on click (not button submit) — GA4 `whatsapp_click` event. ✅ (verify in DebugView)
- [ ] Analytics installed once, on every page — GA4 gtag in BaseHead. ✅ (verify on all 16 pages)
- [ ] Consent banner — ❗ not present; decide on LGPD compliance before launch.
- [ ] SEO: unique title/meta/H1 per page — verify.
- [ ] Canonical tags point to production domain (`tropikos.com.br`) — ✅ (Astro.site set).
- [ ] Staging noindex, production not noindex — verify robots.txt + meta robots.
- [ ] robots.txt allows indexing; sitemap lists production URLs — ✅ (sitemap-index.xml).
- [ ] Structured data validates (ArchitecturalService JSON-LD) — test in Rich Results Test.
- [ ] Core Web Vitals acceptable on mobile — run Lighthouse.
- [ ] Pages work on mobile, Safari, in-app browsers (Instagram, WhatsApp) — test.
- [ ] OG images/titles render when shared — test with opengraph.xyz / Twitter Card Validator.
- [ ] Rollback plan: `cf deploy` promotes previous? Know how to redeploy previous build (keep last `dist/` backup) — document.

### At the switch
- [ ] Deploy redirects if any (none for new site, but ensure apex↔www redirect).
- [ ] HTTPS on every hostname; one redirects to the other.
- [ ] Load top 10 pages, check content + title + canonical + 200.
- [ ] Submit one real WhatsApp click → confirm GA4 event arrives.
- [ ] Submit sitemap in Google Search Console + Bing Webmaster Tools.
- [ ] Re-check production isn't noindex.

### First two weeks
- [ ] Search Console: watch coverage + 404s daily week 1, then weekly.
- [ ] Compare traffic/conversions page-by-page vs. baseline.
- [ ] Confirm GA4 conversions arrive at expected rate.
- [ ] Fix internal links pointing at redirected URLs.
- [ ] Collect bugs, triage.

## 4. Launch Day Checklist

- [ ] Final deploy (`pnpm run deploy`) with all fixes.
- [ ] Announcement post on Instagram (hero reel + "novo site no ar" + link in bio).
- [ ] Instagram Story with link sticker to site.
- [ ] WhatsApp broadcast to past clients (personalized, not mass spam): "novo site, venha conhecer".
- [ ] Email to any list (if exists).
- [ ] Blog post: "Como projetamos" / "O estúdio em 2026" (optional).
- [ ] In-app/website banner: none needed (new site IS the announcement).
- [ ] Team ready to respond to DMs/inquiries within 1h.
- [ ] Monitor GA4 Realtime + Search Console.
- [ ] Monitor for errors (Cloudflare analytics, browser console).

## 5. Post-Launch (first 30 days)

- [ ] Onboarding flow for new inquiries (already in contato page: "Envie endereço, fotos, prazo").
- [ ] Follow up with engaged prospects within 24h.
- [ ] Roundup post: "o que mudou no site" (Instagram).
- [ ] Comparison/positioning content: "arquitetura autoral no Recife" landing page for SEO.
- [ ] Interactive demo: Navattic walkthrough of a project (optional).
- [ ] Gather feedback (Google Form or DM), act on top 3 issues.
- [ ] Plan next launch moment (new project publication, Instagram milestone, etc.).

## 6. Open Items / Decisions Needed

1. **Photography**: replace Unsplash mocks with real project photos (CREDITS.md) before public launch.
2. **Legal**: add privacy policy + cookie consent (LGPD) given GA4.
3. **Email capture**: decide whether to add a "receba novos projetos" lead magnet on contato page.
4. **Consent banner**: decide on LGPD consent mode for GA4.
5. **Domain**: confirm `tropikos.com.br` apex↔www redirect and DNS TTL.
6. **Product Hunt**: not recommended for an architecture studio site (B2B local, not tech product). Skip unless repositioning as a tool.

## 7. Success Metrics (first 90 days)

- GA4: sessions, unique visitors, bounce rate.
- Conversions: `whatsapp_click` count, `phone_click`, `email_click`.
- Instagram: profile visits → site clicks (link in bio).
- Search Console: impressions/clicks for "arquiteto recife", "arquitetura recife", project-specific queries.
- Inquiries received via WhatsApp/email (manual count).
- Target: ≥1 qualified inquiry/week from site within 60 days.

## 8. Timeline (suggested)

| Week | Milestone |
|------|-----------|
| 1 | Clear blockers (photos, legal, consent). Internal review. |
| 2 | Alpha: soft launch to 5–10 trusted contacts. Fix issues. |
| 3 | Beta: Instagram teasers (3 posts). Early-access invites. |
| 4 | Full launch (launch day checklist). |
| 5–6 | Post-launch: feedback, fixes, Search Console monitoring. |
| 7–8 | Comparison/SEO content, first case study post. |
| 9–12 | Iterate on conversion (CRO test ideas), quarterly review. |
