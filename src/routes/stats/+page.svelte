<script>
	import { enhance } from '$app/forms';

	let { data, form } = $props();

	const FIELD_LABELS = {
		company: 'Nazwa firmy',
		email: 'E-mail',
		phone_prefix: 'Prefiks telefonu',
		custom_phone_prefix: 'Własny prefiks telefonu',
		phone: 'Numer telefonu',
		cargo_type: 'Rodzaj ładunku',
		inquiry_content: 'Treść zapytania',
		privacy_consent: 'Zgoda: regulamin i prywatność',
		terms_consent: 'Zgoda: udostępnienie profilu',
		cross_border_consent: 'Zgoda: udostępnienie podmiotom trzecim',
		referral_source: 'Skąd o nas wiesz',
		'(none)': 'Wyjście przed wypełnieniem pola'
	};
	const MIN_SAMPLE = 30;

	const label = (id) => FIELD_LABELS[id] ?? id;
	const pct = (n, d) => (d > 0 ? `${Math.round((n / d) * 100)}%` : '—');
	const secs = (ms) =>
		ms == null || Number.isNaN(Number(ms))
			? '—'
			: `${(Number(ms) / 1000).toFixed(1).replace('.', ',')} s`;
	// Polish plural: 1 formularz / 2–4 formularze / 5+ formularzy (12–14 take the "5+" form)
	const startedForms = (n) => {
		if (n === 1) return 'rozpoczęty formularz';
		const tens = n % 100;
		const ones = n % 10;
		return ones >= 2 && ones <= 4 && (tens < 12 || tens > 14)
			? 'rozpoczęte formularze'
			: 'rozpoczętych formularzy';
	};

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
			? new Date(s.trackingSince).toLocaleDateString('pl-PL', {
					day: 'numeric',
					month: 'long',
					year: 'numeric',
					timeZone: 'Europe/Warsaw'
				})
			: null
	);
</script>

<svelte:head>
	<title>Statystyki formularza · Port Gdańsk Connect</title>
	<meta name="robots" content="noindex, nofollow" />
</svelte:head>

