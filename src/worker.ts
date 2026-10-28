/**
 * Worker entrypoint for agent-friendly content negotiation and media ranges.
 *
 * The site is otherwise static. This Worker runs first for every request so it
 * can:
 *
 * 1. serve a Markdown representation at the same canonical URL when an agent
 *    asks for `Accept: text/markdown` (with `Vary: Accept` so HTML and
 *    Markdown cache entries never collide);
 * 2. return a Markdown problem body for 404s requested as Markdown;
 * 3. keep byte-range playback working for the hero film under `/media/*`.
 */

interface AssetsFetcher {
  fetch(input: Request | string | URL): Promise<Response>;
}

interface Env {
  ASSETS: AssetsFetcher;
}

interface ByteRange {
  start: number;
  end: number;
}

interface MediaRange {
  type: string;
  q: number;
}

const RANGE_PATTERN = /^bytes=(\d*)-(\d*)$/;
const CACHE_CONTROL = "public, max-age=86400";
const MARKDOWN_CACHE_CONTROL = "public, max-age=300, must-revalidate";
const MARKDOWN_CONTENT_TYPE = "text/markdown; charset=utf-8";
const HTML_CONTENT_TYPE = "text/html; charset=utf-8";
const SITE_ORIGIN = "https://tropikos.com.br";
const CANONICAL_HOST = new URL(SITE_ORIGIN).host;

/** Parse a single `bytes=` range against a known file size. */
function parseRange(header: string, size: number): ByteRange | null {
  const match = RANGE_PATTERN.exec(header.trim());
  if (!match) return null;

  const startText = match[1];
  const endText = match[2];
  if (startText === "" && endText === "") return null;

  let start: number;
  let end: number;

  if (startText === "") {
    // Suffix range: `bytes=-N` (the last N bytes).
    const suffixLength = Number(endText);
    if (!Number.isInteger(suffixLength) || suffixLength <= 0) return null;
    start = Math.max(0, size - suffixLength);
    end = size - 1;
  } else {
    start = Number(startText);
    end = endText === "" ? size - 1 : Number(endText);
  }

  if (!Number.isInteger(start) || !Number.isInteger(end)) return null;
  if (start < 0 || start >= size || end < start) return null;

  return { start, end: Math.min(end, size - 1) };
}

/** Add the headers browsers and Cloudflare's cache need for range playback. */
function withMediaHeaders(source: Headers, contentType: string, cacheable = true): Headers {
  const headers = new Headers(source);
  if (!headers.get("Content-Type")) headers.set("Content-Type", contentType);
  headers.set("Accept-Ranges", "bytes");
  headers.set("Cache-Control", cacheable ? CACHE_CONTROL : "no-store");
  return headers;
}

function contentTypeFor(pathname: string): string {
  if (pathname.endsWith(".mp4")) return "video/mp4";
  if (pathname.endsWith(".webm")) return "video/webm";
  if (pathname.endsWith(".webp")) return "image/webp";
  return "application/octet-stream";
}

function bodyAllowed(status: number, method: string): boolean {
  return method !== "HEAD" && status !== 204 && status !== 205 && status !== 304;
}

/** Honour If-Range only when the validator matches the asset. */
function ifRangeMatches(request: Request, asset: Response): boolean {
  const ifRange = request.headers.get("If-Range");
  if (!ifRange) return true;

  const etag = asset.headers.get("ETag");
  if (etag && ifRange === etag) return true;

  const lastModified = asset.headers.get("Last-Modified");
  return Boolean(lastModified && ifRange === lastModified);
}

/** Split an Accept header into media ranges, preserving valid q-values. */
export function parseAcceptHeader(header: string): MediaRange[] {
  return header
    .split(",")
    .map((part) => {
      const [rawType, ...params] = part.trim().split(";");
      const type = rawType.trim().toLowerCase();
      let q = 1;

      for (const param of params) {
        const [rawKey, rawValue] = param.split("=");
        if (rawKey?.trim().toLowerCase() !== "q") continue;
        const value = Number(rawValue);
        if (Number.isFinite(value)) q = Math.max(0, Math.min(1, value));
      }

      return { type, q };
    })
    .filter((range) => range.type.length > 0);
}

/**
 * True when the request explicitly prefers Markdown over HTML.
 *
 * Wildcards alone (for example a bare wildcard Accept header from curl or a
 * browser) must keep serving HTML. Only an explicit `text/markdown` entry can
 * opt into Markdown.
 */
