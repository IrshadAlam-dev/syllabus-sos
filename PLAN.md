# Syllabus SOS implementation plan

1. Verify hackathon page, rules availability, Muse API endpoint/model/schema support, and local access.
2. Build a small FastAPI service for PDF/image upload, safe content extraction, Muse Spark structured extraction, prioritization, and plan regeneration.
3. Build a responsive React/Vite interface for landing, upload, processing, dashboard, focus mode, and editable task completion.
4. Document setup, architecture, demo, known limitations, and submission copy; run requested functional and UI checks.
5. Deploy only if working credentials and a deployment target are available; do not submit the entry.

## Verified requirements and access

- Official event page: https://dev.meta.ai/events/global-hackathon
- Submission deadline shown: Nov 4, 2026, 9:00 PM ET.
- The linked Event Rules and Waiver require participants to build with Meta AI products (including Muse Spark, Glimmer, SAM 3, and other Meta products listed on the event page) but do not mandate a specific model. This app uses Muse Spark 1.3.
- Judging: Impact 30%, Meta AI Tooling 25%, Technical Depth & Execution 20%, Demo (including video) 25%.
- Submit through the Cerebral Valley project portal by Nov 4, 2026, 9:00 PM ET. The rules do not specify exact form fields, demo-video duration, or a separate attribution phrase. The app and README identify Muse Spark use.
- Rules state project ownership remains with the entrant, while organizers receive a perpetual, irrevocable, worldwide, royalty-free, non-exclusive license to use and adapt submissions. Event materials are not confidential; recording/likeness permissions also apply. Do not accept terms or submit on the user's behalf.
- Meta Model API docs confirm base URL `https://api.meta.ai/v1`, `muse-spark-1.3`, bearer key `MODEL_API_KEY`, image understanding, and JSON schema structured output.
- Local `muse` executable exists; CLI reports not logged in. `MODEL_API_KEY` is not configured.

## Project structure

- `backend/`: FastAPI upload and Muse integration.
- `frontend/`: Vite React app.
- `README.md`, `PROGRESS.md`, `TASKS.md`: setup and checkpoint tracking.
