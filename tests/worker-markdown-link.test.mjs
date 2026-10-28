import assert from 'node:assert/strict';
import test from 'node:test';
import worker from '../src/worker.ts';

/**
 * Minimal stand-in for the Cloudflare Assets binding. The Worker hands it both
 * Request and URL objects, and real Assets resolve a directory URL to its
 * index.html, so the stub has to do the same. Astro's default directory format
 * writes `/servicos` as `servicos/index.html` and the Markdown mirror as
 * `servicos/index.md`, while the root is `index.md` and the 404 is `404.md` flat.
 */
function assetsFor(files) {
  const available = new Set(files);

  return {
    async fetch(source) {
      const url = source instanceof URL ? source : new URL(source.url);
      const candidates = [url.pathname];
      if (url.pathname.endsWith('/')) candidates.push(`${url.pathname}index.html`);
      if (!/\.[a-z0-9]+$/i.test(url.pathname)) candidates.push(`${url.pathname}/index.html`);

      const hit = candidates.find((candidate) => available.has(candidate));
      if (!hit) return new Response('missing', { status: 404 });

      const type = hit.endsWith('.md')
        ? 'text/markdown; charset=utf-8'
        : 'text/html; charset=utf-8';
      return new Response('<h1>body</h1>', { status: 200, headers: { 'Content-Type': type } });
    },
  };
}

const PAGES = [
  ['/', '/index.html', '/index.md'],
  ['/servicos/', '/servicos/index.html', '/servicos/index.md'],
  ['/estudio/', '/estudio/index.html', '/estudio/index.md'],
  ['/projetos/casa-brut/', '/projetos/casa-brut/index.html', '/projetos/casa-brut/index.md'],
];

for (const [path, html, markdown] of PAGES) {
  test(`Link header for ${path} advertises a Markdown URL that resolves`, async () => {
    const response = await worker.fetch(
      new Request(`https://tropikos.com.br${path}`, { headers: { Accept: 'text/html' } }),
      { ASSETS: assetsFor([html, markdown]) },
    );

    assert.equal(response.status, 200);
    const link = response.headers.get('Link');
    assert.ok(link, 'Link header present');

    const advertised = /<([^>]+)>; rel="alternate"/.exec(link)?.[1];
    assert.ok(advertised, `advertised target parsed out of: ${link}`);

    // The invariant the old code broke: whatever we advertise must be fetchable.
    const probe = await assetsFor([html, markdown]).fetch(new Request(advertised));
    assert.equal(probe.status, 200, `${advertised} advertised but does not resolve`);
    assert.match(probe.headers.get('Content-Type') ?? '', /text\/markdown/);
  });
}

test('www requests fold onto the apex host with the path and query preserved', async () => {
  const response = await worker.fetch(
    new Request('https://www.tropikos.com.br/projetos/casa-brut?utm_source=x'),
    { ASSETS: assetsFor([]) },
  );

  assert.equal(response.status, 301);
  assert.equal(
    response.headers.get('Location'),
    'https://tropikos.com.br/projetos/casa-brut?utm_source=x',
  );
});

test('workers.dev and preview hosts are not redirected to production', async () => {
  for (const host of ['tropikos-arquitetos.workers.dev', 'localhost:4321']) {
    const response = await worker.fetch(new Request(`https://${host}/servicos/`), {
      ASSETS: assetsFor(['/servicos/index.html', '/servicos/index.md']),
    });
    assert.notEqual(response.status, 301, `${host} should be served, not redirected`);
  }
});
