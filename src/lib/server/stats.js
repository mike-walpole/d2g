import { createHmac, timingSafeEqual } from 'node:crypto';
import { env } from '$env/dynamic/private';

export const SESSION_COOKIE = 'pgc_stats';
export const ALLOWED_DAYS = [7, 30, 90];

function requireEnv(name) {
	const v = env[name];
	if (!v) throw new Error(`[stats] Missing server env var ${name}`);
	return v;
}

/** Session token = HMAC of a fixed label keyed by the password: changing STATS_PASSWORD logs everyone out. */
export function sessionToken() {
	return createHmac('sha256', requireEnv('STATS_PASSWORD'))
		.update('pgc-stats-session-v1')
		.digest('hex');
}

function safeEqual(a, b) {
	const ab = Buffer.from(a);
	const bb = Buffer.from(b);
	return ab.length === bb.length && timingSafeEqual(ab, bb);
}

export function passwordMatches(candidate) {
	return safeEqual(String(candidate ?? ''), requireEnv('STATS_PASSWORD'));
}

export function isAuthed(cookies) {
	const c = cookies.get(SESSION_COOKIE);
	return Boolean(c) && safeEqual(c, sessionToken());
}

// Exclude local/dev traffic so test runs never show up in the client's numbers.
const PROD_ONLY = `properties.$host NOT IN ('localhost', '127.0.0.1') AND properties.$host NOT LIKE 'localhost:%' AND properties.$host NOT LIKE '127.0.0.1:%' AND properties.$host NOT LIKE '%.vercel.app'`;

// PostHog allows 3 concurrent API queries per project; queue the rest.
const MAX_CONCURRENT = 3;
let running = 0;
const waiting = [];
async function withSlot(fn) {
	if (running >= MAX_CONCURRENT) await new Promise((r) => waiting.push(r));
	running += 1;
	try {
		return await fn();
	} finally {
		running -= 1;
		waiting.shift()?.();
	}
}

function hogql(fetchFn, query) {
	return withSlot(() => runHogql(fetchFn, query));
}

async function runHogql(fetchFn, query) {
	const projectId = requireEnv('POSTHOG_PROJECT_ID');
	const key = requireEnv('POSTHOG_PERSONAL_API_KEY');
	const res = await fetchFn(`https://eu.posthog.com/api/projects/${projectId}/query/`, {
		method: 'POST',
		headers: { Authorization: `Bearer ${key}`, 'Content-Type': 'application/json' },
		body: JSON.stringify({ query: { kind: 'HogQLQuery', query }, name: 'pgc-client-stats' })
	});
	const text = await res.text();
	if (!res.ok) {
		throw new Error(
			`[stats] PostHog query failed ${res.status}: ${text.slice(0, 500)}\nQuery: ${query}`
		);
	}
	const json = JSON.parse(text);
	return json.results ?? [];
}

const FUNNEL_STEPS = [
	{ key: 'viewed', label: 'Wyświetlenie formularza' },
	{ key: 'started', label: 'Rozpoczęcie wypełniania' },
	{ key: 'cargo_focused', label: 'Otwarcie listy ładunków' },
	{ key: 'cargo_selected', label: 'Wybór ładunku' },
	{ key: 'submit_clicked', label: 'Kliknięcie „Wyślij”' },
	{ key: 'submitted', label: 'Wysłanie zakończone' }
];

