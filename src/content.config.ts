import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
import { z } from 'astro/zod';

const projects = defineCollection({
  loader: glob({ base: './src/content/projects', pattern: '**/*.md' }),
  schema: ({ image }) =>
    z.object({
      title: z.string(),
      subtitle: z.string().optional(),
      location: z.string(),
      year: z.number(),
      typology: z.string(),
      category: z.enum(['construido', 'projeto', 'comercial', 'reforma']).default('projeto'),
      scope: z.array(z.string()).default([]),
      summary: z.string().max(400),
      cover: image().optional(),
      coverAlt: z.string().optional(),
      gallery: z.array(image()).default([]),
      galleryAlt: z.array(z.string()).default([]),
      video: z.string().optional(),
      poster: image().optional(),
      featured: z.boolean().default(false),
      order: z.number().default(99),
      draft: z.boolean().default(false),
      area: z.string().optional(),
      photography: z.string().optional(),
    }),
});

export const collections = { projects };
