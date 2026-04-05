// @ts-check
import { defineConfig } from 'astro/config';
import tailwindcss from '@tailwindcss/vite';
import vercel from '@astrojs/vercel';
import mdx from '@astrojs/mdx';
import d2 from 'astro-d2';

export default defineConfig({
  output: 'server',
  adapter: vercel({ middlewareMode: 'edge' }),
  vite: {
    plugins: [tailwindcss()],
  },
  integrations: [
    d2({
      skipGeneration: true,
      theme: {
        default: '0',
        dark: '200',
      },
      pad: 40,
      sketch: false,
      inline: true,
    }),
    mdx(),
  ],
});
