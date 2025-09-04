import { browser } from '$app/environment';

export async function load({ request }) {
	// Get geolocation data from Vercel headers
	let detectedLanguage = 'en'; // Default to English
	
	try {
		// Vercel provides geolocation information in headers
		const country = request.headers.get('x-vercel-ip-country') || 
		                request.headers.get('cf-ipcountry') || // Cloudflare fallback
		                null;
		
		console.log('🌍 Detected country from headers:', country);
		
		// Set language based on country
		if (country === 'CN') {
			detectedLanguage = 'zh';
			console.log('🇨🇳 User from China - setting language to Chinese');
		} else {
			detectedLanguage = 'en';
			console.log('🌐 User from other country - setting language to English');
		}
		
	} catch (error) {
		console.error('❌ Error detecting geolocation:', error);
		detectedLanguage = 'en'; // Fallback to English
	}
	
	return {
		geolocation: {
			detectedLanguage,
			timestamp: new Date().toISOString()
		}
	};
}