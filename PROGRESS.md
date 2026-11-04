# Progress

## Checkpoint — Nov 3, 2026

### Completed

- Built Syllabus SOS in `Desktop/Meta Ai hackathon/syllabus-sos`, preserving the adjacent `legal-agent-workshop` project and its uncommitted changes.
- Implemented a React/Vite frontend and FastAPI/Pydantic backend for PDF and image uploads, Muse Spark analysis, structured output validation, deadline-aware prioritization, and action plans.
- Added editable assignment details, deadline correction, task completion, Focus Mode, and a selectable week calendar.
- Clearly labeled sample data and documented that uploaded documents are sent to Meta Muse Spark and not saved by this demo.
- Configured the local Meta API key in ignored `backend/.env`; the backend health endpoint reports Muse Spark configured.
- Completed an end-to-end live Muse Spark check with a synthetic biology assignment PDF. It returned one assignment, the explicit deadline `2026-11-12`, and five subtasks.
- Added scanned-PDF support: if no selectable text exists, up to five pages render to images and go to Muse Spark. The final backend suite has 17 passing tests, including multimodal fallback, page caps, deadline evidence checks, and bounded retry behavior.
- Added the Desktop preview origin to backend CORS and verified its browser preflight succeeds.
- Refreshed the interface for clarity: the landing page starts with a direct upload action, the dashboard uses plain-language labels, inactive controls and sample course clutter are removed, and assignment checklists are collapsed until opened. Added a readable dashboard style system with mobile layouts.
- Added local browser persistence for Muse Spark results, deadline edits, and completed steps, plus a clear-plan control. The uploaded document itself is not retained by the demo; the UI and README disclose that extracted plan data stays on this device.
- Verified the frontend production build and all 9 backend unit tests.
- Browser-checked the landing page, dashboard, Focus Mode, week navigation, and selected-day agenda.
- Verified official hackathon rules and documented the Meta technology requirement, judging criteria, deadline, submission portal, and entrant license terms.
- Added an assignment review queue: extracted results are held pending approval; each item can be edited or rejected, and high-confidence dates with matched text evidence can be approved in a batch. First approval replaces the illustrative sample plan.
- Added exact quote/date/page checks for selectable PDF text. Image-derived dates stay marked for manual confirmation. Deadline evidence remains viewable from approved assignment cards.
- Added bounded retries for transient Meta API errors and more specific malformed-response handling.
- Added browser-local preferences (study hours, days, and focus block), a week-level deadline/capacity workload view, and a Focus Mode timer with next-task progression.
- Verified a live synthetic Muse Spark result through the updated API: the extracted December 10, 2026 date had the matching quote on page 1. A separate browser flow uploaded the synthetic PDF, reviewed evidence, approved it, and displayed only the approved assignment.
- Expanded backend coverage to 17 passing tests, including text/date/page evidence, scanned and mixed-page PDFs, API retries, and upload failures. The final frontend production build and Python syntax compilation passed.
- Created `ARCHITECTURE.md`, `TECHNICAL_AUDIT.md`, `DEMO_SCRIPT.md`, and `SUBMISSION_CHECKLIST.md`; updated setup, privacy, limitations, and API docs in `README.md`.

### Current local preview

- Frontend: `http://127.0.0.1:5174/`
- Backend: `http://127.0.0.1:8001/`
- The preview processes use `backend/.env`. Keep both Terminal processes running while demonstrating the app.

### Remaining

- Test with an owner-selected academic document and manually compare all fields, especially requirements and image-derived dates.
- Inspect the refreshed layout at mobile viewport size; capture final screenshots and record the demo video.
- Connect hosting and deploy a protected public demo. Render and Vercel config files are prepared; no CLI or deployment token was detected locally.
- Check the authenticated submission portal fields after participant sign-in; prepare the final entry for owner review.
- Owner reviews and submits the entry; do not accept event terms or submit on the owner's behalf.

### Known limitations

- The deployment files parse correctly, but the Docker image build is unverified because Docker Desktop’s daemon is not running.

- Scanned PDF pages are rendered as images for Muse Spark, up to five document pages. Later scanned pages are omitted; split long documents and manually confirm dates.
- Extracted assignments and edits are stored in this browser only; there is no account or cross-device sync.
- The week planner is a simple estimate-based distribution and can mark but not eliminate overload. It is not a guarantee or an exact calendar booking.
- Duplicate detection uses normalized exact assignment titles, not semantic similarity.
- Public deployment should add a request limit or demo access gate before exposing a billable API key.
- Muse Code is installed but not authenticated. Its login flow is available; an automatic approval review blocked sending the project prompt/source and configured key to Muse Code pending explicit owner approval. The scanned-PDF improvement was implemented locally meanwhile.

### Next priority

Review with owner-selected documents, capture screenshots/video, then configure and verify protected deployment.
