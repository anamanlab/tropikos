#!/usr/bin/env bash
# Download @tropikosarq posts with an authenticated Instagram session.
#
#   IG_SESSIONID='<sessionid cookie>' ./scripts/ig-fetch.sh
#
# The sessionid is the value of the "sessionid" cookie for .instagram.com.
# It is never written to the repository: the cookie jar is a temp file.
set -euo pipefail

: "${IG_SESSIONID:?Set IG_SESSIONID to the sessionid cookie from instagram.com}"

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT="${1:-$ROOT/media/instagram}"
GALLERY_DL="${GALLERY_DL:-$HOME/tools/venv/bin/gallery-dl}"

if [[ ! -x "$GALLERY_DL" ]]; then
  echo "gallery-dl not found at $GALLERY_DL" >&2
  echo "Install it with: python3 -m venv ~/tools/venv && ~/tools/venv/bin/pip install gallery-dl" >&2
  exit 1
fi

mkdir -p "$OUT"
COOKIES="$(mktemp)"
trap 'rm -f "$COOKIES"' EXIT

cat > "$COOKIES" <<EOF
# Netscape HTTP Cookie File
.instagram.com	TRUE	/	TRUE	2147483647	sessionid	$IG_SESSIONID
EOF

"$GALLERY_DL" \
  --cookies "$COOKIES" \
  --directory "$OUT" \
  --filename "{date:%Y-%m-%d}_{shortcode}_{num:02}.{extension}" \
  --write-metadata \
  --sleep-request 2-5 \
  --range 1-40 \
  "https://www.instagram.com/tropikosarq/"

echo
echo "Downloaded to $OUT"
echo "Next: pick the best frames, copy them into src/assets/projects/<slug>/, and reference them in the project Markdown."
