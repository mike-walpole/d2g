import { writable, derived } from 'svelte/store';
import { browser } from '$app/environment';

// Language store
export const currentLanguage = writable('en');

// Config data store (translations, cargo types)
export const configData = writable(null);

// API base URL from deployed AWS infrastructure
export const apiBaseUrl = writable('https://9u6shrsot7.execute-api.ap-east-1.amazonaws.com');

// Load config data from AWS
export async function loadConfig(language = 'en') {
	if (!browser) return;
	
	try {
		const apiUrl = await new Promise(resolve => {
			apiBaseUrl.subscribe(url => resolve(url))();
		});
		
		const response = await fetch(`${apiUrl}/config?type=all&lang=${language}`);
		const data = await response.json();
		
		if (data.success) {
			configData.set(data);
			return data;
		} else {
			console.error('Failed to load config:', data.error);
			return null;
		}
	} catch (error) {
		console.error('Error loading config:', error);
		return null;
	}
}

// Derived store for translations
export const translations = derived(
	[configData, currentLanguage],
	([$configData, $currentLanguage]) => {
		return $configData?.translations || {};
	}
);

// Derived store for cargo types
export const cargoTypes = derived(
	configData,
	($configData) => {
		return $configData?.cargoTypes || [];
	}
);

// Helper function to get translation
export function t(key, fallback = '') {
	let translation = fallback;
	const unsubscribe = translations.subscribe(trans => {
		const keys = key.split('.');
		let current = trans;
		for (const k of keys) {
			if (current && typeof current === 'object' && k in current) {
				current = current[k];
			} else {
				current = fallback;
				break;
			}
		}
		translation = current;
	});
	unsubscribe(); // Immediately unsubscribe to avoid memory leaks
	return translation;
}

// Language switcher
export function switchLanguage(lang) {
	currentLanguage.set(lang);
	loadConfig(lang);
	
	// Store language preference
	if (browser) {
		localStorage.setItem('preferred-language', lang);
	}
}

// Initialize language from localStorage
if (browser) {
	const savedLang = localStorage.getItem('preferred-language') || 'en';
	currentLanguage.set(savedLang);
	loadConfig(savedLang);
}