export function prefersMarkdown(accept: string | null): boolean {
  if (!accept) return false;

  const ranges = parseAcceptHeader(accept);
  const markdownQ = Math.max(
    0,
    ...ranges.filter((range) => range.type === "text/markdown").map((range) => range.q),
  );
  if (markdownQ <= 0) return false;

  const htmlQ = Math.max(
    0,
    ...ranges
      .filter(
        (range) =>
          range.type === "text/html" || range.type === "text/*" || range.type === "*/*",
      )
      .map((range) => range.q),
  );

  return markdownQ >= htmlQ;
}

function normalizePath(pathname: string): string {
  if (pathname === "/") return "/";
  return pathname.replace(/\/+$/, "");
}

/** Static files (including /llms.txt and /_astro/*) are never Markdown pages. */
function isAssetPath(pathname: string): boolean {
  const lastSegment = pathname.split("/").pop() ?? "";
  return lastSegment.includes(".");
}

/** Candidate Markdown asset paths for a page URL, in lookup order. */
export function markdownPathCandidates(pathname: string): string[] {
  const clean = normalizePath(pathname);
  if (clean === "/") return ["/index.md"];
  if (isAssetPath(clean)) return [];
  return [`${clean}.md`, `${clean}/index.md`];
}

function appendVary(headers: Headers, value: string): void {
  const current = headers.get("Vary");
  if (!current) {
    headers.set("Vary", value);
    return;
  }

  const values = current.split(",").map((part) => part.trim().toLowerCase());
  if (!values.includes("*") && !values.includes(value.toLowerCase())) {
    headers.set("Vary", `${current}, ${value}`);
  }
}

function copyHeaders(source: Headers): Headers {
  return new Headers(source);
}

/** The Markdown problem body used for any missing page requested as Markdown. */
export function notFoundMarkdown(pathname: string): string {
  const path = pathname || "/";
  return [
    "# 404 — Página não encontrada",
    "",
    `O caminho \`${path}\` não existe neste site.`,
    "",
    "Use um dos links abaixo para continuar:",
    "",
    `- [Início](${SITE_ORIGIN}/)`,
    `- [Índice para agentes (llms.txt)](${SITE_ORIGIN}/llms.txt)`,
    `- [Conteúdo completo para agentes (llms-full.txt)](${SITE_ORIGIN}/llms-full.txt)`,
    `- [Sitemap](${SITE_ORIGIN}/sitemap-index.xml)`,
    `- [Contato](${SITE_ORIGIN}/contato)`,
    "",
    "Se você seguiu um link antigo, o sitemap lista todas as páginas atuais.",
  ].join("\n");
}

function markdownResponse(body: BodyInit | null, status = 200): Response {
  return new Response(body, {
    status,
    headers: {
      "Content-Type": MARKDOWN_CONTENT_TYPE,
      Vary: "Accept",
      "Cache-Control": status === 200 ? MARKDOWN_CACHE_CONTROL : "no-store",
      "X-Content-Type-Options": "nosniff",
    },
  });
}

/**
 * The candidate Markdown asset that actually exists for a page URL. Astro emits
 * `/` as `index.md` and `/404` as `404.md` but every other route as
 * `<path>/index.md`, so the lookup order matters: a fixed guess would advertise
 * alternates that 404.
 */
async function lookupMarkdown(
  request: Request,
  env: Env,
  pathname: string,
): Promise<{ path: string; body: BodyInit | null } | null> {
  for (const candidate of markdownPathCandidates(pathname)) {
    const url = new URL(request.url);
    url.pathname = candidate;

    const asset = await env.ASSETS.fetch(new URL(url));
    if (!asset.ok) continue;

    return { path: candidate, body: request.method === "HEAD" ? null : asset.body };
  }

  return null;
}

async function serveMarkdown(
  request: Request,
  env: Env,
  pathname: string,
): Promise<Response | null> {
  const found = await lookupMarkdown(request, env, pathname);
  return found ? markdownResponse(found.body, 200) : null;
}

async function notFoundHtml(request: Request, env: Env): Promise<Response> {
  const url = new URL(request.url);
  url.pathname = "/404.html";
  const asset = await env.ASSETS.fetch(new URL(url));

  if (asset.ok) {
    const headers = copyHeaders(asset.headers);
    headers.set("Content-Type", HTML_CONTENT_TYPE);
    headers.set("Cache-Control", "no-store");
    appendVary(headers, "Accept");
    return new Response(request.method === "HEAD" ? null : asset.body, {
      status: 404,
      headers,
    });
  }

  const headers = new Headers({
    "Content-Type": "text/plain; charset=utf-8",
    "Cache-Control": "no-store",
  });
  appendVary(headers, "Accept");
  return new Response("404 — Página não encontrada.", { status: 404, headers });
}

