# Technical audit — Syllabus SOS

Audit target: the Desktop project at `Desktop/Meta Ai hackathon/syllabus-sos`.

## Stack and repository state

- Frontend: React + Vite, single-page app in `frontend/src/main.jsx`, CSS in `frontend/src/style.css` plus review/workload styles.
- Backend: FastAPI in `backend/main.py`; Pydantic response validation; HTTPX Meta API client; PyMuPDF PDF processing.
- Local dependencies already installed (`frontend/node_modules`, `backend/.venv`). Backend secret file is ignored by `.gitignore`; its contents were not inspected or printed.
- No `.git` directory exists in this project copy, so source history and diffs cannot be audited here.
- Existing persistence is browser local storage, not a database.

## Working and verified

- PDF/image intake, content-signature checks, 10 MB upload limit, selectable PDF extraction, scanned-PDF rendering, strict structured model response, and deadline ordering.
- Real Muse Spark 1.3 request through the Meta Model API Responses endpoint using a synthetic non-personal assignment PDF. It returned one assignment, three subtasks, and a December 10, 2026 due date whose exact quote matched page 1.
- Browser upload → review → approve → replace sample plan, inspected in the local preview. The approved result appeared on the assignment list with the evidence disclosure and entered the daily plan.
- Study capacity and preferred days changed the weekly workload view and survived a page refresh in the browser.
- Focus Mode displayed current-task details; start/pause timer and mark-complete advanced to the next task.
- All 17 backend unit tests and the production frontend build pass (see submission checklist for exact results).

## Incomplete or constrained

- No owner-selected syllabus/assignment evaluation set or measured accuracy score exists. The synthetic smoke test proves connectivity and response parsing only.
- Screenshot/scanned-image deadlines need manual verification. Text evidence validation cannot establish semantic correctness beyond matching the quoted date and page.
- PDF pages without selectable text are rendered only through the first five document pages. Later scanned pages are listed as omitted.
- Duplicate prevention is normalized exact-title matching, not semantic matching.
- Workload is a simple greedy distribution across preferred days, bounded by deadlines and daily capacity. It can still surface overloaded days and does not optimize course importance, calendar events, or variable availability.
- Focus timer is a browser timer without background persistence or notifications.
- No public deployment, request authentication, rate limiting, database, or account system is configured.
- No checked-in screenshot assets or demo video are present.

## Critical risks before public demo

1. The open upload endpoint can incur API usage if exposed publicly. Add a request limit or demo access gate before deployment.
2. A user’s course documents are sent to Meta for analysis. Keep that disclosure visible and test with documents the owner is willing to transmit.
3. The configured key’s presence is not proof of access; the synthetic live request proves it worked at test time, but verify again before recording.
4. Students should confirm image-derived dates, unclear dates, and high-impact requirements against the original source.

## Recommended order

1. Run the final unit suite/build and live health check.
2. Review at least one owner-selected assignment and one screenshot manually, recording any mistakes.
3. Capture clean screenshots and record the demo with the real review flow; label any illustrative sample data.
4. Configure protected backend hosting and frontend URL/CORS, then verify a public upload before claiming deployment.
5. Complete the submission portal and owner review; never claim a deployment, demo, or portal submission that was not verified.
