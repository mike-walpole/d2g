<script>
	import '../app.css';
	import favicon from '$lib/assets/favicon.svg';
	import {
		Header,
		HeaderNav,
		HeaderNavItem,
		Button,
		SkipToContent
	} from 'carbon-components-svelte';
	// Removed carbon icons to avoid import issues
	import { currentLanguage, translations, switchLanguage, t } from '$lib/stores/config.js';
	import { onMount } from 'svelte';
	import { page } from '$app/stores';
	import { detectLanguageFromGeolocation } from '$lib/utils/geolocation.js';
	import {
		getDomainLanguage,
		shouldOverrideGeolocation,
		getDomainMetadata
	} from '$lib/utils/domain.js';
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
			// Use server-side geolocation data from Vercel middleware
			let detectedLanguage = null;

			const serverGeolocation = $page.data?.geolocation;

			if (serverGeolocation?.detectedLanguage) {
				detectedLanguage = serverGeolocation.detectedLanguage;
				console.log(
					`🎯 Server-side geolocation: ${serverGeolocation.country || 'unknown'} -> ${detectedLanguage}`
				);

				// Store geolocation info for debugging
				if (serverGeolocation.country) {
					localStorage.setItem('user-country', serverGeolocation.country);
					localStorage.setItem('user-city', serverGeolocation.city || '');
				}
			} else {
				console.log('⚠️ Server-side geolocation not available, trying fallback...');
				// Fallback to old client-side geolocation
				detectedLanguage = await detectLanguageFromGeolocation();
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
		import('$lib/stores/config.js').then((module) => {
			module.loadConfig($currentLanguage);
		});
	});

	// Enhanced language switching with override tracking
	function handleLanguageSwitch(lang) {
		console.log('🔄 User manually switched to language:', lang);

		try {
			// Force immediate language switch
			switchLanguage(lang);

			// Mark that user has manually chosen a language (override geolocation)
			if (typeof localStorage !== 'undefined') {
				localStorage.setItem('language-override', 'true');
				localStorage.setItem('preferred-language', lang);
			}

			console.log('✅ Language switch completed:', lang);
		} catch (error) {
			console.error('❌ Language switch failed:', error);
		}
	}
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
	<title
		>{domainMetadata.title ||
			t('site_title', 'Dock2Gdansk') +
				' - ' +
				t('site_tagline', 'Professional Cargo Transportation')}</title
	>
	<meta
		name="description"
		content={domainMetadata.description ||
			t(
				'site_description',
				'Reliable, efficient, and professional shipping services connecting Asia to Europe'
			)}
	/>
	<meta property="og:title" content={domainMetadata.title || t('site_title', 'Dock2Gdansk')} />
	<meta
		property="og:description"
		content={domainMetadata.description ||
			t(
				'site_description',
				'Reliable, efficient, and professional shipping services connecting Asia to Europe'
			)}
	/>
	<meta property="og:type" content="website" />
	{#if browser}
		<meta property="og:url" content={window.location.href} />
	{/if}
</svelte:head>

<Header company="Dock2Gdansk" platformName="">
	<HeaderNav>
		<div class="language-selector">
			<HeaderNavItem
				class={`language-btn ${$currentLanguage === 'en' ? 'active' : ''}`}
				on:click={() => handleLanguageSwitch('en')}
				text={t('EN', 'EN')}
			/>
			<HeaderNavItem
				class={`language-btn ${$currentLanguage === 'zh' ? 'active' : ''}`}
				on:click={() => handleLanguageSwitch('zh')}
				text={t('中文', '中文')}
			/>
		</div>
	</HeaderNav>
</Header>

<SkipToContent />

<main>
	{@render children?.()}
</main>

<footer style="background: #f1f1f1; border-top: 1px solid #ddd; padding: 32px 0;">
	<div style="max-width: 1200px; margin: 0 auto; padding: 0 16px; text-align: center;">
		<p style="font-size: 14px; color: #666;">
			{t('footer.copyright', '© 2025 Dock2Gdansk. All rights reserved.')}
		</p>
		<div style="display: flex; justify-content: center; gap: 16px; margin-top: 8px;">
			<a
				href="https://www.portgdansk.pl"
				target="_blank"
				rel="noopener noreferrer"
				style="font-size: 14px; color: #0043ce; text-decoration: none;"
			>
				{t('footer.port_website', 'Port of Gdańsk')}
			</a>
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
	.language-selector {
		display: flex;
		gap: 8px;
		align-items: center;
	}

	:global(.language-btn) {
		min-width: 40px !important;
		padding: 8px 12px !important;
		font-size: 14px !important;
		border-radius: 4px !important;
		transition: all 0.2s ease !important;
		background-color: transparent !important;
		color: white !important;
		border: 1px solid rgba(255, 255, 255, 0.3) !important;
	}

	:global(.language-btn:hover) {
		background-color: rgba(255, 255, 255, 0.1) !important;
		border-color: rgba(255, 255, 255, 0.5) !important;
	}

	:global(.language-btn.active) {
		background-color: white !important;
		color: #0043ce !important;
		border-color: white !important;
	}

	:global(.language-btn.active:hover) {
		background-color: rgba(255, 255, 255, 0.95) !important;
		color: #0043ce !important;
	}

	main {
		min-height: calc(100vh - 200px);
	}

	:global(.bx--header) {
		position: fixed !important;
		top: 0 !important;
		z-index: 1000 !important;
	}

	/* Ensure language selector is visible on mobile */
	@media (max-width: 768px) {
		.language-selector {
			position: relative !important;
			z-index: 1001 !important;
		}

		:global(.language-btn) {
			min-width: 35px !important;
			padding: 6px 10px !important;
			font-size: 13px !important;
			margin: 0 2px !important;
		}

		/* Ensure header nav items are visible on mobile */
		:global(.bx--header__nav) {
			display: flex !important;
			align-items: center !important;
		}

		:global(.bx--header__nav-item) {
			display: inline-block !important;
			visibility: visible !important;
		}
	}

	/* Tablet adjustments */
	@media (max-width: 1024px) and (min-width: 769px) {
		:global(.language-btn) {
			min-width: 38px !important;
			padding: 7px 11px !important;
			font-size: 13px !important;
		}
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