async function handleMedia(request: Request, env: Env, url: URL): Promise<Response> {
  const contentType = contentTypeFor(url.pathname);

  // Fetch the complete asset and handle ranges ourselves so behaviour is
  // identical whether or not the assets binding honours Range. Conditional
  // headers (If-None-Match, If-Modified-Since) are still forwarded.
  const assetHeaders = new Headers(request.headers);
  assetHeaders.delete("Range");
  const asset = await env.ASSETS.fetch(
    new Request(request.url, { method: request.method, headers: assetHeaders }),
  );

  const headers = withMediaHeaders(asset.headers, contentType, asset.ok);

  // Pass through errors, conditional responses, and non-GET/HEAD methods.
  if (!asset.ok || request.method !== "GET" || asset.status === 206) {
    return new Response(bodyAllowed(asset.status, request.method) ? asset.body : null, {
      status: asset.status,
      statusText: asset.statusText,
      headers,
    });
  }

  const rangeHeader = request.headers.get("Range");
  if (!rangeHeader || !ifRangeMatches(request, asset)) {
    return new Response(asset.body, {
      status: asset.status,
      statusText: asset.statusText,
      headers,
    });
  }

  // Multiple ranges are not used by media elements. Serve the complete
  // response and let Cloudflare slice it if needed.
  if (rangeHeader.includes(",")) {
    return new Response(asset.body, {
      status: asset.status,
      statusText: asset.statusText,
      headers,
    });
  }

  // Never slice an encoded payload: byte offsets refer to the encoded body.
  const encoding = headers.get("Content-Encoding");
  if (encoding && encoding.toLowerCase() !== "identity") {
    return new Response(asset.body, {
      status: asset.status,
      statusText: asset.statusText,
      headers,
    });
  }
  if (encoding) headers.delete("Content-Encoding");

  const bytes = await asset.arrayBuffer();
  const size = bytes.byteLength;
  const range = parseRange(rangeHeader, size);

  if (!range) {
    return new Response(null, {
      status: 416,
      headers: {
        "Accept-Ranges": "bytes",
        "Cache-Control": "no-store",
        "Content-Range": `bytes */${size}`,
      },
    });
  }

  const { start, end } = range;
  headers.set("Content-Length", String(end - start + 1));
  headers.set("Content-Range", `bytes ${start}-${end}/${size}`);

  return new Response(bytes.slice(start, end + 1), { status: 206, headers });
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);

    // www serves byte-identical content, so fold it onto the apex instead of
    // splitting the duplicate. Scoped to the www host only so workers.dev and
    // local previews are left alone.
    if (url.host === `www.${CANONICAL_HOST}`) {
      const target = new URL(request.url);
      target.host = CANONICAL_HOST;
      target.protocol = "https:";
      return new Response(null, {
        status: 301,
        headers: { Location: target.toString(), "Cache-Control": "public, max-age=604800" },
      });
    }

    if (url.pathname.startsWith("/media/")) {
      return handleMedia(request, env, url);
    }

    const isRead = request.method === "GET" || request.method === "HEAD";
    const wantsMarkdown = isRead && prefersMarkdown(request.headers.get("Accept"));

    if (wantsMarkdown) {
      const markdown = await serveMarkdown(request, env, url.pathname);
      if (markdown) return markdown;

      // A missing static file (CSS, image, etc.) should not turn into a
      // Markdown page. Page-like URLs get the Markdown 404 body below.
      if (isAssetPath(normalizePath(url.pathname))) {
        return env.ASSETS.fetch(request);
      }

      return markdownResponse(
        request.method === "HEAD" ? null : notFoundMarkdown(url.pathname),
        404,
      );
    }

    const asset = await env.ASSETS.fetch(request);

    if (asset.status === 404) {
      return notFoundHtml(request, env);
    }

    const contentType = asset.headers.get("Content-Type") ?? "";
    if (!contentType.toLowerCase().includes("text/html")) {
      return asset;
    }

    const headers = copyHeaders(asset.headers);
    appendVary(headers, "Accept");

    // Discoverability for agents that read HTML first: point at the parallel
    // Markdown representation without changing the canonical URL. Only advertise
    // a candidate that resolved, so the alternate is never a 404.
    const markdown = await lookupMarkdown(request, env, url.pathname);
    if (markdown) {
      headers.set(
        "Link",
        `<${new URL(markdown.path, request.url).toString()}>; rel="alternate"; type="text/markdown"`,
      );
    }

    return new Response(asset.body, {
      status: asset.status,
      statusText: asset.statusText,
      headers,
    });
  },
};
