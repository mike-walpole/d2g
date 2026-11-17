import { fail, redirect } from '@sveltejs/kit';
import {
	ALLOWED_DAYS,
	SESSION_COOKIE,
	isAuthed,
	loadStats,
	passwordMatches,
	sessionToken
} from '$lib/server/stats.js';

export async function load({ cookies, url, fetch, setHeaders }) {
	setHeaders({ 'cache-control': 'private, no-store', 'x-robots-tag': 'noindex, nofollow' });
	if (!isAuthed(cookies)) return { authed: false };

	const requested = Number(url.searchParams.get('days') ?? 30);
	const days = ALLOWED_DAYS.includes(requested) ? requested : 30;
	return { authed: true, stats: await loadStats(fetch, days) };
}

export const actions = {
	login: async ({ request, cookies }) => {
		const form = await request.formData();
		if (!passwordMatches(form.get('password'))) {
			// Slow down guessing
			await new Promise((r) => setTimeout(r, 800));
			return fail(401, { wrong: true });
		}
		cookies.set(SESSION_COOKIE, sessionToken(), {
			path: '/stats',
			httpOnly: true,
			secure: true,
			sameSite: 'strict',
			maxAge: 60 * 60 * 24 * 30
		});
		redirect(303, '/stats');
	},
	logout: async ({ cookies }) => {
		cookies.delete(SESSION_COOKIE, { path: '/stats' });
		redirect(303, '/stats');
	}
};
