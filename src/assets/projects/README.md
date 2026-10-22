# Project media

> **Placeholder status:** the current covers and galleries are mock imagery,
> not confirmed Trópikos project photography. They combine free Unsplash
> placeholders with frames from the studio reel. Replace them before public
> launch. Source URLs are listed in [`CREDITS.md`](./CREDITS.md).

Drop real project photography here, one folder per project slug:

```text
src/assets/projects/
  casa-boa-viagem/
    cover.jpg
    01.jpg
    02.jpg
```

Then reference the files from the project Markdown (paths are relative to
`src/content/projects/<slug>.md`):

```yaml
cover: ../../assets/projects/casa-boa-viagem/cover.jpg
gallery:
  - ../../assets/projects/casa-boa-viagem/01.jpg
```

Astro converts these to responsive WebP at build time. Prefer source images at
least 2000px on the long edge, sRGB, JPEG or PNG. Do not commit Instagram
downloads directly from `media/instagram/` without selecting and cropping the
best frames first.
