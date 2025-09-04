export async function load({ request, getClientAddress }) {
	// Comprehensive geolocation debug information
	const headers = request.headers;
	const clientIP = getClientAddress();
	
	// Collect all possible geolocation headers
	const geolocationData = {
		clientIP: clientIP,
		timestamp: new Date().toISOString(),
		headers: {
			// Vercel headers
			'x-vercel-ip-country': headers.get('x-vercel-ip-country'),
			'x-vercel-ip-city': headers.get('x-vercel-ip-city'),
			'x-vercel-ip-latitude': headers.get('x-vercel-ip-latitude'),
			'x-vercel-ip-longitude': headers.get('x-vercel-ip-longitude'),
			
			// Cloudflare headers (if using Cloudflare)
			'cf-ipcountry': headers.get('cf-ipcountry'),
			'cf-ipcity': headers.get('cf-ipcity'),
			
			// Other common headers
			'x-forwarded-for': headers.get('x-forwarded-for'),
			'x-real-ip': headers.get('x-real-ip'),
			'user-agent': headers.get('user-agent'),
			'accept-language': headers.get('accept-language'),
		},
		detectedCountry: headers.get('x-vercel-ip-country') || headers.get('cf-ipcountry'),
		detectedLanguage: null
	};
	
	// Determine language from detected country
	if (geolocationData.detectedCountry) {
		const country = geolocationData.detectedCountry.toUpperCase();
		const chineseCountries = ['CN', 'HK', 'MO', 'TW', 'SG'];
		geolocationData.detectedLanguage = chineseCountries.includes(country) ? 'zh' : 'en';
	}
	
	return {
		geolocation: geolocationData
	};
}