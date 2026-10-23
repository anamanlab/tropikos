# AGENTS.md

Astro 7 + Tailwind 4 static site for Trópikos Arquitetos, a pt-BR architecture portfolio. Single package (not a monorepo), pnpm + Node 22+, no client framework. `README.md` covers setup but is stale on analytics, placeholder imagery, and parts of the build pipeline; trust `package.json`, `src/components/BaseHead.astro`, and `src/assets/projects/CREDITS.md` when they conflict.

## Commands

- `pnpm install` — pnpm only; `pnpm-lock.yaml` is committed and CI uses `--frozen-lockfile`.
- `pnpm dev` — Astro at http://localhost:4321. It does not execute `src/worker.ts`, so Markdown negotiation and `/media/*` range behavior are not exercised locally.
- `pnpm check` — `astro check` (Astro/TypeScript + content schema).
- `pnpm build` — `astro check && astro build && node scripts/generate-agent-markdown.mjs`. This is the standard verification and what CI runs; it also writes `dist/**/*.md` and `dist/llms-full.txt`.
- `pnpm test` — builds, then runs `node --experimental-strip-types --test tests/*.test.mjs`. Tests cover Markdown negotiation, Markdown 404s, `llms.txt`, homepage JSON-LD/title, trust-page content, and `llms-full.txt`. CI does not run this; run it after changes to `src/worker.ts`, routes, metadata, or agent files.
- Single test (after `pnpm build`): `node --experimental-strip-types --test --test-name-pattern="Markdown lookup" tests/agent-readiness.test.mjs`.
- `pnpm preview` — serve the built `dist/`.
- `pnpm icons` — regenerate `public/icon-192.png`, `icon-512.png`, `maskable-512.png`, and `apple-touch-icon.png` from `brand-kit/svg/tropikos-symbol-white.svg`; don't hand-edit those PNGs.
- `pnpm deploy` / `pnpm deploy:dry` — build, then `cf deploy` / `cf deploy --dry-run`. Run `cf auth login` once. `cf` is the deploy CLI; do not use `wrangler deploy`.
- No lint or formatter script/config exists; match the existing style manually.

## Architecture

- `src/pages/` contains file-based routes. `src/layouts/BaseLayout.astro` wraps pages with `BaseHead`, header, footer, menu, WhatsApp float, consent banner, and skip link.
- `src/content.config.ts` defines the strict `projects` collection; content lives in `src/content/projects/*.md`. `entry.id` is the filename, so renaming a file changes its public URL.
- `src/site.config.ts` is the single source for contact details, navigation, and service copy (including `whatsappHref`). Don't duplicate contact data in pages.
- `src/styles/global.css` implements the design system with Tailwind v4 `@theme`; there is no `tailwind.config.*`. `DESIGN.md` is the reference. `@/*` maps to `src/*`.
- Fonts are self-hosted through the Astro Fonts API in `astro.config.mjs`: Inter + JetBrains Mono, weight 400 only. `DESIGN.md` names TWK Everett, but Inter/JetBrains are the shipped substitutes; don't add weights or font files.
- `src/worker.ts` runs first for every request (`cloudflare.config.ts` `runWorkerFirst: true`). It serves Markdown when `Accept` explicitly prefers `text/markdown`, adds `Vary: Accept` and a `Link` alternate, returns Markdown 404s, and handles `/media/*` byte ranges; otherwise it falls through to `env.ASSETS`. Keep that fallback and negotiation behavior.
- `scripts/generate-agent-markdown.mjs` converts built HTML into `.md` mirrors and `dist/llms-full.txt`; `public/llms.txt` is hand-written and copied into the build. Keep its page list, contact details, and project list aligned with the source pages; never edit generated `.md` files in `dist`.
- English trust pages `/about`, `/contact`, `/privacy` coexist with the Portuguese `/estudio`, `/contato`, `/privacidade`; `/perguntas` is the FAQ. They are separate pages, not redirects — keep shared facts consistent.
- `src/worker.ts` is imported directly by tests with Node's `--experimental-strip-types`; keep it to erasable TypeScript (no enums, namespaces, or parameter properties).

