# SEO & AI Search Research — Trópikos Arquitetos

> Research conducted using `seo-audit`, `ai-seo`, `local-seo`, `content-strategy`, `site-architecture`, `schema`, and `analytics` skills + web research (Archsplace Recife directory, CAU/BR, competitor sites, common client questions).

## 1. Keyword Landscape (Brazil / Recife)

### Primary (high intent, local)
| Keyword | Intent | Target page | Difficulty |
|---------|--------|-------------|------------|
| arquiteto Recife | transactional | Home / Estúdio | High |
| arquitetura Recife | informational | Home | High |
| escritório de arquitetura Recife | transactional | Home / Estúdio | Medium |
| projeto arquitetônico Recife | transactional | Serviços | Medium |
| arquitetura de interiores Recife | transactional | Serviços | Medium |
| reforma apartamento Recife | transactional | Serviços / FAQ | Medium |
| arquiteto para reforma Recife | transactional | Serviços | Low-Med |

### Long-tail (lower volume, higher conversion)
| Keyword | Target page |
|---------|-------------|
| casa em Boa Viagem projeto arquitetônico | Project pages (location field) |
| apartamento interiores Rosarinho | Project pages |
| quanto custa projeto arquitetônico Recife | FAQ / Serviços |
| como escolher arquiteto Recife | FAQ |
| arquitetura clima tropical Recife | Content (thought leadership) |
| projeto executivo o que é | FAQ |
| arquiteto para reforma apartamento Recife | Serviços / FAQ |

### Branded
- Trópikos Arquitetos, Trópikos arq, tropikosarq (Instagram)

### AI-search query patterns (how people ask assistants)
- "melhor arquiteto no Recife para casa"
- "quanto custa contratar arquiteto em Recife"
- "como funciona projeto arquitetônico"
- "arquiteto que acompanha obra Recife"
- "escritório arquitetura Recife interiores"

## 2. Competitor Landscape (Recife)

From Archsplace directory (7 listed architects in Recife) + web:
- Francisco Vagner de Oliveira (UFPE, institucional/patrimônio) — R$25+
- Artur Paes (residencial/comercial/interiores) — R$125+
- Renato Menezes (10+ anos, residencial/comercial)
- Fernanda Santps (4 anos, interiores/decoração) — R$450+
- Larissa Emanuelle (UNICAP 2020, interiores)
- Mariana Batista (UFPE, espaços únicos)
- Fernanda A. Queiroz (UFPE 2003, hospitalar/shopping/residencial)

**Competitive gaps we can exploit:**
- Most competitors have thin, templated sites or only directory profiles — few have a strong authored portfolio site with case studies. Our monograph-style site + project detail pages is a differentiator.
- Few publish process/FAQ content → opportunity for long-tail + AI citations.
- Most don't have structured data (schema) or llms.txt → we're ahead.
- Local SEO (GBP) — unknown if competitors have optimized profiles; likely inconsistent. First-mover advantage.

## 3. Top 5 Priorities (SEO + AI Search)

### Priority 1 — Google Business Profile (Local SEO)
**Why:** 32% of local ranking weight. Dominates "arquiteto Recife" map pack. Highest ROI for a local studio.
**Action:** Create/claim GBP, complete all fields, photos, services, hours, Q&A, booking link → WhatsApp. Weekly posts. Target ≥10 reviews in 6 months.
**Skill:** `local-seo` (profile-and-citations reference).

### Priority 2 — FAQ page (AI extraction + long-tail SEO)
**Why:** Captures decision-stage queries ("quanto custa", "como escolher", "como funciona"). AI assistants heavily cite FAQ-style content. Low competition in PT-BR architecture niche.
**Action:** ✅ Created `/perguntas` with 13 Q&As + FAQPage schema. Add internal links from servicos/contato/home. Add to footer nav.
**Skill:** `ai-seo` (content-patterns), `seo-audit`.

### Priority 3 — Project pages as SEO landing pages
**Why:** Each project targets "[typology] em [bairro]" long-tail with near-zero competition. 16 projects = 16 landing pages.
**Action:** Ensure each project page has unique title/meta including location + typology; add "Gostou? Vamos conversar" CTA (✅ done); add internal links from servicos/home; add BreadcrumbList schema (✅). Consider adding a short narrative per project (already have summary + Content).
**Skill:** `seo-audit` (on-page), `cro`.

### Priority 4 — Process/how-to content (authority + AI citations)
**Why:** "Como funciona um projeto arquitetônico", "Como escolher um arquiteto" — high AI citation potential, establishes authority, feeds the funnel.
**Action:** Publish 2–3 long-form pieces (serviços expansion, "como escolher arquiteto", "arquitetura no clima de Recife"). Use direct 40–60 word answer blocks, statistics with sources, expert attribution (CAU numbers).
**Skill:** `content-strategy`, `ai-seo` (content-patterns).

### Priority 5 — Third-party presence (AI citations + authority)
**Why:** AI assistants cite third-party sources (Houzz, ArchDaily, Google Business Profile, Instagram). Shortlist recommendations depend on web-wide consensus.
**Action:** Consistent NAP + description across Instagram, Houzz, ArchDaily, Google Business Profile. Authentic participation in local/architecture communities. Get 1–2 project features in local press or ArchDaily.
**Skill:** `ai-seo` (Pillar 3: Presence), `link-building`.

## 4. FAQ Content (Brazil-specific)

Created `/perguntas` with 13 questions covering:
- O que faz um arquiteto?
- Por que contratar um arquiteto e não só um engenheiro ou designer?
- Quanto custa um projeto arquitetônico?
- Como funciona o processo?
- Quanto tempo leva?
- Vocês acompanham a obra?
- Trabalham com reformas de apartamento?
- Atendem quais cidades/regiões?
- É obrigatório ter arquiteto?
- O que é projeto executivo?
- Como escolher um arquiteto?
- Vocês fazem interiores?
- Como solicitar um orçamento?

Each answer is 40–60 words (optimal for AI snippet extraction) and leads with a direct answer. FAQPage JSON-LD included (semantic value; Google rich results retired May 2026 but still useful for AI parsers and other consumers).

## 5. Implementation Status

| Item | Status |
|------|--------|
| FAQ page `/perguntas` | ✅ Created |
| FAQPage JSON-LD | ✅ |
| BreadcrumbList schema | ✅ (serviços, contato, estúdio, projetos) |
| Person schema (founders) | ✅ (estúdio) |
| ArchitecturalService JSON-LD (geo, hours) | ✅ |
| llms.txt | ✅ |
| Project detail CTA | ✅ |
| Google Business Profile | ⏳ Needs creation (your action) |
| NAP citation cleanup | ⏳ Needs manual audit |
| Content pieces (how-to, case study) | ⏳ To be written |
| Third-party listings (Houzz, ArchDaily) | ⏳ To be created |

## 6. Next Steps

1. Review the FAQ page copy; adjust tone/pricing if needed.
2. Create Google Business Profile (highest priority).
3. Write first content piece: "Como funciona um projeto arquitetônico do início ao fim" (expand serviços).
4. Add internal links: home → /perguntas, servicos → /perguntas, contato → /perguntas.
5. Add /perguntas to footer "Navegar" list.
6. Submit sitemap to Search Console + Bing.
7. Set up monthly AI citation tracking (spreadsheet, top 20 queries).

Say "implement" and I'll add the internal links + footer link + deploy. Or tell me which item to tackle first.