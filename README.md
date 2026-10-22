# Trópikos Arquitetos

Website for **Trópikos Arquitetos**, an architecture and interiors studio in Recife, Pernambuco. Built as a type-driven architectural monograph: paper white, a single onyx ink, one weight, no radius, no shadows, no chromatic color on the page.

- **Studio:** Rua Ferreira Lopes, 334 — Salas 201/202/203, Parnamirim, Recife — PE, 52060-235
- **Contact:** tropikosarquitetura@gmail.com · +55 81 99302-0201
- **Instagram:** [@tropikosarq](https://www.instagram.com/tropikosarq/)
- **Links:** [linktr.ee/tropikosarq](https://linktr.ee/tropikosarq)
- **Founded:** 2021

## Stack

- [Astro 7](https://astro.build) — static output, content collections, image optimization
- [Tailwind CSS 4](https://tailwindcss.com) — via `@tailwindcss/vite`
- Self-hosted Inter + JetBrains Mono through the Astro Fonts API
- `@astrojs/sitemap`, JSON-LD `ArchitecturalService`, OG/Twitter metadata
- Cloudflare Workers static assets — deployed with the `cf` CLI
- No client framework, no runtime CSS-in-JS, no analytics

## Local development

```bash
pnpm install
pnpm dev        # http://localhost:4321
pnpm build      # astro check + static build to dist/
pnpm preview    # serve dist/
```

Node 22+ and pnpm are required.

## Structure

```text
src/
  assets/                 optimizable images (projects, brand)
  components/             Header, MenuOverlay, Footer, ProjectBand, ProjectRow, BaseHead
  content/projects/       one Markdown file per project
  layouts/BaseLayout.astro
  pages/                  index, projetos, estudio, servicos, contato, 404
  styles/global.css       the design system (tokens + primitives)
  site.config.ts          brand, contact, navigation, services copy
public/
  media/                  hero reel cuts, posters, studio still
  favicon*, site.webmanifest, og-image.png, robots.txt
.agents/skills/           installed design + accessibility skills
```

## Editing projects

Each project is a Markdown file in `src/content/projects/`. Example frontmatter:

```yaml
---
title: Casa Boa Viagem
subtitle: Uma casa que respira pelo pátio
location: Boa Viagem, Recife
year: 2025
typology: Residência
scope: ['Arquitetura', 'Interiores', 'Obra']
summary: One-sentence summary used in metadata and the project header.
cover: ../../assets/projects/casa-boa-viagem/cover.jpg
coverAlt: Pátio central da Casa Boa Viagem
gallery:
  - ../../assets/projects/casa-boa-viagem/01.jpg
  - ../../assets/projects/casa-boa-viagem/02.jpg
galleryAlt:
  - Fachada moderna com volumes brancos e madeira
  - Mesa de jantar junto à cozinha, com madeira e vidro
featured: true
order: 1
---
```

- `cover`, `gallery`, and `poster` are optional. Without them the site renders the intentional technical-grid placeholder instead of a broken image.
- Set `featured: true` for the three projects that appear as full-bleed bands on the home page.
- `video` accepts a path under `public/` (for example `/media/casa-boa-viagem.mp4`).
- Astro converts covers and gallery images to WebP at responsive widths. Prefer source images of at least 2000px on the long edge.
- Add `galleryAlt` alongside `gallery` so each image has a descriptive alternative.

> **Placeholder notice:** the project photography currently in `src/assets/projects/` is mock material from Unsplash, plus real frames from the studio reel for Cozinha Espinheiro. It is meant to show the finished layout and must be replaced with confirmed project photography before public launch. Sources are documented in [`src/assets/projects/CREDITS.md`](src/assets/projects/CREDITS.md). The hero reel in `public/media/hero-tropikos-*` is a real Trópikos asset.

## Instagram media

Bulk Instagram access is blocked from this server's IP (login wall, 401/429). The download toolchain is installed and ready:

- `ffmpeg` — video transcode and poster frames
- `gallery-dl`, `instaloader`, `yt-dlp` in `/home/civo/tools/venv`
- Playwright + Chromium at `/home/civo/tools/igrab`

To download the profile after providing an authenticated `sessionid` cookie:

```bash
IG_SESSIONID='<cookie value>' ./scripts/ig-fetch.sh
```

Files land in `media/instagram/` (git-ignored). Select the best frames, copy them into `src/assets/projects/<slug>/`, and reference them from the project Markdown. Then transcode any reel to H.264 MP4 (no audio, faststart) before placing it in `public/media/`.

A logged-in session is the only reliable route: Instagram serves a login wall to anonymous datacenter traffic. If you have the account credentials instead, `instaloader --login tropikosarq` also works.

## Design system

`DESIGN.md` holds the source measurements for the visual language. `src/styles/global.css` implements it:

- `--color-paper #ffffff`, `--color-onyx #191919`, `--color-concrete #6b6b6b` (text-safe), `--color-hairline #191919`
- 11 / 15 / 21 / 32 / 62 px type scale; display tracking −0.05em; single 400 weight
- 0px radius, no shadows, hairline rules only
- `.wordmark` is sized to overflow the viewport and crop on both edges
- `.band` is the full-bleed dark project surface
- `.inverse` lifts secondary ink to `#a6a6a6` so captions stay AA on onyx
- The home hero renders a responsive poster first. The video source is attached after load, fades in on `playing`, and is never requested when `prefers-reduced-motion: reduce` is set. Mobile uses a 4:5 cut; desktop uses 16:9.
- Motion is limited to a 1.02 image scale on hover, a menu rise, and the reel. All of it is disabled under `prefers-reduced-motion`.

## Quality checks

```bash
pnpm build
pnpm preview
# accessibility (axe-core, WCAG 2.2 AA)
node /home/civo/tools/igrab/axe.mjs
# design anti-pattern detector
.agents/skills/impeccable/scripts/impeccable detect http://localhost:4321 --json
```

Installed skills: `impeccable`, `design-taste-frontend`, `frontend-design-direction`, `accessibility`. Their lock data is in `skills-lock.json`.

## Deployment

Live: **https://tropikos-arquitetos.optivoo-edu.workers.dev/**

The site is a static build deployed as a Cloudflare Worker with static assets. It is managed by the official `cf` CLI, not Wrangler commands:

- `cloudflare.config.ts` — Worker name, compatibility date, asset routing, 404 page.
- `wrangler.config.ts` — tells the cf Wrangler bundler to package `dist/`.

```bash
pnpm run deploy       # astro check + build, then cf deploy
pnpm run deploy:dry   # same, but validate without uploading
```

`cf` beta cannot build Astro 6+ directly yet. The project uses cf's Wrangler bundler for the static output: `pnpm run deploy` runs the Astro build first, then `cf deploy` packages and uploads `dist/`. You do not need to run Wrangler directly.

First-time setup:

```bash
pnpm install
cf auth login
```

Set the production URL in `astro.config.mjs` (`SITE_URL`) and `public/robots.txt`; canonical, OG, and sitemap URLs derive from `SITE_URL`. The Worker name is in `cloudflare.config.ts`; the account's workers.dev subdomain is `optivoo-edu`.
