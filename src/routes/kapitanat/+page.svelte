<script>
	import {
		Button,
		TextInput,
		Tile,
		Grid,
		Column,
		Loading,
		InlineNotification,
		Form
	} from 'carbon-components-svelte';
	// Removed carbon icons to avoid import issues
	import { t } from '$lib/stores/config.js';
	import { goto } from '$app/navigation';
	import { onMount } from 'svelte';

	let email = '';
	let password = '';
	let isLoading = false;
	let loginMessage = '';
	let loginStatus = 'info';
	let isLoggedIn = false;

	// Check if already logged in
	onMount(() => {
		const token = localStorage.getItem('admin-token');
		if (token) {
			// Verify token validity (you'd make an API call here)
			isLoggedIn = true;
			goto('/kapitanat/dashboard');
		}
	});

	async function handleLogin() {
		if (!email || !password) {
			loginMessage = 'Please enter email and password';
			loginStatus = 'error';
			return;
		}

		isLoading = true;
		loginMessage = '';

		try {
			// This would normally call AWS Cognito
			// For now, simulate the login process
			await new Promise((resolve) => setTimeout(resolve, 1000));

			// Mock successful login
			const mockToken = 'mock-jwt-token-' + Date.now();
			localStorage.setItem('admin-token', mockToken);
			localStorage.setItem('admin-email', email);

			loginMessage = 'Login successful! Redirecting...';
			loginStatus = 'success';

			setTimeout(() => {
				goto('/kapitanat/dashboard');
			}, 1000);
		} catch (error) {
			loginMessage = 'Login failed. Please check your credentials.';
			loginStatus = 'error';
		} finally {
			isLoading = false;
		}
	}
</script>

<svelte:head>
	<title>{t('admin.login', 'Admin Login')} - Dock2Gdansk</title>
</svelte:head>

<div class="flex min-h-screen items-center justify-center bg-gray-50 px-4 py-12">
	<div class="w-full max-w-md">
		<div class="mb-8 text-center">
			<div class="mb-4 text-5xl">🔐</div>
			<h1 class="text-3xl font-bold text-gray-900">
				{t('admin.login', 'Admin Login')}
			</h1>
			<p class="mt-2 text-gray-600">Dock2Gdansk Administration Panel</p>
		</div>

		<Tile class="p-8">
			{#if loginMessage}
				<div class="mb-6">
					<InlineNotification kind={loginStatus} title={loginMessage} hideCloseButton />
				</div>
			{/if}

			<Form on:submit={handleLogin}>
				<div class="space-y-6">
					<TextInput
						type="email"
						labelText={t('admin.email', 'Email')}
						placeholder="admin@dock2gdansk.com"
						bind:value={email}
						required
						disabled={isLoading}
					/>

					<TextInput
						type="password"
						labelText={t('admin.password', 'Password')}
						placeholder="Enter your password"
						bind:value={password}
						required
						disabled={isLoading}
					/>

					<Button type="submit" class="mt-4 w-full" disabled={isLoading}>
						{#if isLoading}
							<Loading withOverlay={false} small />
							Logging in...
						{:else}
							{t('admin.login_button', 'Login')}
						{/if}
					</Button>
				</div>
			</Form>

			<div class="mt-6 text-center">
				<p class="text-sm text-gray-600">For demo purposes, use any email and password</p>
			</div>
		</Tile>

		<div class="mt-6 text-center">
			<Button kind="ghost" href="/">← Back to Homepage</Button>
		</div>
	</div>
</div>

<style>
	:global(.bx--form) {
		margin: 0;
	}
</style>
