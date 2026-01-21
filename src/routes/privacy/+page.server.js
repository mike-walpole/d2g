import { redirect } from '@sveltejs/kit';

/** @type {import('./$types').PageServerLoad} */
export async function load({ locals, url }) {
	const geolocation = locals.geolocation || {};

	// Check if user has manually overridden location (via cookie or query param)
	const forceRegion = url.searchParams.get('region');

	// If user explicitly wants non-China version, don't redirect
	if (forceRegion === 'global') {
		console.log('📍 Privacy: User explicitly requested global version');
		return {};
	}

	// Redirect Chinese users to China-specific privacy policy
	if (geolocation.isChineseRegion || forceRegion === 'china') {
		console.log('🇨🇳 Privacy: Redirecting Chinese user to /privacy/china');
		throw redirect(302, '/privacy/china');
	}

	console.log('🌐 Privacy: Showing global version for', geolocation.country || 'unknown');
	return {};
}
