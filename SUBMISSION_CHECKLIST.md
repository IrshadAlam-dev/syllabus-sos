# Submission checklist

Updated: November 3, 2026.

## Product and verification

- [x] Frontend production build: `npm run build` succeeded after the final review/workload/Focus Mode edits.
- [x] Backend unit suite: all 17 tests passed in the final run, including mixed scanned/text-page limits, evidence/date checks, retries, and API error paths.
- [x] Backend Python syntax compilation passed for `main.py` and `test_main.py`.
- [x] Live Muse Spark integration: a synthetic, non-personal PDF received HTTP 200 through the updated local FastAPI service; Muse Spark 1.3 returned a structured assignment, and the deadline excerpt matched page 1.
- [x] Browser workflow: synthetic upload opened review, showed matched quote and page, then approval replaced sample content with the approved assignment.
- [x] Preferences: study capacity and preferred days changed the workload view and survived browser refresh.
- [x] Focus Mode: timer start/pause and mark-complete-to-next-task were exercised in the browser.
- [ ] Accuracy evaluation on owner-selected documents. The synthetic API call is not a general accuracy benchmark.
- [ ] Image/scanned-document accuracy review against original screenshots.
- [ ] Final live API request on the owner’s chosen demo document immediately before recording; the latest live check used a synthetic document.

## Delivery status

- [x] README includes setup, API environment, data flow, limitations, testing, privacy, and deployment steps.
- [x] Architecture diagram and component boundaries documented in `ARCHITECTURE.md`.
- [x] Demo video published on YouTube.
- [x] Technical audit documented in `TECHNICAL_AUDIT.md`.
- [ ] Screenshot assets captured and checked into the project. None are currently included.
- [ ] Demo video recorded. None is currently included.
- [ ] Public deployment configured and verified. No deployment URL exists yet.
- [ ] Submission portal fields and entry confirmed. No submission was made.
- [ ] Owner reviews event terms and completes final submission.

## Secret and deployment checks

- [x] `.gitignore` excludes `.env`, virtual environments, `node_modules`, and generated build assets.
- [x] `backend/.env.example` contains variable names/placeholders, not a real key.
- [ ] Confirm the hosting provider keeps `MODEL_API_KEY` server-side and limits public upload usage.
- [ ] Set exact `CORS_ORIGINS` and `VITE_API_URL` for a deployment, then test from the public frontend origin.

## Status meaning

- **VERIFIED**: exercised in the current local app or test suite as listed above.
- **PARTIALLY VERIFIED**: feature passed a synthetic/local check but not an owner-selected real-document evaluation.
- **NOT VERIFIED**: no test or external confirmation yet.
- **BLOCKED**: requires external deployment, owner review, or portal action.
