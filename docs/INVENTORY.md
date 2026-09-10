# OceanEmbed implementation inventory

## Requirements and authoritative material

Read Final Solution v3, all five team task files, the re-import guide, live status report, root cause trace, corrected inversion cell, both training notebooks, frontend React and map source, Gemini assistant script, source cube and three revised exports. Earlier solution variants and Stitch exports are historical design/intent. Current code and actual execution take priority. Source checkpoint, raw acquisition code and original FastAPI source were not found in the project; the three UI ZIPs contain HTML/screenshots, not backend code. `data_fetch` is empty.

## Verified existing work

- Existing Render health reports database OK. OpenAPI contains health, profile, regional metrics and inversion routes.
- Live metrics contain the revised region labels and correctly map CSV `rmse`/`bias` to API `rmse_c`/`bias_c`.
- Live case rows now contain real data and match the revised CSV. No destructive re-import is necessary.
- Database schema was inspected using a read-only transaction; no live tables were changed.
- React visual tokens (navy, blue, orange, Arial), masthead, tab structure, panels and map are retained.

## Implemented but scientifically provisional

- 676,740 stored profiles, 60 dates (2023-05-02–2023-06-30), 11,279 identical supported locations each date; arrays contain 15 positions and preserve nulls.
- 58 metric rows: two regions × (15 GLORYS + 14 ARGO). ARGO surface is absent.
- Two inversion profiles, each 15 positions but only six populated (0–50 m). All case GLORYS values/nulls match the cube exactly. No source ARGO exists at these locations/depths; exact integer ARGO coordinates rule out the historical truncation explanation for these cases.
- At two sampled 100 m columns, stored climatology agrees with a full-series two-harmonic least-squares fit within 1.1e-7 °C. This supports evaluation leakage; it does not prove every source preprocessing operation.
- Notebook fills target NaNs with zero then scores ordinary MSE. Its sign-count penalty is non-differentiable and applied to anomalies, not a hydrostatic density constraint.
- Decoder uses dense depth mixing, not self-attention. Regime gating is implemented.
- Temperature threshold proxies use 0.5°C and 0.2°C crossings; clipped SLD−MLD is zero in recorded output and is not density-based BLT.
- Uncertainty is a learned scale, not calibrated interval coverage.

## Repairs in this checkout

Data discovery; bounded nearest-grid matching; date and input validation; upstream schema validation; all metrics controls; real case tables/plots; chart gaps; local case RMSE labeled 0–50 m; explicit request failures and retry; server-side Gemini function calling; rate/concurrency/tool/time limits; realistic methodology; CSV downloads; direct hash navigation and responsive layout.

Fabricated sync logs, station telemetry, numeric fallbacks, confidence claims, percentages, inference timing, fake contact links and canned AI responses were removed. Unsupported satellite overlays, live inference and density products are described as unavailable.

## Missing dependencies / material decisions

- Original backend deployment credentials/source are absent; keep the working Render/Aiven infrastructure. New server code is a same-origin Worker API facade, adding discovery, strict profile validation and Gemini. Metrics/cases are versioned local copies of verified exports, preserving sample counts missing from the old database schema.
- Local cube lacks required `ocean_mask`; notebook versions refer to a different prepared cube. No checkpoint, acquisition scripts, training metadata file or fresh untouched test data were found. A 4 GB RTX 2050 exists but available system memory was only about 4 GB during inspection. Exact historical retraining is not reproducible from the supplied artifacts. No successful retraining or new scientific validation is claimed.
- Do not execute the supplied “corrected” inversion cell blindly: it excludes incomplete profiles and suggests unsupported causal explanations. Preserve provided cases and label their actual coverage.
- A recoverable source archive, including original supplied scripts, exists outside the checkout at `/home/pseudo/.codex/oceanembed-checkpoint/original-source.tar.gz` (mode 0600). Source had no Git history on arrival.
- Sites registered successfully, but subsequent environment configuration returned HTTP 401 `token_revoked`. Reconnection is required before deployment can complete.
