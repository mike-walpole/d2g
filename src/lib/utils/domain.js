/**
 * Domain-specific utilities for multi-domain setup
 */

// Domain configuration - all domains have same behavior, only branding differs
const DOMAIN_CONFIG = {
	// Primary domains - all use geolocation for language detection
	'dock2gdansk.com': {
		region: 'international',
		title: 'Dock2Gdansk - Professional Cargo Transportation',
		description: 'Reliable cargo transportation between China and Poland'
	},
	'dock2gdansk.cn': {
		region: 'china',
		title: 'Dock2Gdansk - Professional Cargo Transportation',
		description: 'Reliable cargo transportation between China and Poland'
	},
	'dock2gdansk.pl': {
		region: 'poland',
		title: 'Dock2Gdansk - Professional Cargo Transportation',
		description: 'Reliable cargo transportation between China and Poland'
	}
	// Add more domains as needed - all will use geolocation
};

/**
 * Get domain configuration based on current hostname
 * @param {string} hostname - Current hostname (e.g., 'dock2gdansk.com')
 * @returns {Object} Domain configuration
 */
export function getDomainConfig(hostname) {
	// Remove www prefix if present
	const cleanDomain = hostname.replace(/^www\./, '');

	// Return specific config or default
	return DOMAIN_CONFIG[cleanDomain] || DOMAIN_CONFIG['dock2gdansk.com'];
}

/**
 * Check if domain should override geolocation
 * @param {string} hostname - Current hostname
 * @returns {boolean} Always false - all domains use geolocation
 */
export function shouldOverrideGeolocation(hostname) {
	// All domains now use geolocation-based language detection
	return false;
}

/**
 * Get default language for domain (fallback only)
 * @param {string} hostname - Current hostname
 * @returns {string} Always 'en' as default fallback
 */
export function getDomainLanguage(hostname) {
	// All domains use the same fallback language
	return 'en';
}

/**
 * Get domain-specific metadata
 * @param {string} hostname - Current hostname
 * @returns {Object} Title and description for meta tags
 */
export function getDomainMetadata(hostname) {
	const config = getDomainConfig(hostname);
	return {
		title: config.title,
		description: config.description,
		region: config.region
	};
}
