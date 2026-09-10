# OceanEmbed

React/Vite interface and a Cloudflare Workers-compatible same-origin API. This prototype serves precomputed May–June 2023 profiles through the existing Render/Aiven service; it does not run live model inference. Regional metrics and case studies are versioned snapshots of the supplied exports.

## Run and restart

Node 20.19+ required.

```sh
npm ci
npm run build
cp .env.example .env.local
# Configure GEMINI_API_KEY securely in .env.local, then:
node --env-file=.env.local scripts/serve.mjs
```

Open http://localhost:4173. Stop with Ctrl-C and repeat the final command to restart. The local server runs the same API module used by the deployed Worker. All records persist in the existing database or tracked export snapshots; process memory is only used for short-term rate limits.

```sh
npm test
npm run lint
```

## Hosting

The existing `.openai/hosting.json` identifies the registered Sites project; do not create another Site. Set server-only `GEMINI_API_KEY` (secret), `GEMINI_MODEL=gemini-3.6-flash`, and optionally `UPSTREAM_API_BASE` using Sites environment settings. Build, commit/push this exact checkout using the registered repository credential, package with the Sites hosting helper, save a version, then deploy. Rebuild after source changes; redeploy after environment changes. Source checkout is `/home/pseudo/SIH2026/front_end/ocean-embed`.

The Worker build lives in `dist/server/index.js`; static client assets are in `dist/client`. Browser routes use hash navigation; direct navigation also serves the application shell. No database mutation is needed. The existing Render API remains at https://oceanembed-api-4m85.onrender.com.

## API

- `GET /health`: facade health and whether Gemini is configured (does not claim external database readiness).
- `GET /api/coverage`: supported dates, grid points, depth positions, counts and matching policy.
- `GET /api/profile?date=YYYY-MM-DD&lat=…&lon=…`: nearest supported point within 25 km, strict upstream validation, matching metadata.
- `GET /api/regime-metrics?regime=…&validation_target=…`: separate regions/targets, including sample counts.
- `GET /api/inversion-case`: all real case rows, including nulls.
- `POST /api/ai`: JSON `{ "message": "…", "context": { "date": "2023-05-02", "lat": 14.375, "lon": 88.125 } }`.

Gemini uses the official REST `generateContent` function-calling API. The initial turn must retrieve data; provider model content (including thought signatures) is preserved between turns. Maximum 4 rounds / 6 tool calls / 90-second nominal deadline, 35-second provider requests, 45-second profile requests. Six questions per minute per IP and three concurrent requests **per Worker isolate**, not a global quota; set provider account quotas for a publicly shared deployment. No browser credential or fake provider fallback.

Reference: https://ai.google.dev/gemini-api/docs/generate-content/function-calling

## Data and limitations

See `docs/INVENTORY.md`, `docs/data-audit.json`, and verification records. Source CSV hashes and source matching checks are recorded. The exported uncertainty is uncalibrated. The supplied notebook has leakage/masking concerns and checkpoint provenance is absent. No scientific retraining was performed. Preserved historical output is clearly labeled provisional.

`server/data` is generated from the supplied CSVs. `scripts/audit-data.py` rechecks exports and cube and regenerates those files using NumPy/xarray/h5netcdf; its default source workspace is `/home/pseudo/SIH2026`. Raw CSV/cube files and credentials are not included in the deployed frontend.