## Content editing

- Required frontmatter: `title`, `location`, `year` (number), `typology`, `summary` (max 400 chars). `cover` and `gallery` are optional; missing media renders the intentional technical-grid placeholder.
- Put project images under `src/assets/` and reference them relatively; `public/` files bypass Astro's responsive WebP pipeline. Keep `galleryAlt` aligned with `gallery`.
- `category` is `construido | projeto | comercial | reforma`. The `/projetos` filter UI only exposes the first three, so a `reforma` entry appears in "Todos" but has no filter button.
- Projects sort by `order` ascending; `draft: true` hides an entry from every page. The home page shows `featured: true` entries, capped at the first four by `order`.
- Project/studio media is real archive material; see `src/assets/projects/CREDITS.md`. Never invent project facts, credits, or substitute stock imagery. The README's Unsplash placeholder notice is stale.
- Renaming a project slug? Add 301s to `public/_redirects` (there is already an `apartamento-graca` → `apartamento-gracas` redirect).

## Media

- `public/media/` is deployed; root `media/` is git-ignored Instagram downloads. Don't confuse the two.
- Streamed video belongs under `/media/`; the Worker only applies range handling there. Keep video/poster pairs together.
- The home page reads both `public/media/hero-tropikos-wide.mp4` and `hero-tropikos-tall.mp4` at build time to content-hash them; missing files break `pnpm build`. Keep the matching posters and the 16:9 / 4:5 cuts.
- Media import scripts are machine-specific: `scripts/sync-all-drive-projects.mjs` needs a local Drive inventory and `gcloud` auth; `scripts/ig-fetch.sh` needs `IG_SESSIONID` and external tools. Don't wire them into CI.

## Analytics and consent

- `src/components/BaseHead.astro` loads GA4 (default `G-7KB6VK4D5Y`, override with `PUBLIC_GA_MEASUREMENT_ID`) with Consent Mode v2 defaulting to denied. `src/components/ConsentBanner.astro` persists `tropikos_consent` in a first-party cookie (shared across apex/www) and localStorage, then updates `gtag` consent. Do not add tracking or measurement that bypasses explicit consent.
- The privacy pages describe analytics and cookies; update `/privacidade` and `/privacy` together if data practices change. README's "no analytics" statement is stale.

## Design and accessibility

- Core system: monochrome paper/onyx/concrete, single 400 weight, 0 radius, no shadows, hairline rules; palm/terracotta are logo-mark colors only. Reuse `.shell`, `.caption`, `.body-copy`, `.rule-top`, `.inverse`, `.link-rule`, and `.tap`.
- Utility exceptions are the hero fallback play control, the WhatsApp FAB (WhatsApp green, rounded), and the consent banner (rounded, shadow); keep those styles isolated from page content.
- `.inverse` lifts `--color-concrete` to `#a6a6a6` for AA contrast. Keep `.tap` (24px hit area) on standalone inline links. CSS animations are disabled under `prefers-reduced-motion`; the hero video still autoplays muted and has a fallback play control, so don't add extra motion.

## Deployment

- `cloudflare.config.ts` is the real Worker config (name, compatibility date, static assets, 404, run-first routing). `wrangler.config.ts` only tells cf's bundler where `dist/` is; this is a static build, not SSR — don't add `@astrojs/cloudflare`.
- `SITE_URL` in `astro.config.mjs` and the sitemap URL in `public/robots.txt` are hardcoded together; canonical, OG, and sitemap URLs derive from `SITE_URL`. Update both if the domain changes.
- Production: https://tropikos.com.br. CI (`.github/workflows/ci.yml`) runs only `pnpm build` for pushes/PRs to `main`; run `pnpm test` locally when the change touches the Worker, SEO metadata, or agent output.
