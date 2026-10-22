// @ts-check
import { defineConfig, fontProviders } from 'astro/config';
import sitemap from '@astrojs/sitemap';
import tailwindcss from '@tailwindcss/vite';

// Workers static site URL. Replace with the studio domain when it is connected.
const SITE_URL = 'https://tropikos-arquitetos.optivoo-edu.workers.dev';

export default defineConfig({
  site: SITE_URL,

  integrations: [sitemap()],

  prefetch: true,

  vite: {
    plugins: [tailwindcss()],
  },

  // Self-hosted at build time. A single weight across the whole range is
  // the signature of the system: hierarchy comes from scale, not weight.
  fonts: [
    {
      provider: fontProviders.google(),
      name: 'Inter',
      cssVariable: '--ff-body',
      weights: ['400'],
      styles: ['normal'],
      subsets: ['latin', 'latin-ext'],
    },
    {
      provider: fontProviders.google(),
      name: 'JetBrains Mono',
      cssVariable: '--ff-mono',
      weights: ['400'],
      subsets: ['latin', 'latin-ext'],
    },
  ],
});
