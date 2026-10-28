import assert from 'node:assert/strict';
import { readFile, stat } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import test from 'node:test';
import { SERVICE_AREAS } from '../src/site.config.ts';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const dist = path.join(root, 'dist');

async function exists(file) {
  try {
    await stat(file);
    return true;
  } catch {
    return false;
  }
}

async function pageHtml(slug) {
  return readFile(path.join(dist, 'atuacao', slug, 'index.html'), 'utf8');
}

function schemaNodes(html) {
  const blocks = [
    ...html.matchAll(
      /<script[^>]+type="application\/ld\+json"[^>]*>([\s\S]*?)<\/script>/gi,
    ),
  ].map((match) => JSON.parse(match[1]));

  return blocks.flatMap((block) => (Array.isArray(block['@graph']) ? block['@graph'] : [block]));
}

function mainText(html) {
  const main = html.match(/<main\b[^>]*>([\s\S]*?)<\/main>/i)?.[1] ?? '';
  return main
    .replace(/<script[\s\S]*?<\/script>/gi, ' ')
    .replace(/<style[\s\S]*?<\/style>/gi, ' ')
    .replace(/<[^>]+>/g, ' ')
    .replace(/&nbsp;/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();
}

function sentences(text) {
  return new Set(
    text
      .split(/(?<=[.!?])\s+/)
      .map((sentence) => sentence.trim().toLowerCase())
      .filter((sentence) => sentence.length > 30),
  );
}

const built = await exists(path.join(dist, 'atuacao', 'olinda', 'index.html'));

// A skipped suite reads as green, which is the wrong signal in CI. There the
// build output is required; locally the skip stays so a single `node --test`
// run does not need a fresh build.
if (!built && process.env.CI) {
  throw new Error('dist/atuacao is missing; run `pnpm build` before the service-area tests.');
}

const skip = built ? false : 'Run `pnpm build` before the service-area tests.';

test('every service area builds a page reachable from the hub', async (t) => {
  if (skip) return t.skip(skip);

  const hub = await readFile(path.join(dist, 'atuacao', 'index.html'), 'utf8');
  for (const area of SERVICE_AREAS) {
    assert.ok(await exists(path.join(dist, 'atuacao', area.slug, 'index.html')), area.slug);
    assert.match(hub, new RegExp(`href="/atuacao/${area.slug}"`), `${area.city} missing from hub`);
    for (const sibling of SERVICE_AREAS) {
      if (sibling.slug === area.slug) continue;
      const html = await pageHtml(area.slug);
      assert.match(
        html,
        new RegExp(`href="/atuacao/${sibling.slug}"`),
        `${area.city} does not link to ${sibling.city}`,
      );
    }
  }
});

test('Recife is left to the homepage instead of competing with it', async (t) => {
  if (skip) return t.skip(skip);

  assert.ok(!(await exists(path.join(dist, 'atuacao', 'recife', 'index.html'))));
});

test('each page states the Recife base and the visit arrangement', async (t) => {
  if (skip) return t.skip(skip);

  for (const area of SERVICE_AREAS) {
    const text = mainText(await pageHtml(area.slug));
    assert.match(text, /Recife/, `${area.city} never names the base city`);
    assert.match(text, /agendad|combinad/i, `${area.city} omits the visit/scheduling arrangement`);
    assert.match(text, /escopo/i, `${area.city} omits that travel cost sits in the scope`);
  }
});

// A sentence that denies the claim ("Não executamos uma obra em Olinda") is the
// opposite of a claim, so negation has to be read per sentence.
function claimingSentences(text, pattern) {
  return text
    .split(/(?<=[.!?])\s+/)
    .filter((sentence) => pattern.test(sentence))
    .filter((sentence) => !/\b(não|nunca|jamais)\b/i.test(sentence));
}

// `\b` is ASCII-only in JavaScript, so `\bGravatá\b` never matches: `á` is not
// a word character and the trailing boundary falls between two non-word chars.
// Build the boundary explicitly so every city name, accented or not, can match.
function cityClaim(city, lead, window) {
  return new RegExp(`(?:${lead})[^.]{0,${window}}${city}(?![\\p{L}])`, 'iu');
}

const officePattern = (city) => cityClaim(city, 'escritório|estúdio|sede|filial', 15);
const workPattern = (city) => cityClaim(city, 'obra|obras|construímos|executamos', 20);

test('the claim guard matches every city name, accents included', () => {
  for (const area of SERVICE_AREAS) {
    assert.ok(
      officePattern(area.city).test(`Temos escritório em ${area.city}.`),
      `the office guard never matches "${area.city}"`,
    );
    assert.ok(
      workPattern(area.city).test(`Executamos obra em ${area.city}.`),
      `the work guard never matches "${area.city}"`,
    );
  }
});

test('no page claims an office or an unearned work in the city', async (t) => {
  if (skip) return t.skip(skip);

  // Gravatá is the only served city with work in the portfolio.
  const citiesWithWork = new Set(['Gravatá']);

  for (const area of SERVICE_AREAS) {
    const text = mainText(await pageHtml(area.slug));

    // A studio, office or branch tied to the city by name is the claim the
    // studio must never make: the only address is the Recife one.
    const officeClaims = claimingSentences(text, officePattern(area.city));
    assert.deepEqual(officeClaims, [], `${area.city} implies an office there`);

    if (citiesWithWork.has(area.city)) continue;

    const workClaims = claimingSentences(text, workPattern(area.city));
    assert.deepEqual(workClaims, [], `${area.city} claims unearned local work`);
  }
});

test('every configured project renders as a card on its city page', async (t) => {
  if (skip) return t.skip(skip);

  for (const area of SERVICE_AREAS) {
    const html = await pageHtml(area.slug);
    const cards = html.match(/class="project-item project-card/g)?.length ?? 0;
    assert.equal(cards, area.projects.length, `${area.city} renders ${cards} cards`);

    for (const id of area.projects) {
      assert.ok(
        html.includes(`href="/projetos/${id}"`),
        `${area.city} is missing the card for "${id}"`,
      );
    }
  }
});

test('every project card states whether it was built', async (t) => {
  if (skip) return t.skip(skip);

  for (const area of SERVICE_AREAS) {
    const html = await pageHtml(area.slug);
    const cards = html.match(/class="project-item project-card/g)?.length ?? 0;
    const badges = [
      ...html.matchAll(
        /<span[^>]+class="caption absolute[^"]*"[^>]*>\s*(?:Construído|Projeto 3D)\s*<\/span>/g,
      ),
    ];
    assert.equal(badges.length, cards, `${area.city} has a card without a status badge`);
  }
});

test('the WhatsApp link names the city so inquiries can be traced', async (t) => {
  if (skip) return t.skip(skip);

  for (const area of SERVICE_AREAS) {
    const html = await pageHtml(area.slug);
    const links = [...html.matchAll(/href="(https:\/\/wa\.me\/[^"]+)"/g)].map((match) =>
      decodeURIComponent(match[1]),
    );
    assert.ok(
      links.some((href) => href.includes(area.city)),
      `${area.city} only links to the generic WhatsApp message`,
    );
  }
});

test('projects keep their real city instead of being relocated', async (t) => {
  if (skip) return t.skip(skip);

  for (const area of SERVICE_AREAS) {
    const html = await pageHtml(area.slug);
    const captions = [...html.matchAll(/<p class="caption text-concrete mt-1">([\s\S]*?)<\/p>/g)].map(
      (match) => match[1].replace(/<[^>]+>/g, ' ').trim(),
    );

    for (const caption of captions) {
      assert.match(
        caption,
        /—\s*[A-Z]/,
        `project card in ${area.city} has no explicit location: "${caption}"`,
      );
      if (area.city !== 'Gravatá') {
        assert.doesNotMatch(
          caption,
          new RegExp(area.city),
          `project card relocated to ${area.city}: "${caption}"`,
        );
      }
    }
  }
});

test('city copy is not a template with the name swapped', async (t) => {
  if (skip) return t.skip(skip);

  const sets = new Map();
  for (const area of SERVICE_AREAS) {
    sets.set(area.slug, sentences(mainText(await pageHtml(area.slug))));
  }

  const slugs = [...sets.keys()];
  for (let i = 0; i < slugs.length; i += 1) {
    for (let j = i + 1; j < slugs.length; j += 1) {
      const a = sets.get(slugs[i]);
      const b = sets.get(slugs[j]);
      const shared = [...a].filter((sentence) => b.has(sentence)).length;
      const overlap = shared / Math.min(a.size, b.size);
      assert.ok(
        overlap < 0.35,
        `${slugs[i]} and ${slugs[j]} share ${(overlap * 100).toFixed(0)}% of their sentences`,
      );
    }
  }

  const descriptions = new Set(SERVICE_AREAS.map((area) => area.metaDescription));
  assert.equal(descriptions.size, SERVICE_AREAS.length, 'duplicate meta descriptions');
});

test('each page carries canonical, breadcrumb and a Service node scoped to the city', async (t) => {
  if (skip) return t.skip(skip);

  for (const area of SERVICE_AREAS) {
    const html = await pageHtml(area.slug);
    assert.match(
      html,
      new RegExp(`<link rel="canonical" href="https://tropikos\\.com\\.br/atuacao/${area.slug}/?"`),
      `${area.city} canonical`,
    );

    const nodes = schemaNodes(html);
    const trail = nodes.find((node) => node['@type'] === 'BreadcrumbList');
    assert.ok(trail, `${area.city} breadcrumb`);
    assert.equal(trail.itemListElement.length, 3);
    assert.match(trail.itemListElement[2].item, new RegExp(`/atuacao/${area.slug}/$`));

    const service = nodes.find((node) => node['@type'] === 'Service');
    assert.ok(service, `${area.city} Service node`);
    assert.equal(service['@id'], `https://tropikos.com.br/atuacao/${area.slug}/#service`);
    assert.equal(service.url, `https://tropikos.com.br/atuacao/${area.slug}/`);
    assert.equal(service.provider['@id'], 'https://tropikos.com.br/#architectural-service');
    assert.equal(service.address, undefined, `${area.city} Service node must not claim an address`);

    const served = service.areaServed.map((place) => place.name);
    assert.ok(served.includes(area.city), `${area.city} missing from areaServed`);
  }
});

test('the hub explains the model once, not per city', async (t) => {
  if (skip) return t.skip(skip);

  const hub = await readFile(path.join(dist, 'atuacao', 'index.html'), 'utf8');
  const hubText = mainText(hub);
  assert.match(hubText, /Como atendemos fora do Recife/);
  assert.match(hubText, /deslocamento/i);

  for (const area of SERVICE_AREAS) {
    assert.doesNotMatch(
      mainText(await pageHtml(area.slug)),
      /Como atendemos fora do Recife/,
      `${area.city} duplicates the shared attendance block`,
    );
  }
});

test('each page emits FAQPage markup for the answers a visitor can read', async (t) => {
  if (skip) return t.skip(skip);

  for (const area of SERVICE_AREAS) {
    const html = await pageHtml(area.slug);
    const faq = schemaNodes(html).find((node) => node['@type'] === 'FAQPage');
    assert.ok(faq, `${area.city} FAQPage node`);
    assert.equal(faq.mainEntity.length, area.faq.length, `${area.city} FAQ count`);

    const text = mainText(html);
    for (const entry of faq.mainEntity) {
      assert.equal(entry['@type'], 'Question', `${area.city} FAQ entry type`);
      assert.equal(entry.acceptedAnswer['@type'], 'Answer', `${area.city} FAQ answer type`);
      assert.ok(
        entry.acceptedAnswer.text.length > 40,
        `${area.city} answer is too thin: ${entry.name}`,
      );
      assert.ok(text.includes(entry.name), `${area.city} question is not visible: ${entry.name}`);
      assert.ok(
        text.includes(entry.acceptedAnswer.text),
        `${area.city} answer is not visible: ${entry.name}`,
      );
    }
  }
});
