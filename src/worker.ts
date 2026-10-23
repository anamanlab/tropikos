/**
 * Worker entrypoint for /media/* requests.
 *
 * Workers Static Assets served directly by the platform ignore the `Range`
 * header (they return a full `200` with no `Accept-Ranges`). Desktop browsers
 * rely on range requests to stream video, so the hero film can stall and stay
 * on the poster frame.
 *
 * This Worker runs first for `/media/*` (see `worker.assets.runWorkerFirst` in
 * cloudflare.config.ts) and turns those responses into standards-compliant
 * partial content (`206`) responses. Non-media requests never invoke it.
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

const RANGE_PATTERN = /^bytes=(\d*)-(\d*)$/;
const CACHE_CONTROL = "public, max-age=86400";

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

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);

    // Defensive: the runtime only routes /media/* here, but keep the Worker
    // safe if that configuration ever changes.
    if (!url.pathname.startsWith("/media/")) {
      return env.ASSETS.fetch(request);
    }

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
  },
};
