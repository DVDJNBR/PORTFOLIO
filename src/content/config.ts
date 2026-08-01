import { defineCollection, z } from 'astro:content';

const projects = defineCollection({
  type: 'content',
  schema: z.object({
    order: z.number(),
    title: z.string(),
    description: z.string(),
    url: z.string().url(),
    tags: z.array(z.string()),
    briefNumber: z.number().optional(),
    githubRepo: z.string().optional(),
  }),
});

export const collections = { projects };