<div class="stats" lang="pl">
	{#if !data.authed}
		<section class="login card">
			<h1>Statystyki formularza</h1>
			<p class="muted">Port Gdańsk Connect · panel prywatny</p>
			<form method="POST" action="?/login" use:enhance>
				<label for="password">Hasło</label>
				<input
					id="password"
					name="password"
					type="password"
					autocomplete="current-password"
					required
				/>
				{#if form?.wrong}<p class="error" role="alert">Nieprawidłowe hasło.</p>{/if}
				<button type="submit">Otwórz panel</button>
			</form>
		</section>
	{:else}
		<header class="top">
			<div>
				<h1>Statystyki formularza zapytań</h1>
				<p class="muted">
					{#if sinceLabel}Dane od {sinceLabel}.{:else}Brak danych: zbieranie zaczyna się od
						pierwszej wizyty po uruchomieniu.{/if}
					Jedna wizyta = jedno wczytanie strony. Treści wpisywane w formularz nie są zapisywane.
				</p>
			</div>
			<div class="controls">
				<nav class="range" aria-label="Okres">
					{#each [7, 30, 90] as d (d)}
						<a
							href="?days={d}"
							class:active={s.days === d}
							aria-current={s.days === d ? 'page' : undefined}>{d} dni</a
						>
					{/each}
				</nav>
				<form method="POST" action="?/logout">
					<button class="link" type="submit">Wyloguj</button>
				</form>
			</div>
		</header>

		{#if !enoughData}
			<div class="notice" role="status">
				<strong>Mała próba.</strong>
				{started}
				{startedForms(started)} w tym okresie. Procenty są orientacyjne, dopóki formularza nie rozpocznie
				co najmniej {MIN_SAMPLE} osób.
			</div>
		{/if}

		<section class="tiles" aria-label="Najważniejsze liczby">
			<div class="tile">
				<span class="tile-label">Wizyty na stronie głównej</span><span class="tile-value"
					>{s.pageLoads}</span
				>
			</div>
			<div class="tile">
				<span class="tile-label">Wyświetlenia formularza</span><span class="tile-value"
					>{viewed}</span
				>
			</div>
			<div class="tile">
				<span class="tile-label">Rozpoczęte formularze</span><span class="tile-value"
					>{started}</span
				>
				<span class="tile-sub">{pct(started, viewed)} wyświetleń</span>
			</div>
			<div class="tile">
				<span class="tile-label">Wysłane</span><span class="tile-value">{submitted}</span>
				<span class="tile-sub">{pct(submitted, started)} rozpoczętych</span>
			</div>
		</section>

		<section class="card">
			<h2>Czy lista ładunków zniechęca do wysłania?</h2>
			<div class="verdict">
				<div class="tile">
					<span class="tile-label">Utrata na liście ładunków</span>
					<span class="tile-value"
						>{cargoLoss == null ? '—' : `${Math.round(cargoLoss * 100)}%`}</span
					>
					<span class="tile-sub">osób, które otworzyły listę i nic nie wybrały</span>
				</div>
				<div class="tile">
					<span class="tile-label">Typowa utrata na innych krokach</span>
					<span class="tile-value"
						>{typicalLoss == null ? '—' : `${Math.round(typicalLoss * 100)}%`}</span
					>
					<span class="tile-sub">średnia z pozostałych kroków lejka</span>
				</div>
				<div class="tile">
					<span class="tile-label">Porzucenia na polu ładunku</span>
					<span class="tile-value">{pct(abandonAtCargo, abandonTotal)}</span>
					<span class="tile-sub">{abandonAtCargo} z {abandonTotal} porzuconych formularzy</span>
				</div>
				<div class="tile">
					<span class="tile-label">Czas wyboru ładunku</span>
					<span class="tile-value">{secs(s.cargoEffort?.p50)}</span>
					<span class="tile-sub"
						>mediana · najwolniejsza ćwiartka powyżej {secs(s.cargoEffort?.p75)}</span
					>
				</div>
			</div>
			<p class="muted small">
				Lista jest problemem, jeśli pierwsza liczba jest wyraźnie wyższa od drugiej, pole ładunku
				najczęściej kończy wizytę, a wybór trwa dużo dłużej niż kilka sekund.
			</p>
		</section>

		<section class="card">
			<h2>Lejek</h2>
			<ol class="bars" aria-label="Lejek formularza">
				{#each s.funnel as step, i (step.key)}
					{@const loss = i > 0 ? stepLoss[i - 1] : null}
					<li
						title="{step.label}: {step.n} ({pct(
							step.n,
							viewed
						)} wyświetleń formularza){loss?.loss != null
							? ` · ${Math.round(loss.loss * 100)}% utraconych na tym kroku`
							: ''}"
					>
						<span class="bar-label">
							{step.label}
							{#if step.key === 'cargo_focused' || step.key === 'cargo_selected'}<span class="tag"
									>ładunek</span
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
			<p class="muted small">Prawa kolumna: odsetek utracony względem poprzedniego kroku.</p>
		</section>

		<div class="grid2">
			<section class="card">
				<h2>Wypełnianie pól po kolei</h2>
				{#if s.fields.length === 0}
					<p class="muted">Brak danych.</p>
				{:else}
					<ol class="bars compact" aria-label="Wypełnione pola w kolejności formularza">
						{#each s.fields as f (f.field)}
							<li title="{label(f.field)}: {f.n} z {started} rozpoczętych ({pct(f.n, started)})">
								<span class="bar-label"
									>{label(f.field)}{#if f.field === 'cargo_type'}<span class="tag">ładunek</span
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
						Odsetek rozpoczętych formularzy, w których wypełniono dane pole, w kolejności
						formularza.
					</p>
				{/if}
			</section>

			<section class="card">
				<h2>Ostatnie pole przed wyjściem</h2>
				{#if s.abandons.length === 0}
					<p class="muted">Brak porzuconych formularzy w tym okresie.</p>
				{:else}
					<table>
						<thead
							><tr><th>Pole</th><th class="num">Wizyty</th><th class="num">Udział</th></tr></thead
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
				<h2>Najczęściej wybierane ładunki</h2>
				{#if s.cargoTop.length === 0}
					<p class="muted">Brak danych.</p>
				{:else}
					<table>
						<thead
							><tr
								><th>Ładunek</th><th class="num">Pozycja na liście</th><th class="num">Wybrany</th
								><th class="num">Wysłany</th></tr
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
						{s.cargoEffort?.others ?? 0} z {s.cargoEffort?.picks ?? 0} pierwszych wyborów to rodzaje
						trafiające do bazy jako „Others”.
					</p>
				{/if}
			</section>

			<section class="card">
				<h2>Według języka</h2>
				{#if s.languages.length === 0}
					<p class="muted">Brak danych.</p>
				{:else}
					<table>
						<thead
							><tr
								><th>Język</th><th class="num">Rozpoczęte</th><th class="num">Wysłane</th><th
									class="num">Konwersja</th
								></tr
							></thead
						>
						<tbody>
							{#each s.languages as l (l.lang)}
								<tr>
									<td>{l.lang === 'zh' ? 'chiński' : l.lang === 'en' ? 'angielski' : l.lang}</td>
									<td class="num">{l.started}</td>
									<td class="num">{l.submitted}</td>
									<td class="num">{pct(l.submitted, l.started)}</td>
								</tr>
							{/each}
						</tbody>
					</table>
				{/if}

				<h2 class="mt">Według dni</h2>
				{#if s.daily.length === 0}
					<p class="muted">Brak danych.</p>
				{:else}
					<table>
						<thead
							><tr><th>Dzień</th><th class="num">Rozpoczęte</th><th class="num">Wysłane</th></tr
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
