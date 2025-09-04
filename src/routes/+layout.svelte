<script>
	import '../app.css';
	import favicon from '$lib/assets/favicon.svg';
	import { Header, HeaderNav, HeaderNavItem, Button, SkipToContent } from 'carbon-components-svelte';
	// Removed carbon icons to avoid import issues
	import { currentLanguage, translations, switchLanguage, t } from '$lib/stores/config.js';
	import { onMount } from 'svelte';
	import { page } from '$app/stores';
	import { detectLanguageFromGeolocation } from '$lib/utils/geolocation.js';
	import { getDomainLanguage, shouldOverrideGeolocation, getDomainMetadata } from '$lib/utils/domain.js';
	import { browser } from '$app/environment';

	let { children } = $props();
	
	// Domain-specific metadata
	let domainMetadata = $state({ title: '', description: '' });
	
	$effect(() => {
		if (browser) {
			const hostname = window.location.hostname;
			domainMetadata = getDomainMetadata(hostname);
		}
	});
	
	onMount(async () => {
		if (!browser) return;
		
		const hostname = window.location.hostname;
		console.log('🌐 Current domain:', hostname);
		
		// Check for user language preferences first
		const userPreference = localStorage.getItem('preferred-language');
		const userOverride = localStorage.getItem('language-override');
		
		// Check if domain should override geolocation
		const domainOverride = shouldOverrideGeolocation(hostname);
		const domainLanguage = getDomainLanguage(hostname);
		
		let finalLanguage = null;
		
		if (domainOverride) {
			// Domain-specific language (e.g., .cn always Chinese, .pl always English)
			console.log(`🎯 Domain ${hostname} forces language:`, domainLanguage);
			finalLanguage = domainLanguage;
		} else if (userOverride && userPreference) {
			// User has manually set preference
			console.log('🔧 User has manually overridden language:', userPreference);
			finalLanguage = userPreference;
		} else {
			// Use geolocation detection
			let detectedLanguage = null;
			
			// Try server-side geolocation first (Vercel headers)
			const geolocationData = $page.data?.geolocation;
			
			if (geolocationData?.detectedLanguage) {
				console.log('🌍 Server-side geolocation detected:', geolocationData.detectedLanguage);
				detectedLanguage = geolocationData.detectedLanguage;
			} else {
				// Fallback to client-side geolocation
				console.log('📍 Server-side geolocation not available, trying client-side...');
				detectedLanguage = await detectLanguageFromGeolocation();
				console.log('🔍 Client-side geolocation detected:', detectedLanguage);
			}
			
			finalLanguage = detectedLanguage || domainLanguage || 'en';
			
			if (detectedLanguage) {
				localStorage.setItem('language-geolocation', detectedLanguage);
			}
		}
		
		// Apply the determined language
		if (finalLanguage) {
			console.log('✅ Final language decision:', finalLanguage);
			switchLanguage(finalLanguage);
		}
		
		// Initialize config loading with current language
		import('$lib/stores/config.js').then(module => {
			module.loadConfig($currentLanguage);
		});
	});
	
	// Enhanced language switching with override tracking
	function handleLanguageSwitch(lang) {
		console.log('🔄 User manually switched to language:', lang);
		switchLanguage(lang);
		// Mark that user has manually chosen a language (override geolocation)
		localStorage.setItem('language-override', 'true');
		localStorage.setItem('preferred-language', lang);
	}
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
	<title>{domainMetadata.title || t('site_title', 'Dock2Gdansk') + ' - ' + t('site_tagline', 'Professional Cargo Transportation')}</title>
	<meta name="description" content={domainMetadata.description || t('site_description', 'Reliable, efficient, and professional shipping services connecting Asia to Europe')} />
	<meta property="og:title" content={domainMetadata.title || t('site_title', 'Dock2Gdansk')} />
	<meta property="og:description" content={domainMetadata.description || t('site_description', 'Reliable, efficient, and professional shipping services connecting Asia to Europe')} />
	<meta property="og:type" content="website" />
	{#if browser}
		<meta property="og:url" content={window.location.href} />
	{/if}
</svelte:head>

<Header company="Dock2Gdansk" platformName={t('site_tagline', 'Professional Cargo Transportation')}>
	<HeaderNav>
		
		<HeaderNavItem onclick={() => handleLanguageSwitch('en')} text={t('EN', 'EN')} />
		<HeaderNavItem onclick={() => handleLanguageSwitch('zh')} text={t('中文', '中文')} />
	
	
	</HeaderNav>
</Header>

<SkipToContent />

<main>
	{@render children?.()}
</main>

<footer style="background: #f1f1f1; border-top: 1px solid #ddd; padding: 32px 0;">
	<div style="max-width: 1200px; margin: 0 auto; padding: 0 16px; text-align: center;">
		<p style="font-size: 14px; color: #666;">
			{t('footer.copyright', '© 2024 Dock2Gdansk. All rights reserved.')}
		</p>
		<div style="display: flex; justify-content: center; gap: 16px; margin-top: 8px;">
			<a href="/privacy" style="font-size: 14px; color: #0043ce; text-decoration: none;">
				{t('footer.privacy', 'Privacy Policy')}
			</a>
			<a href="/terms" style="font-size: 14px; color: #0043ce; text-decoration: none;">
				{t('footer.terms', 'Terms of Service')}
			</a>
		</div>
	</div>
</footer>

<style>
	:global(.language-btn.active) {
		background-color: var(--cds-button-primary);
		color: var(--cds-text-on-color);
	}
	
	main {
	min-height: calc(100vh - 200px);
}

:global(.bx--header) {
	position: fixed !important;
	top: 0 !important;
	z-index: 1000 !important;
}

/* Fix dropdown to show only one chevron */
:global(.bx--select__arrow) {
	display: none !important;
}

:global(.bx--select-input) {
	background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 20 20'%3e%3cpath stroke='%236b7280' stroke-linecap='round' stroke-linejoin='round' stroke-width='1.5' d='M6 8l4 4 4-4'/%3e%3c/svg%3e") !important;
	background-position: right 12px center !important;
	background-repeat: no-repeat !important;
	background-size: 16px 16px !important;
}
</style>
