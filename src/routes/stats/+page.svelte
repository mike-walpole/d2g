<script>
	import { enhance } from '$app/forms';

	let { data, form } = $props();

	const FIELD_LABELS = {
		company: 'Company name',
		email: 'Email',
		phone_prefix: 'Phone prefix',
		custom_phone_prefix: 'Custom phone prefix',
		phone: 'Phone number',
		cargo_type: 'Cargo type',
		inquiry_content: 'Inquiry details',
		privacy_consent: 'Terms & privacy consent',
		terms_consent: 'Profile-sharing consent',
		cross_border_consent: 'Third-party sharing consent',
		referral_source: 'Where did you hear about us',
		'(none)': 'Left before touching a field'
	};
	const MIN_SAMPLE = 30;

	const label = (id) => FIELD_LABELS[id] ?? id;
	const pct = (n, d) => (d > 0 ? `${Math.round((n / d) * 100)}%` : '—');
	const secs = (ms) =>
		ms == null || Number.isNaN(Number(ms)) ? '—' : `${(Number(ms) / 1000).toFixed(1)} s`;

	let s = $derived(data.stats);
	let started = $derived(s ? (s.funnel.find((x) => x.key === 'started')?.n ?? 0) : 0);
	let submitted = $derived(s ? (s.funnel.find((x) => x.key === 'submitted')?.n ?? 0) : 0);
	let viewed = $derived(s ? (s.funnel[0]?.n ?? 0) : 0);
	let funnelMax = $derived(s ? Math.max(1, ...s.funnel.map((x) => x.n)) : 1);

	// Loss at each step relative to the previous one; the cargo step is compared to the rest.
	let stepLoss = $derived.by(() => {
		if (!s) return [];
		return s.funnel.slice(1).map((step, i) => {
			const prev = s.funnel[i].n;
			return { key: step.key, label: step.label, loss: prev > 0 ? 1 - step.n / prev : null, prev };
		});
	});
	let cargoLoss = $derived(stepLoss.find((x) => x.key === 'cargo_selected')?.loss ?? null);
	let otherLosses = $derived(
		stepLoss.filter((x) => x.key !== 'cargo_selected' && x.loss != null).map((x) => x.loss)
	);
	let typicalLoss = $derived(
		otherLosses.length ? otherLosses.reduce((a, b) => a + b, 0) / otherLosses.length : null
	);
	let abandonTotal = $derived(s ? s.abandons.reduce((a, b) => a + b.n, 0) : 0);
	let abandonAtCargo = $derived(
		s ? (s.abandons.find((a) => a.lastField === 'cargo_type')?.n ?? 0) : 0
	);
	let enoughData = $derived(started >= MIN_SAMPLE);
	let sinceLabel = $derived(
		s?.trackingSince
			? new Date(s.trackingSince).toLocaleDateString('en-GB', {
					day: 'numeric',
					month: 'short',
					year: 'numeric',
					timeZone: 'Europe/Warsaw'
				})
			: null
	);
</script>

<svelte:head>
	<title>Form Analytics · Port Gdańsk Connect</title>
	<meta name="robots" content="noindex, nofollow" />
</svelte:head>

