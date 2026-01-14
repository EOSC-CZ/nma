import http from 'k6/http';
import { check, sleep, group } from 'k6';
import { Trend, Rate } from 'k6/metrics';

// Base configuration
const BASE_URL = __ENV.BASE_URL || 'https://127.0.0.1:5000';
const MAX_VUS = __ENV.MAX_VUS || 1000
const MAX_RPS = __ENV.MAX_RPS || MAX_VUS
const DURATION = __ENV.DURATION || '30m'
const SEARCH_URL = `${BASE_URL}/api/datasets`
const SEARCH_UI_URL = `${BASE_URL}/datasets`
const ABORT_ON_UX_FAIL = false;

// Metrics
const searchLatency = new Trend('search_latency');
const recordLatency = new Trend('record_latency');
const idLookupLatency = new Trend('id_lookup_latency');
const pingLatency = new Trend('ping_latency');
const errorRate = new Rate('errors');

// k6 options — progressive ramping to find breakpoint
export const options = {
    scenarios: {
        breakpoint: {
            executor: 'ramping-arrival-rate', //Assure load increase if the system slows
            preAllocatedVUs: 1,
            maxVUs: MAX_VUS,
            stages: [
                { target: MAX_RPS, duration: DURATION },
            ],
        }
    },

    thresholds: {
        // Overall KPIs tied to UX
        errors: [{ threshold: 'rate<0.01', abortOnFail: true, delayAbortEval: '10s' }],
        http_req_failed: [{
            threshold: 'rate<0.02', abortOnFail: true, delayAbortEval: '10s',
        }],      // <2% HTTP errors tolerated
        http_req_duration: [{
            threshold: 'p(75)<5000', abortOnFail: ABORT_ON_UX_FAIL, delayAbortEval: '10s',
        }],   // 95% < 5s for generic http requests
        search_latency: [{
            threshold: 'p(95)<3000', abortOnFail: ABORT_ON_UX_FAIL, delayAbortEval: '10s',
        }],      // 95% < ~3s for search
        record_latency: [{
            threshold: 'p(95)<1500', abortOnFail: ABORT_ON_UX_FAIL, delayAbortEval: '10s',
        }],      // 95% < ~1.5s for detail
        ping_latency: [{
            threshold: 'p(99)<5000', abortOnFail: true, delayAbortEval: '10s',
        }],      // 95% < ~5s for ping - same as liveliness probe timeout

    },
    insecureSkipTLSVerify: BASE_URL === 'https://127.0.0.1:5000',
};

// Default sleep time between requests
const THINK_TIME = 1 + Math.random() * 2;

function isJsonResponse (res) {
    const ct = res.headers['Content-Type'] || res.headers['content-type'];
    return ct && ct.includes('application/json');
}

function safeJson (res) {
    try {
        return res.json();
    } catch (e) {
        console.error(res)
        return null;
    }
}

export default function () {

    const pingRes = http.get(`${BASE_URL}/ping`);
    pingLatency.add(pingRes.timings.duration);
    const ok = check(pingRes, {
        'liveliness HTTP 200': (r) => r.status === 200,
    });
    if (!ok) errorRate.add(1);

    group('Landing page', () => {
        // 1) Homepage load
        const res = http.get(`${BASE_URL}/`);
        const ok = check(res, {
            'landing page HTTP 200': (r) => r.status === 200,
        });
        if (!ok) errorRate.add(1);
    });

    sleep(THINK_TIME);

    group('Browse all records', () => {
        // 2) Search — base empty query (UI typically uses empty q to load all)
        const url = `${SEARCH_URL}?q=&page=1&size=10`;
        const res = http.get(url, { headers: { Accept: 'application/json' } });
        searchLatency.add(res.timings.duration);

        const ok = check(res, {
            'search HTTP 200': (r) => r.status === 200,
            'search contains hits': (r) => {
                if (!isJsonResponse(r)) return false;

                const body = safeJson(r);
                return (
                    body &&
                    body.hits &&
                    Array.isArray(body.hits.hits)
                );
            }
        });
        if (!ok) errorRate.add(1);
    });

    sleep(THINK_TIME);

    group('Search a term', () => {
        // 3) Search — keyword query
        const url = `${SEARCH_URL}?q=open&page=1&size=10`;
        const res = http.get(url, { headers: { Accept: 'application/json' } });
        searchLatency.add(res.timings.duration);

        const ok = check(res, {
            'keyword search HTTP 200': (r) => r.status === 200,
        });
        if (!ok) errorRate.add(1);
    });

    sleep(THINK_TIME);

    group('Faceted search', () => {
        // 4) Facet filtering - filter results by resource type & language
        const url = `${SEARCH_URL}?f=metadata.resource_type:dataset&f=metadata.languages:ces&page=1&size=10`;
        const res = http.get(url, { headers: { Accept: 'application/json' } });
        searchLatency.add(res.timings.duration);

        const ok = check(res, {
            'facet search HTTP 200': (r) => r.status === 200,
        });
        if (!ok) errorRate.add(1);
    });

    sleep(THINK_TIME);

    group('Dataset detail page', () => {
        // 5) Record detail — pick 1 from search results & export as DataCite JSON
        const listRes = http.get(`${SEARCH_URL}?page=1&size=1`, { headers: { Accept: 'application/json' } });
        if (listRes.status === 200) {
            const hits = listRes.json().hits.hits;
            if (hits && hits.length > 0) {
                const record_link = hits[0].links.self_html;
                const detailRes = http.get(record_link, { headers: { Accept: 'text/html' } });
                recordLatency.add(detailRes.timings.duration);

                const ok = check(detailRes, {
                    'record detail HTTP 200': (r) => r.status === 200,
                });
                if (!ok) errorRate.add(1);
            }
        } else {
            errorRate.add(1);
        }
    });

    sleep(THINK_TIME);

    group('Look up by identifier', () => {
        const identifierPool = [
            'https://doi.org/10.5281/zenodo.17162434',
            'https://doi.org/10.5281/zenodo.8033351',
            'https://doi.org/10.5281/zenodo.16753981',
            'https://hdl.handle.net/20.500.14391/3611'
        ]

        const identifier = identifierPool[Math.floor(Math.random() * identifierPool.length)];

        const searchRes = http.get(`${SEARCH_UI_URL}?q=${encodeURIComponent(identifier)}`, { redirects: 0 });

        idLookupLatency.add(searchRes.timings.duration);

        if (searchRes.status === 302 && searchRes.headers["Location"]) {
            const detailUrl = searchRes.headers["Location"];
            const detailRes = http.get(`${BASE_URL}${detailUrl}`, { headers: { Accept: 'text/html' } });

            recordLatency.add(detailRes.timings.duration);

            const ok = check(detailRes, {
                'record detail HTTP 200': (r) => r.status === 200,
                'record detail contains identifier': (r) => r.body.includes(identifier)
            });

            if (!ok) errorRate.add(1);
        } else {
            errorRate.add(1);
        }
    });

    sleep(THINK_TIME);
}
