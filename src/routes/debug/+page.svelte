<script>
	import { onMount } from 'svelte';
	import { detectLanguageFromGeolocation, detectCountryClient } from '$lib/utils/geolocation.js';
	import { currentLanguage, t } from '$lib/stores/config.js';
	import { page } from '$app/stores';

	let geolocationResults = {
		serverSide: null,
		clientSide: null,
		detectedCountry: null,
		detectedLanguage: null,
		currentLanguage: null,
		userPreferences: {},
		timestamp: new Date().toISOString()
	};

	let loading = true;

	onMount(async () => {
		// Get server-side geolocation
		geolocationResults.serverSide = $page.data?.geolocation || 'Not available';

		// Test client-side geolocation
		try {
			geolocationResults.detectedCountry = await detectCountryClient();
			geolocationResults.detectedLanguage = await detectLanguageFromGeolocation();
		} catch (error) {
			console.error('Client-side geolocation failed:', error);
			geolocationResults.detectedCountry = 'Failed';
			geolocationResults.detectedLanguage = 'Failed';
		}

		// Get current language
		geolocationResults.currentLanguage = $currentLanguage;

		// Get user preferences
		geolocationResults.userPreferences = {
			savedLanguage: localStorage.getItem('preferred-language'),
			userOverride: localStorage.getItem('language-override'),
			geolocationLanguage: localStorage.getItem('language-geolocation')
		};

		loading = false;
	});

	function clearPreferences() {
		localStorage.removeItem('preferred-language');
		localStorage.removeItem('language-override');
		localStorage.removeItem('language-geolocation');
		alert('Preferences cleared! Refresh the page to test geolocation again.');
	}

	function testGeolocation() {
		location.reload();
	}
</script>

<svelte:head>
	<title>Geolocation Debug - Dock2Gdansk</title>
</svelte:head>

<div style="max-width: 800px; margin: 100px auto 50px; padding: 20px; font-family: monospace;">
	<h1 style="color: #0043ce; margin-bottom: 30px;">🌍 Geolocation Debug Page</h1>

	{#if loading}
		<div style="padding: 20px; background: #f0f8ff; border-radius: 8px;">
			<p>🔍 Testing geolocation detection...</p>
		</div>
	{:else}
		<div style="display: grid; gap: 20px;">
			<!-- Server-side Results -->
			<div
				style="padding: 20px; background: #f0f8ff; border-radius: 8px; border-left: 4px solid #0043ce;"
			>
				<h3 style="margin: 0 0 15px 0; color: #0043ce;">
					🖥️ Server-side Detection (Vercel Headers)
				</h3>
				<pre
					style="background: #ffffff; padding: 15px; border-radius: 4px; overflow-x: auto;">{JSON.stringify(
						geolocationResults.serverSide,
						null,
						2
					)}</pre>
			</div>

			<!-- Client-side Results -->
			<div
				style="padding: 20px; background: #f0fdf4; border-radius: 8px; border-left: 4px solid #22c55e;"
			>
				<h3 style="margin: 0 0 15px 0; color: #16a34a;">🌐 Client-side Detection (IP APIs)</h3>
				<div style="background: #ffffff; padding: 15px; border-radius: 4px;">
					<p><strong>Detected Country:</strong> {geolocationResults.detectedCountry}</p>
					<p><strong>Detected Language:</strong> {geolocationResults.detectedLanguage}</p>
				</div>
			</div>

			<!-- Current State -->
			<div
				style="padding: 20px; background: #fef3c7; border-radius: 8px; border-left: 4px solid #f59e0b;"
			>
				<h3 style="margin: 0 0 15px 0; color: #d97706;">⚙️ Current Language State</h3>
				<div style="background: #ffffff; padding: 15px; border-radius: 4px;">
					<p><strong>Active Language:</strong> {geolocationResults.currentLanguage}</p>
					<p>
						<strong>Translation Test:</strong>
						{t('site_title', 'Dock2Gdansk')} - {t(
							'site_tagline',
							'Professional Cargo Transportation'
						)}
					</p>
				</div>
			</div>

			<!-- User Preferences -->
			<div
				style="padding: 20px; background: #f3e8ff; border-radius: 8px; border-left: 4px solid #8b5cf6;"
			>
				<h3 style="margin: 0 0 15px 0; color: #7c3aed;">👤 User Preferences (localStorage)</h3>
				<pre
					style="background: #ffffff; padding: 15px; border-radius: 4px; overflow-x: auto; font-size: 12px;">{JSON.stringify(
						geolocationResults.userPreferences,
						null,
						2
					)}</pre>
			</div>

			<!-- Debug Actions -->
			<div
				style="padding: 20px; background: #fee2e2; border-radius: 8px; border-left: 4px solid #ef4444;"
			>
				<h3 style="margin: 0 0 15px 0; color: #dc2626;">🔧 Debug Actions</h3>
				<div style="display: flex; gap: 10px; flex-wrap: wrap;">
					<button
						onclick={clearPreferences}
						style="padding: 10px 20px; background: #ef4444; color: white; border: none; border-radius: 4px; cursor: pointer;"
					>
						Clear Preferences
					</button>
					<button
						onclick={testGeolocation}
						style="padding: 10px 20px; background: #0043ce; color: white; border: none; border-radius: 4px; cursor: pointer;"
					>
						Refresh & Test
					</button>
					<a
						href="/"
						style="padding: 10px 20px; background: #22c55e; color: white; text-decoration: none; border-radius: 4px; display: inline-block;"
					>
						Back to Home
					</a>
				</div>
			</div>

			<!-- How It Works -->
			<div
				style="padding: 20px; background: #f8fafc; border-radius: 8px; border: 1px solid #e2e8f0;"
			>
				<h3 style="margin: 0 0 15px 0; color: #64748b;">📋 How Geolocation Detection Works</h3>
				<ol style="margin: 0; padding-left: 20px; line-height: 1.6;">
					<li>
						<strong>Server-side (Vercel):</strong> Uses <code>x-vercel-ip-country</code> header from
						Vercel Edge Network
					</li>
					<li>
						<strong>Client-side fallback:</strong> Uses free IP geolocation APIs (ipapi.co, ip-api.com,
						etc.)
					</li>
					<li>
						<strong>Language mapping:</strong> CN/HK/MO/TW/SG → Chinese (zh), all others → English (en)
					</li>
					<li>
						<strong>User preferences:</strong> Manual language selection overrides geolocation
					</li>
					<li>
						<strong>localStorage keys:</strong>
						<ul style="margin: 5px 0;">
							<li><code>preferred-language</code>: User's saved language choice</li>
							<li>
								<code>language-override</code>: Set to 'true' when user manually selects language
							</li>
							<li><code>language-geolocation</code>: Language detected by geolocation</li>
						</ul>
					</li>
				</ol>
			</div>
		</div>
	{/if}
</div>
