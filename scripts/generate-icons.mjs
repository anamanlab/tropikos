import { readFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import path from 'node:path';
import sharp from 'sharp';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const symbolPath = path.join(root, 'brand-kit/svg/tropikos-symbol-white.svg');
const outDir = path.join(root, 'public');

const source = await readFile(symbolPath, 'utf8');
const symbol = source
  .replace(/^<svg[^>]*>/, '')
  .replace(/<\/svg>\s*$/, '')
  .replace(/<title[^>]*>[\s\S]*?<\/title>/g, '');

// The official app-icon composition uses this transform inside the 256-unit
// master. Keeping it preserves the mark's clear space at small sizes.
const symbolGroup = `<g transform="translate(20.1 23.93) scale(0.853)">${symbol}</g>`;

function appIcon(size, { rounded = true } = {}) {
  return `<svg xmlns="http://www.w3.org/2000/svg" width="${size}" height="${size}" viewBox="0 0 256 256">
    <rect width="256" height="256"${rounded ? ' rx="57.6"' : ''} fill="#191919"/>
    ${symbolGroup}
  </svg>`;
}

async function render(svg, size, filename) {
  await sharp(Buffer.from(svg))
    .resize(size, size)
    .png({ compressionLevel: 9 })
    .toFile(path.join(outDir, filename));
  console.log(`wrote public/${filename}`);
}

await render(appIcon(192), 192, 'icon-192.png');
await render(appIcon(512), 512, 'icon-512.png');
await render(appIcon(512, { rounded: false }), 512, 'maskable-512.png');
await render(appIcon(180, { rounded: false }), 180, 'apple-touch-icon.png');
