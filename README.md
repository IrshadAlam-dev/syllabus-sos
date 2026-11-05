# Syllabus SOS

Turn syllabi, assignment PDFs, and course screenshots into a reviewable study plan. Meta Muse Spark extracts likely assignments, deadlines, requirements, and next steps; students can verify and edit the results before adding them to their plan.

## Try it

- [Open the live app](https://syllabus-sos.vercel.app)
- [Watch the demo video](https://youtu.be/cCQiEG6IxEc)

## Features

- Upload PDF, PNG, and JPEG course documents (4 MB maximum).
- Review, edit, approve, or reject extracted assignments before they enter the plan.
- Check supporting text and PDF page references for selectable-text deadlines; image-derived dates are flagged for manual review.
- Organize approved work with a weekly workload view, due-date calendar, study preferences, and Focus Mode.
- Save assignments and preferences in the browser.

## How Meta Muse Spark is used

Muse Spark analyzes uploaded documents and returns structured assignment details. The app validates the response and checks quoted dates against selectable PDF text when possible. Uncertain or image-derived information is shown for the student to verify. The API key stays on the backend.

## Run locally

Requirements: Python 3.11+ and Node.js 20.19+ (or 22.12+).

1. Configure the backend:

```bash
cd backend
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

Add your Meta API key as `MODEL_API_KEY` in `backend/.env`. Then load the environment and start the API:

```bash
set -a
source .env
set +a
uvicorn main:app --reload --port 8000
```

2. In a second terminal, start the frontend:

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5173. The backend health check is http://localhost:8000/api/health. Keep `backend/.env` private; never expose the API key in frontend variables.

## Verify

```bash
cd backend
.venv/bin/python -m unittest -v test_main.py
cd ../frontend
npm run build
```

These tests do not measure general extraction accuracy. Verify dates and requirements against the original documents, especially for scans and screenshots.

## Privacy and limitations

Uploaded documents are sent to Meta Model API for analysis and are not saved by this demo. Plans and preferences are stored in browser local storage; there are no accounts or cross-device sync. Image-derived dates need manual checking. The workload schedule is an estimate, not a guaranteed plan. Public uploads can incur model usage charges.

## More project details

- [Architecture](ARCHITECTURE.md)
- [Submission checklist](SUBMISSION_CHECKLIST.md)
- [MIT License](LICENSE)