/** @param {typeof fetch} fetchFn @param {number} days */
export async function loadStats(fetchFn, days) {
	if (!ALLOWED_DAYS.includes(days)) throw new Error(`[stats] days must be one of ${ALLOWED_DAYS}`);
	const range = `timestamp >= now() - INTERVAL ${days} DAY AND ${PROD_ONLY}`;

	const [
		funnelRows,
		pageRows,
		fieldRows,
		abandonRows,
		cargoEffortRows,
		cargoTopRows,
		langRows,
		dailyRows,
		firstRows
	] = await Promise.all([
		// One distinct_id = one page load (memory persistence). Each step requires all earlier steps.
		hogql(
			fetchFn,
			`SELECT
					countIf(v) AS viewed,
					countIf(v AND s) AS started,
					countIf(v AND s AND cf) AS cargo_focused,
					countIf(v AND s AND cf AND cs) AS cargo_selected,
					countIf(v AND s AND cf AND cs AND sc) AS submit_clicked,
					countIf(v AND s AND cf AND cs AND sc AND ok) AS submitted
				FROM (
					SELECT distinct_id,
						max(event = 'form_viewed') AS v,
						max(event = 'form_started') AS s,
						max(event = 'cargo_focused') AS cf,
						max(event = 'cargo_selected') AS cs,
						max(event = 'submit_clicked') AS sc,
						max(event = 'form_submitted') AS ok
					FROM events
					WHERE ${range} AND event IN ('form_viewed','form_started','cargo_focused','cargo_selected','submit_clicked','form_submitted')
					GROUP BY distinct_id
				)`
		),
		hogql(
			fetchFn,
			`SELECT count() FROM events WHERE ${range} AND event = '$pageview' AND properties.$pathname = '/'`
		),
		// Per-field completion among page loads that started the form
		hogql(
			fetchFn,
			`SELECT properties.field AS field, min(toInt(properties.field_index)) AS idx, count(DISTINCT distinct_id) AS n
				FROM events WHERE ${range} AND event = 'field_completed'
				GROUP BY field ORDER BY idx`
		),
		hogql(
			fetchFn,
			`SELECT coalesce(properties.last_field, '(none)') AS last_field, count() AS n,
					countIf(properties.reached_cargo = 'true' OR properties.reached_cargo = true) AS reached_cargo
				FROM events WHERE ${range} AND event = 'form_abandoned'
				GROUP BY last_field ORDER BY n DESC`
		),
		// Time from first opening the cargo list to the first pick
		hogql(
			fetchFn,
			`SELECT
					count() AS picks,
					quantile(0.5)(toFloat(properties.ms_to_select)) AS p50,
					quantile(0.75)(toFloat(properties.ms_to_select)) AS p75,
					quantile(0.9)(toFloat(properties.ms_to_select)) AS p90,
					countIf(properties.cargo_maps_to_others = 'true' OR properties.cargo_maps_to_others = true) AS others
				FROM events WHERE ${range} AND event = 'cargo_selected' AND toInt(properties.change_count) = 1`
		),
		hogql(
			fetchFn,
			`SELECT properties.cargo_name AS cargo,
					count(DISTINCT distinct_id) AS selected,
					count(DISTINCT if(event = 'form_submitted', distinct_id, NULL)) AS submitted,
					max(toInt(properties.cargo_list_position)) AS position
				FROM events WHERE ${range} AND event IN ('cargo_selected','form_submitted') AND properties.cargo_name IS NOT NULL
				GROUP BY cargo ORDER BY selected DESC LIMIT 15`
		),
		hogql(
			fetchFn,
			`SELECT lang, countIf(s) AS started, countIf(s AND ok) AS submitted FROM (
					SELECT distinct_id, any(properties.site_language) AS lang,
						max(event = 'form_started') AS s, max(event = 'form_submitted') AS ok
					FROM events WHERE ${range} AND event IN ('form_started','form_submitted')
					GROUP BY distinct_id
				) GROUP BY lang ORDER BY started DESC`
		),
		hogql(
			fetchFn,
			`SELECT toDate(timestamp) AS day,
					count(DISTINCT if(event = 'form_started', distinct_id, NULL)) AS started,
					count(DISTINCT if(event = 'form_submitted', distinct_id, NULL)) AS submitted
				FROM events WHERE ${range} AND event IN ('form_started','form_submitted')
				GROUP BY day ORDER BY day`
		),
		// min() over zero rows returns the 1970 epoch in ClickHouse, not NULL
		hogql(
			fetchFn,
			`SELECT if(count() = 0, NULL, min(timestamp)) FROM events WHERE ${PROD_ONLY} AND event = 'form_viewed'`
		)
	]);

	const f = funnelRows[0] ?? [];
	const funnel = FUNNEL_STEPS.map((step, i) => ({ ...step, n: Number(f[i] ?? 0) }));

	return {
		days,
		pageLoads: Number(pageRows[0]?.[0] ?? 0),
		funnel,
		fields: fieldRows.map(([field, idx, n]) => ({ field, idx: Number(idx), n: Number(n) })),
		abandons: abandonRows.map(([lastField, n, reachedCargo]) => ({
			lastField,
			n: Number(n),
			reachedCargo: Number(reachedCargo)
		})),
		cargoEffort: cargoEffortRows[0]
			? {
					picks: Number(cargoEffortRows[0][0]),
					p50: cargoEffortRows[0][1],
					p75: cargoEffortRows[0][2],
					p90: cargoEffortRows[0][3],
					others: Number(cargoEffortRows[0][4])
				}
			: null,
		cargoTop: cargoTopRows.map(([cargo, selected, submitted, position]) => ({
			cargo,
			selected: Number(selected),
			submitted: Number(submitted),
			position: position == null ? null : Number(position)
		})),
		languages: langRows.map(([lang, started, submitted]) => ({
			lang: lang || 'unknown',
			started: Number(started),
			submitted: Number(submitted)
		})),
		daily: dailyRows.map(([day, started, submitted]) => ({
			day: String(day),
			started: Number(started),
			submitted: Number(submitted)
		})),
		trackingSince: firstRows[0]?.[0] ?? null
	};
}
