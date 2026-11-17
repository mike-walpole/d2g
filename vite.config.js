import { paraglideVitePlugin } from '@inlang/paraglide-js';
import tailwindcss from '@tailwindcss/vite';
import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
	plugins: [
		tailwindcss(),
		sveltekit(),
		paraglideVitePlugin({
			project: './project.inlang',
			outdir: './src/lib/paraglide'
		})
	],
	server: {
		// Mirrors the PostHog rewrites in vercel.json so /pgc-e works in dev too
		proxy: {
			'/pgc-e/static': {
				target: 'https://eu-assets.i.posthog.com',
				changeOrigin: true,
				rewrite: (p) => p.replace(/^\/pgc-e/, '')
			},
			'/pgc-e/array': {
				target: 'https://eu-assets.i.posthog.com',
				changeOrigin: true,
				rewrite: (p) => p.replace(/^\/pgc-e/, '')
			},
			'/pgc-e': {
				target: 'https://eu.i.posthog.com',
				changeOrigin: true,
				rewrite: (p) => p.replace(/^\/pgc-e/, '')
			}
		}
	}
});
