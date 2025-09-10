import { paraglideMiddleware } from '$lib/paraglide/server';
import { sequence } from '@sveltejs/kit/hooks';

// Geolocation handling middleware
const handleGeolocation = async ({ event, resolve }) => {
	try {
		// Get country from Vercel's geolocation headers
		let country = event.request.headers.get('x-vercel-ip-country') || '';
		const city = event.request.headers.get('x-vercel-ip-city') || '';
		const region = event.request.headers.get('x-vercel-ip-country-region') || '';
		
		// Development fallback: check if running locally without Vercel headers
		const url = new URL(event.request.url);
		const isDevelopment = url.hostname === 'localhost' || url.hostname === '127.0.0.1';
		const hasVercelHeaders = Boolean(country);
		
		if (!hasVercelHeaders && isDevelopment) {
			// For development, you can test different countries by visiting:
			// http://localhost:5176/?test-country=CN
			const testCountry = url.searchParams.get('test-country');
			country = testCountry || 'US'; // Default to US for development
			console.log(`🔧 Development mode - using test country: ${country}`);
		}
		
		console.log('🌍 Server hook geolocation:', { country, city, region, isDevelopment, hasVercelHeaders });
		
		// Determine language based on country
		// Chinese for China (CN), Hong Kong (HK), Macau (MO), Taiwan (TW)
		const chineseCountries = ['CN', 'HK', 'MO', 'TW'];
		const detectedLanguage = chineseCountries.includes(country) ? 'zh' : 'en';
		
		console.log(`🎯 Server hook: ${country || 'unknown'} -> ${detectedLanguage}`);
		
		// Add geolocation data to locals so it's available in load functions and components
		event.locals.geolocation = {
			country,
			city,
			region,
			detectedLanguage,
			isChineseRegion: chineseCountries.includes(country)
		};
		
	} catch (error) {
		console.error('❌ Server hook geolocation error:', error);
		
		// Fallback geolocation data
		event.locals.geolocation = {
			country: '',
			city: '',
			region: '',
			detectedLanguage: 'en',
			isChineseRegion: false
		};
	}
	
	return await resolve(event);
};

// Paraglide handling middleware
const handleParaglide = ({ event, resolve }) =>
	paraglideMiddleware(event.request, ({ request, locale }) => {
		event.request = request;

		return resolve(event, {
			transformPageChunk: ({ html }) => html.replace('%paraglide.lang%', locale)
		});
	});

// Combine both middleware functions
export const handle = sequence(handleGeolocation, handleParaglide);
