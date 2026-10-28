import assert from 'node:assert/strict';
import { readFile, stat } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import test from 'node:test';
import {
  markdownPathCandidates,
  notFoundMarkdown,
  prefersMarkdown,
} from '../src/worker.ts';

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

async function builtHtml(relativePath) {
  return readFile(path.join(dist, relativePath), 'utf8');
}

function schemaNodes(html) {
  const blocks = [
    ...html.matchAll(
      /<script[^>]+type="application\/ld\+json"[^>]*>([\s\S]*?)<\/script>/gi,
    ),
  ].map((match) => JSON.parse(match[1]));

  return blocks.flatMap((block) => (Array.isArray(block['@graph']) ? block['@graph'] : [block]));
}

function visibleText(html) {
  return html
    .replace(/<script[\s\S]*?<\/script>/gi, ' ')
    .replace(/<style[\s\S]*?<\/style>/gi, ' ')
    .replace(/<[^>]+>/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();
}

test('explicit text/markdown wins over HTML; wildcards stay HTML', () => {
  assert.equal(prefersMarkdown('text/markdown'), true);
  assert.equal(prefersMarkdown('text/markdown, text/html;q=0.9'), true);
  assert.equal(prefersMarkdown('text/html, text/markdown;q=0.9'), false);
  assert.equal(prefersMarkdown('text/html'), false);
  assert.equal(prefersMarkdown('*/*'), false);
  assert.equal(prefersMarkdown('text/markdown;q=0'), false);
  assert.equal(prefersMarkdown(null), false);
});

test('Markdown lookup covers root, trailing slashes, and directory indexes', () => {
  assert.deepEqual(markdownPathCandidates('/'), ['/index.md']);
  assert.deepEqual(markdownPathCandidates('/estudio/'), [
    '/estudio.md',
    '/estudio/index.md',
  ]);
  assert.deepEqual(markdownPathCandidates('/projetos'), [
    '/projetos.md',
    '/projetos/index.md',
  ]);
  assert.deepEqual(markdownPathCandidates('/favicon.ico'), []);
});

test('Markdown 404 body explains the error and links to agent resources', () => {
  const body = notFoundMarkdown('/some-missing-page');
  assert.ok(body.length > 20);
  assert.match(body, /\/some-missing-page/);
  assert.match(body, /llms\.txt/);
  assert.match(body, /llms-full\.txt/);
  assert.match(body, /sitemap-index\.xml/);
});

test('llms.txt includes explicit when-to-use guidance and agent instructions', async () => {
  const llms = await readFile(path.join(root, 'public/llms.txt'), 'utf8');
  assert.match(llms, /## When to use this site/);
  assert.match(llms, /Projeto arquitetônico residencial/);
  assert.match(llms, /tropikosarquitetura@gmail\.com/);
  assert.match(llms, /Accept: text\/markdown/);
  assert.match(llms, /\/estudio/);
  assert.match(llms, /\/contato/);
  assert.match(llms, /\/privacidade/);
});

test('llms.txt does not direct agents to the retired English slugs', async () => {
  const llms = await readFile(path.join(root, 'public/llms.txt'), 'utf8');
  // Naming the retired slugs is fine (it documents the 301); pointing at them
  // as a resource is not.
  for (const retired of ['/about', '/contact', '/privacy']) {
    assert.ok(
      !llms.includes(`tropikos.com.br${retired}`),
      `llms.txt links agents to the retired ${retired}`,
    );
  }
});

test('retired English slugs redirect to their Portuguese twins', async () => {
  const redirects = await readFile(path.join(root, 'public/_redirects'), 'utf8');
  const pairs = [
    ['/about', '/estudio'],
    ['/contact', '/contato'],
    ['/privacy', '/privacidade'],
  ];

  for (const [from, to] of pairs) {
    for (const suffix of ['', '/']) {
      const rule = new RegExp(`^${from}${suffix}\\s+${to}${suffix}\\s+301$`, 'm');
      assert.match(redirects, rule, `missing 301 ${from}${suffix} -> ${to}${suffix}`);
    }
  }
});

test('built output: homepage negotiates to a nonempty Markdown mirror', async (t) => {
  if (!(await exists(path.join(dist, 'index.md')))) {
    return t.skip('Run `pnpm build` before the build-output tests.');
  }

  const markdown = await readFile(path.join(dist, 'index.md'), 'utf8');
  assert.ok(markdown.length > 500);
  assert.match(markdown, /Trópikos/);
  assert.match(markdown, /Arquitetura/);
  assert.match(markdown, /llms\.txt/);
});

test('built output: homepage has Organization identity with contactPoint and address', async (t) => {
  if (!(await exists(path.join(dist, 'index.html')))) {
    return t.skip('Run `pnpm build` before the build-output tests.');
  }

  const html = await builtHtml('index.html');
  const organization = schemaNodes(html).find(
    (node) =>
      node['@type'] === 'Organization' ||
      (Array.isArray(node['@type']) && node['@type'].includes('Organization')),
  );

  assert.ok(organization, 'Organization JSON-LD node');
  assert.ok(organization.contactPoint, 'contactPoint');
  assert.equal(organization.address?.['@type'], 'PostalAddress');
  assert.equal(organization.address?.addressLocality, 'Recife');
});

test('built output: homepage title and H1 name the brand and the product', async (t) => {
  if (!(await exists(path.join(dist, 'index.html')))) {
    return t.skip('Run `pnpm build` before the build-output tests.');
  }

  const html = await builtHtml('index.html');
  const title = html.match(/<title>([\s\S]*?)<\/title>/i)?.[1] ?? '';
  assert.match(title, /Trópikos Arquitetos/);
  assert.match(title, /Arquitetura e Interiores no Recife/);
  assert.match(html, /arquitetura e interiores no Recife/i);
});

test('built output: trust anchors have at least 500 characters of main content', async (t) => {
  if (!(await exists(path.join(dist, 'estudio/index.html')))) {
    return t.skip('Run `pnpm build` before the build-output tests.');
  }

  for (const slug of ['estudio', 'contato', 'privacidade']) {
    const html = await builtHtml(`${slug}/index.html`);
    const main = html.match(/<main\b[^>]*>([\s\S]*?)<\/main>/i)?.[1] ?? html;
    const text = visibleText(main);
    assert.ok(text.length >= 500, `${slug} main content is only ${text.length} characters`);
    assert.ok(
      await exists(path.join(dist, slug, 'index.md')),
      `${slug} has a Markdown mirror`,
    );
  }
});

test('built output: llms-full.txt aggregates every generated page', async (t) => {
  if (!(await exists(path.join(dist, 'llms-full.txt')))) {
    return t.skip('Run `pnpm build` before the build-output tests.');
  }

  const full = await readFile(path.join(dist, 'llms-full.txt'), 'utf8');
  assert.ok(full.length > 5000);
  assert.match(full, /Trópikos Arquitetos/);
  assert.match(full, /https:\/\/tropikos\.com\.br\/llms\.txt/);
});
