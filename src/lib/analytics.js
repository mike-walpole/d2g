import posthog from 'posthog-js';
import { browser } from '$app/environment';
import { PUBLIC_POSTHOG_KEY, PUBLIC_POSTHOG_HOST } from '$env/static/public';

let started = false;

/**
 * Privacy posture (GDPR / PIPL):
 * - persistence: 'memory' -> nothing is written to cookies or localStorage, so no consent banner is
 *   needed; one page load = one anonymous journey, which is exactly the unit the form funnel needs.
 * - autocapture off, no session replay: only the explicit form events below are sent, and they never
 *   carry what the visitor typed (no company, email, phone or inquiry text).
 * - Traffic goes through our own domain (/pgc-e -> PostHog EU), see vercel.json.
 */
export function initAnalytics({ country = '', language = 'en' } = {}) {
	if (!browser || started) return;
	if (!PUBLIC_POSTHOG_KEY || !PUBLIC_POSTHOG_HOST) {
		throw new Error(
			'[analytics] PUBLIC_POSTHOG_KEY / PUBLIC_POSTHOG_HOST are not set - form analytics would be silently missing'
		);
	}
	posthog.init(PUBLIC_POSTHOG_KEY, {
		api_host: PUBLIC_POSTHOG_HOST,
		ui_host: 'https://eu.posthog.com',
		defaults: '2026-08-30',
		persistence: 'memory',
		autocapture: false,
		disable_session_recording: true,
		disable_surveys: true,
		person_profiles: 'identified_only'
	});
	posthog.register({ country: country || 'unknown', site_language: language });
	started = true;
}

export function setAnalyticsLanguage(language) {
	if (!started) return;
	posthog.register({ site_language: language });
}

/** @param {string} event @param {Record<string, unknown>} [props] @param {{beacon?: boolean}} [opts] */
export function track(event, props = {}, opts = {}) {
	if (!started) return;
	posthog.capture(event, props, opts.beacon ? { transport: 'sendBeacon' } : undefined);
}
