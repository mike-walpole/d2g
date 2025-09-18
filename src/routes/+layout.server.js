/** @type {import('./$types').LayoutServerLoad} */
export async function load({ locals }) {
	// Pass geolocation data from server hooks to the client
	// This data was already processed in hooks.server.js
	const geolocation = locals.geolocation || {
		country: '',
		city: '',
		region: '',
		detectedLanguage: 'en',
		isChineseRegion: false
	};

	console.log('📤 Layout server load - sending geolocation to client:', geolocation);

	return {
		geolocation: {
			...geolocation,
			timestamp: new Date().toISOString()
		}
	};
}
