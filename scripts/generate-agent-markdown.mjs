/**
 * Generate Markdown mirrors of every built HTML page.
 *
 * The Worker serves these files at the same canonical URL when a request asks
 * for `Accept: text/markdown`. Keeping the conversion in the build means the
 * Markdown can never silently drift from the pages agents are reading.
 *
 * Usage: node scripts/generate-agent-markdown.mjs (runs after `astro build`)
 */
import { readdir, readFile, writeFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import TurndownService from 'turndown';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const dist = path.join(root, 'dist');
const site = 'https://tropikos.com.br';

const pageOrder = [
  '/',
  '/about',
  '/estudio',
  '/servicos',
  '/projetos',
  '/perguntas',
  '/contact',
  '/privacy',
];

const turndown = new TurndownService({
  headingStyle: 'atx',
  bulletListMarker: '-',
  codeBlockStyle: 'fenced',
  emDelimiter: '_',
});

turndown.remove(['script', 'style', 'noscript', 'iframe', 'svg', 'video', 'source']);

function isInsideLink(node) {
  let parent = node.parentNode;
  while (parent) {
    if (parent.nodeName === 'A') return true;
    parent = parent.parentNode;
  }
  return false;
}

// Hashed image URLs are noise for agents; the alt text is the useful part.
// Images inside an anchor stay plain text so we do not generate nested links.
turndown.addRule('imageAltText', {
  filter: 'img',
  replacement: (_content, node) => {
    const alt = node.getAttribute('alt')?.trim();
    if (!alt) return '';
    return isInsideLink(node) ? `${alt} — ` : `\n\n[Imagem: ${alt}]\n\n`;
  },
});

function normalizeUrlPath(relativePath) {
  if (relativePath === 'index.html') return '/';
  if (relativePath === '404.html') return '/404';
  return `/${relativePath.replace(/\/index\.html$/, '').replace(/\.html$/, '')}`;
}

function extractMain(html) {
  const main = html.match(/<main\b[^>]*>([\s\S]*?)<\/main>/i);
  if (main) return main[1];

  const body = html.match(/<body\b[^>]*>([\s\S]*?)<\/body>/i);
  return body ? body[1] : html;
}

function extractTitle(html) {
  return html.match(/<title[^>]*>([\s\S]*?)<\/title>/i)?.[1]?.trim() ?? '';
}

async function walk(directory) {
  const entries = await readdir(directory, { withFileTypes: true });
  const files = [];

  for (const entry of entries) {
    const fullPath = path.join(directory, entry.name);
    if (entry.isDirectory()) {
      files.push(...(await walk(fullPath)));
    } else {
      files.push(fullPath);
    }
  }

  return files;
}

const htmlFiles = (await walk(dist))
  .filter((file) => file.endsWith('.html'))
  .sort((a, b) => a.localeCompare(b));

if (htmlFiles.length === 0) {
  throw new Error('No HTML files found in dist. Run `astro build` first.');
}

const pages = [];

for (const file of htmlFiles) {
  const relativePath = path.relative(dist, file).split(path.sep).join('/');
  const urlPath = normalizeUrlPath(relativePath);
  const html = await readFile(file, 'utf8');
  const main = extractMain(html);
  let markdown = turndown.turndown(main).trim();

  if (!/^#\s/m.test(markdown)) {
    const title = extractTitle(html);
    if (title) markdown = `# ${title}\n\n${markdown}`;
  }

  const footer = [
    '',
    '---',
    '',
    `Fonte: ${site}${urlPath}`,
    'Contato: tropikosarquitetura@gmail.com · +55 81 99302-0201',
    `Índice para agentes: ${site}/llms.txt`,
  ].join('\n');

  markdown = `${markdown}${footer}`.replace(/\n{3,}/g, '\n\n').trim() + '\n';

  await writeFile(file.replace(/\.html$/, '.md'), markdown);
  pages.push({ urlPath, markdown });
  console.log(`markdown ${urlPath} -> ${path.relative(root, file.replace(/\.html$/, '.md'))}`);
}

const ordered = [
  ...pageOrder
    .map((urlPath) => pages.find((page) => page.urlPath === urlPath))
    .filter(Boolean),
  ...pages.filter((page) => !pageOrder.includes(page.urlPath)),
];

const full = [
  '# Trópikos Arquitetos — conteúdo completo do site',
  '',
  '> Versão em Markdown de todas as páginas públicas. Gerada automaticamente no build.',
  '',
  ...ordered.map((page) => `\n---\n\n<!-- ${page.urlPath} -->\n\n${page.markdown}`),
].join('\n');

await writeFile(path.join(dist, 'llms-full.txt'), full);
console.log(`markdown full -> dist/llms-full.txt (${ordered.length} pages)`);
