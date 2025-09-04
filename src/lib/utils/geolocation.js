/**
 * Geolocation utilities for language detection
 */

// Free IP geolocation APIs for client-side fallback
const GEOLOCATION_APIS = [
	{
		name: 'ipapi.co',
		url: 'https://ipapi.co/json/',
		transform: (data) => data?.country_code
	},
	{
		name: 'ipify + ipinfo.io', 
		url: 'https://ipinfo.io/json',
		transform: (data) => data?.country
	},
	{
		name: 'ipgeolocation.io',
		url: 'https://api.ipgeolocation.io/ipgeo?apiKey=free',
		transform: (data) => data?.country_code2
	}
];

/**
 * Detect country code using client-side geolocation APIs
 * @returns {Promise<string|null>} Two-letter country code or null
 */
export async function detectCountryClient() {
	// Try each API until one works
	for (const api of GEOLOCATION_APIS) {
		try {
			console.log(`🌍 Trying ${api.name} for geolocation...`);
			
			const response = await fetch(api.url, {
				method: 'GET',
				headers: {
					'Accept': 'application/json',
				},
			});
			
			if (response.ok) {
				const data = await response.json();
				const countryCode = api.transform(data);
				
				if (countryCode) {
					console.log(`✅ ${api.name} detected country:`, countryCode);
					return countryCode.toUpperCase();
				}
			}
		} catch (error) {
			console.warn(`❌ ${api.name} failed:`, error.message);
			continue;
		}
	}
	
	console.warn('⚠️ All geolocation APIs failed, using default language');
	return null;
}

/**
 * Get language based on country code
 * @param {string} countryCode - Two-letter country code
 * @returns {string} Language code ('zh' for China, 'en' for others)
 */
export function getLanguageFromCountry(countryCode) {
	if (!countryCode) return 'en';
	
	const country = countryCode.toUpperCase();
	
	// Chinese-speaking regions
	const chineseCountries = ['CN', 'HK', 'MO', 'TW', 'SG'];
	
	if (chineseCountries.includes(country)) {
		console.log(`🇨🇳 Country ${country} maps to Chinese`);
		return 'zh';
	} else {
		console.log(`🌐 Country ${country} maps to English`);
		return 'en';
	}
}

/**
 * Comprehensive geolocation detection with multiple fallbacks
 * @returns {Promise<string>} Detected language ('en' or 'zh')
 */
export async function detectLanguageFromGeolocation() {
	try {
		// Try client-side detection
		const countryCode = await detectCountryClient();
		
		if (countryCode) {
			return getLanguageFromCountry(countryCode);
		}
		
		console.log('📍 Geolocation detection failed, using English as default');
		return 'en';
		
	} catch (error) {
		console.error('💥 Error in geolocation detection:', error);
		return 'en'; // Safe fallback
	}
}