<div class="stats">
	{#if !data.authed}
		<section class="login card">
			<h1>Form analytics</h1>
			<p class="muted">Port Gdańsk Connect · private dashboard</p>
			<form method="POST" action="?/login" use:enhance>
				<label for="password">Password</label>
				<input
					id="password"
					name="password"
					type="password"
					autocomplete="current-password"
					required
				/>
				{#if form?.wrong}<p class="error" role="alert">Wrong password.</p>{/if}
				<button type="submit">Open dashboard</button>
			</form>
		</section>
	{:else}
		<header class="top">
			<div>
				<h1>Inquiry form analytics</h1>
				<p class="muted">
					{#if sinceLabel}Tracking since {sinceLabel}.{:else}No data yet: tracking starts with the
						first visit after launch.{/if}
					One visit = one page load. Nothing a visitor types is recorded.
				</p>
			</div>
			<div class="controls">
				<nav class="range" aria-label="Period">
					{#each [7, 30, 90] as d (d)}
						<a
							href="?days={d}"
							class:active={s.days === d}
							aria-current={s.days === d ? 'page' : undefined}>{d} days</a
						>
					{/each}
				</nav>
				<form method="POST" action="?/logout">
					<button class="link" type="submit">Log out</button>
				</form>
			</div>
		</header>

		{#if !enoughData}
			<div class="notice" role="status">
				<strong>Small sample.</strong>
				{started} started form{started === 1 ? '' : 's'} in this period. Treat the percentages as indicative
				until at least {MIN_SAMPLE} visitors have started the form.
			</div>
		{/if}

		<section class="tiles" aria-label="Key numbers">
			<div class="tile">
				<span class="tile-label">Homepage visits</span><span class="tile-value">{s.pageLoads}</span>
			</div>
			<div class="tile">
				<span class="tile-label">Saw the form</span><span class="tile-value">{viewed}</span>
			</div>
			<div class="tile">
				<span class="tile-label">Started the form</span><span class="tile-value">{started}</span>
				<span class="tile-sub">{pct(started, viewed)} of those who saw it</span>
			</div>
			<div class="tile">
				<span class="tile-label">Submitted</span><span class="tile-value">{submitted}</span>
				<span class="tile-sub">{pct(submitted, started)} of those who started</span>
			</div>
		</section>

		<section class="card">
			<h2>Does the cargo list cause drop-off?</h2>
			<div class="verdict">
				<div class="tile">
					<span class="tile-label">Lost at the cargo list</span>
					<span class="tile-value"
						>{cargoLoss == null ? '—' : `${Math.round(cargoLoss * 100)}%`}</span
					>
					<span class="tile-sub">of visitors who opened it never picked a type</span>
				</div>
				<div class="tile">
					<span class="tile-label">Typical loss at other steps</span>
					<span class="tile-value"
						>{typicalLoss == null ? '—' : `${Math.round(typicalLoss * 100)}%`}</span
					>
					<span class="tile-sub">average of the other funnel steps</span>
				</div>
				<div class="tile">
					<span class="tile-label">Gave up on the cargo field</span>
					<span class="tile-value">{pct(abandonAtCargo, abandonTotal)}</span>
					<span class="tile-sub">{abandonAtCargo} of {abandonTotal} abandoned forms</span>
				</div>
				<div class="tile">
					<span class="tile-label">Time to pick a cargo type</span>
					<span class="tile-value">{secs(s.cargoEffort?.p50)}</span>
					<span class="tile-sub">median · slowest quarter over {secs(s.cargoEffort?.p75)}</span>
				</div>
			</div>
			<p class="muted small">
				The list is a problem if the first number is clearly higher than the second, cargo is the
				most common field people leave on, and picking takes much longer than a few seconds.
			</p>
		</section>

		<section class="card">
			<h2>Funnel</h2>
			<ol class="bars" aria-label="Form funnel">
				{#each s.funnel as step, i (step.key)}
					{@const loss = i > 0 ? stepLoss[i - 1] : null}
					<li
						title="{step.label}: {step.n} ({pct(
							step.n,
							viewed
						)} of those who saw the form){loss?.loss != null
							? ` · ${Math.round(loss.loss * 100)}% lost at this step`
							: ''}"
					>
						<span class="bar-label">
							{step.label}
							{#if step.key === 'cargo_focused' || step.key === 'cargo_selected'}<span class="tag"
									>cargo</span
								>{/if}
						</span>
						<span class="bar-track">
							<span
								class="bar"
								class:bar-cargo={step.key === 'cargo_selected'}
								style="width: {(step.n / funnelMax) * 100}%"
							></span>
						</span>
						<span class="bar-value">{step.n}</span>
						<span class="bar-sub">
							{#if loss?.loss != null}−{Math.round(loss.loss * 100)}%{:else if i > 0}—{/if}
						</span>
					</li>
				{/each}
			</ol>
			<p class="muted small">Right-hand column: share lost compared with the step above.</p>
		</section>

		<div class="grid2">
			<section class="card">
				<h2>Field-by-field completion</h2>
				{#if s.fields.length === 0}
					<p class="muted">No data yet.</p>
				{:else}
					<ol class="bars compact" aria-label="Fields completed, in form order">
						{#each s.fields as f (f.field)}
							<li title="{label(f.field)}: {f.n} of {started} who started ({pct(f.n, started)})">
								<span class="bar-label"
									>{label(f.field)}{#if f.field === 'cargo_type'}<span class="tag">cargo</span
										>{/if}</span
								>
								<span class="bar-track"
									><span
										class="bar"
										style="width: {started ? Math.min(100, (f.n / started) * 100) : 0}%"
									></span></span
								>
								<span class="bar-value">{pct(f.n, started)}</span>
							</li>
						{/each}
					</ol>
					<p class="muted small">
						Share of visitors who started the form and completed each field, in form order.
					</p>
				{/if}
			</section>

			<section class="card">
				<h2>Last field before leaving</h2>
				{#if s.abandons.length === 0}
					<p class="muted">No abandoned forms in this period.</p>
				{:else}
					<table>
						<thead
							><tr><th>Field</th><th class="num">Visitors</th><th class="num">Share</th></tr></thead
						>
						<tbody>
							{#each s.abandons as a (a.lastField)}
								<tr class:hl={a.lastField === 'cargo_type'}>
									<td>{label(a.lastField)}</td>
									<td class="num">{a.n}</td>
									<td class="num">{pct(a.n, abandonTotal)}</td>
								</tr>
							{/each}
						</tbody>
					</table>
				{/if}
			</section>
		</div>

		<div class="grid2">
			<section class="card">
				<h2>Most chosen cargo types</h2>
				{#if s.cargoTop.length === 0}
					<p class="muted">No data yet.</p>
				{:else}
					<table>
						<thead
							><tr
								><th>Cargo</th><th class="num">Position in list</th><th class="num">Picked</th><th
									class="num">Submitted</th
								></tr
							></thead
						>
						<tbody>
							{#each s.cargoTop as c (c.cargo)}
								<tr>
									<td>{c.cargo}</td>
									<td class="num">{c.position ?? '—'}</td>
									<td class="num">{c.selected}</td>
									<td class="num">{c.submitted}</td>
								</tr>
							{/each}
						</tbody>
					</table>
					<p class="muted small">
						{s.cargoEffort?.others ?? 0} of {s.cargoEffort?.picks ?? 0} first picks were types that go
						to the database as “Others”.
					</p>
				{/if}
			</section>

			<section class="card">
				<h2>By language</h2>
				{#if s.languages.length === 0}
					<p class="muted">No data yet.</p>
				{:else}
					<table>
						<thead
							><tr
								><th>Language</th><th class="num">Started</th><th class="num">Submitted</th><th
									class="num">Rate</th
								></tr
							></thead
						>
						<tbody>
							{#each s.languages as l (l.lang)}
								<tr>
									<td>{l.lang === 'zh' ? 'Chinese' : l.lang === 'en' ? 'English' : l.lang}</td>
									<td class="num">{l.started}</td>
									<td class="num">{l.submitted}</td>
									<td class="num">{pct(l.submitted, l.started)}</td>
								</tr>
							{/each}
						</tbody>
					</table>
				{/if}

				<h2 class="mt">By day</h2>
				{#if s.daily.length === 0}
					<p class="muted">No data yet.</p>
				{:else}
					<table>
						<thead
							><tr><th>Day</th><th class="num">Started</th><th class="num">Submitted</th></tr
							></thead
						>
						<tbody>
							{#each [...s.daily].reverse() as d (d.day)}
								<tr
									><td>{d.day}</td><td class="num">{d.started}</td><td class="num">{d.submitted}</td
									></tr
								>
							{/each}
						</tbody>
					</table>
				{/if}
			</section>
		</div>
	{/if}
</div>

<style>
	.stats {
		--ink: #161616;
		--muted: #525252;
		--line: #e0e0e0;
		--surface: #ffffff;
		--page: #f4f4f4;
		--bar: #4589ff;
		--bar-strong: #0043ce;
		--track: #edf2fc;
		--warn-bg: #fcf4d6;
		--warn-line: #f1c21b;
		color: var(--ink);
		background: var(--page);
		max-width: 1100px;
		min-height: calc(100vh - 48px);
		margin: 48px auto 0;
		padding: 32px 16px 64px;
		box-sizing: border-box;
	}
	:global(body:has(.stats)) {
		background: #f4f4f4;
	}
	h1 {
		font-size: 28px;
		font-weight: 600;
		margin: 0 0 6px;
	}
	h2 {
		font-size: 18px;
		font-weight: 600;
		margin: 0 0 16px;
	}
	h2.mt {
		margin-top: 28px;
	}
	.muted {
		color: var(--muted);
		margin: 0;
	}
	.small {
		font-size: 13px;
		margin-top: 12px;
	}
	.card {
		background: var(--surface);
		border: 1px solid var(--line);
		border-radius: 8px;
		padding: 24px;
		margin-bottom: 16px;
		min-width: 0;
	}
	.login {
		max-width: 380px;
		margin: 40px auto;
	}
	.login form {
		display: flex;
		flex-direction: column;
		gap: 8px;
		margin-top: 20px;
	}
	.login input {
		border: 1px solid #8d8d8d;
		border-radius: 4px;
		padding: 10px 12px;
		font-size: 16px;
	}
	button {
		background: var(--bar-strong);
		color: #fff;
		border: 0;
		border-radius: 4px;
		padding: 11px 16px;
		font-size: 15px;
		cursor: pointer;
	}
	button.link {
		background: none;
		color: var(--bar-strong);
		padding: 6px 0;
		text-decoration: underline;
	}
	.error {
		color: #da1e28;
		margin: 0;
	}
	.top {
		display: flex;
		justify-content: space-between;
		align-items: flex-start;
		gap: 16px;
		flex-wrap: wrap;
		margin-bottom: 20px;
	}
	.controls {
		display: flex;
		align-items: center;
		gap: 16px;
	}
	.range {
		display: flex;
		border: 1px solid var(--line);
		border-radius: 6px;
		overflow: hidden;
		background: var(--surface);
	}
	.range a {
		padding: 8px 12px;
		color: var(--ink);
		text-decoration: none;
		font-size: 14px;
	}
	.range a.active {
		background: var(--bar-strong);
		color: #fff;
	}
	.notice {
		background: var(--warn-bg);
		border-left: 4px solid var(--warn-line);
		padding: 12px 16px;
		margin-bottom: 16px;
		border-radius: 4px;
	}
	.tiles,
	.verdict {
		display: grid;
		grid-template-columns: repeat(4, minmax(0, 1fr));
		gap: 12px;
		margin-bottom: 16px;
	}
	.verdict {
		margin-bottom: 0;
	}
	.tile {
		background: var(--surface);
		border: 1px solid var(--line);
		border-radius: 8px;
		padding: 16px;
		display: flex;
		flex-direction: column;
		gap: 4px;
	}
	.verdict .tile {
		background: var(--page);
		border: 0;
	}
	.tile-label {
		font-size: 13px;
		color: var(--muted);
	}
	.tile-value {
		font-size: 30px;
		font-weight: 600;
		font-variant-numeric: tabular-nums;
	}
	.tile-sub {
		font-size: 12px;
		color: var(--muted);
	}
	.bars {
		list-style: none;
		margin: 0;
		padding: 0;
		display: flex;
		flex-direction: column;
		gap: 10px;
	}
	.bars li {
		display: grid;
		grid-template-columns: minmax(150px, 220px) 1fr 48px 52px;
		align-items: center;
		gap: 12px;
	}
	.bars.compact li {
		grid-template-columns: minmax(140px, 200px) 1fr 48px;
	}
	.bar-label {
		font-size: 14px;
	}
	.bar-track {
		height: 14px;
		background: var(--track);
		border-radius: 0 4px 4px 0;
	}
	.bar {
		display: block;
		height: 100%;
		background: var(--bar);
		border-radius: 0 4px 4px 0;
		min-width: 2px;
	}
	.bar-cargo {
		background: var(--bar-strong);
	}
	.bars li:hover .bar {
		filter: brightness(0.9);
	}
	.bar-value {
		text-align: right;
		font-variant-numeric: tabular-nums;
		font-weight: 600;
	}
	.bar-sub {
		text-align: right;
		font-size: 13px;
		color: var(--muted);
		font-variant-numeric: tabular-nums;
	}
	.tag {
		display: inline-block;
		margin-left: 6px;
		font-size: 11px;
		padding: 1px 6px;
		border-radius: 10px;
		border: 1px solid var(--bar-strong);
		color: var(--bar-strong);
		vertical-align: 1px;
	}
	.grid2 {
		display: grid;
		grid-template-columns: repeat(2, minmax(0, 1fr));
		gap: 16px;
	}
	table {
		width: 100%;
		border-collapse: collapse;
		font-size: 14px;
	}
	th,
	td {
		text-align: left;
		padding: 8px 6px;
		border-bottom: 1px solid var(--line);
	}
	th {
		color: var(--muted);
		font-weight: 500;
	}
	.num {
		text-align: right;
		font-variant-numeric: tabular-nums;
	}
	tr.hl td {
		font-weight: 600;
		background: var(--track);
	}
	@media (max-width: 760px) {
		.tiles,
		.verdict,
		.grid2 {
			grid-template-columns: repeat(2, minmax(0, 1fr));
		}
		.grid2 {
			grid-template-columns: 1fr;
		}
		.bars li {
			grid-template-columns: 1fr 44px 48px;
		}
		.bars li .bar-track {
			grid-column: 1 / -1;
			grid-row: 2;
		}
		.bars.compact li {
			grid-template-columns: 1fr 44px;
		}
		.tile-value {
			font-size: 24px;
		}
	}
</style>
