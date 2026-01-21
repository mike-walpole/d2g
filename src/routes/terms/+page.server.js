import { redirect } from '@sveltejs/kit';

/** @type {import('./$types').PageServerLoad} */
export async function load({ locals, url }) {
	const geolocation = locals.geolocation || {};

	// Check if user has manually overridden location (via cookie or query param)
	const forceRegion = url.searchParams.get('region');

	// If user explicitly wants non-China version, don't redirect
	if (forceRegion === 'global') {
		console.log('📍 Terms: User explicitly requested global version');
		return {};
	}

	// Redirect Chinese users to China-specific terms
	if (geolocation.isChineseRegion || forceRegion === 'china') {
		console.log('🇨🇳 Terms: Redirecting Chinese user to /terms/china');
		throw redirect(302, '/terms/china');
	}

	console.log('🌐 Terms: Showing global version for', geolocation.country || 'unknown');
	return {};
}
