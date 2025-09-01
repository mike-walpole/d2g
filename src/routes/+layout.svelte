<script>
	import '../app.css';
	import favicon from '$lib/assets/favicon.svg';
	import { Header, HeaderNav, HeaderNavItem, Button, SkipToContent } from 'carbon-components-svelte';
	// Removed carbon icons to avoid import issues
	import { currentLanguage, translations, switchLanguage, t } from '$lib/stores/config.js';
	import { onMount } from 'svelte';

	let { children } = $props();
	
	onMount(() => {
		// Initialize config loading
		import('$lib/stores/config.js').then(module => {
			module.loadConfig($currentLanguage);
		});
	});
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
	<title>{t('site_title', 'Dock2Gdansk')} - {t('site_tagline', 'Professional Cargo Transportation')}</title>
</svelte:head>

<Header company="Dock2Gdansk" platformName={t('site_tagline', 'Professional Cargo Transportation')}>
	<HeaderNav>
		
		<HeaderNavItem onclick={() => switchLanguage('en')} text={t('EN', 'EN')} />
		<HeaderNavItem onclick={() => switchLanguage('zh')} text={t('中文', '中文')} />
	
	
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
