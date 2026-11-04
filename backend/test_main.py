import asyncio
import json
import os
import unittest
from unittest.mock import AsyncMock, patch

import fitz
from fastapi import HTTPException
from fastapi.testclient import TestClient

import main


def model_result(deadline=None):
    return {
        "assignments": [{
            "assignment_title": "Biology · Lab report",
            "description": "Summarize the experiment.",
            "extracted_deadline": deadline,
            "deadline_confidence": "not_found" if deadline is None else "high",
            "deadline_source": None if deadline is None else "Due Nov 6",
            "requirements": ["Write a conclusion"],
            "estimated_hours": 2,
            "priority": "medium",
            "priority_reason": "No deadline was provided." if deadline is None else "Due soon.",
            "dependencies": [],
            "subtasks": [{"title": "Draft conclusion", "estimated_hours": 1, "completed": False}],
            "missing_information": ["Deadline not found"] if deadline is None else [],
        }],
        "daily_plan": ["Draft conclusion · Biology · 1 hour"],
    }


class SyllabusApiTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(main.app)

    def test_health_and_rejects_unsupported_mime(self):
        with patch.dict(os.environ, {}, clear=False):
            os.environ.pop("MODEL_API_KEY", None)
            self.assertFalse(self.client.get("/api/health").json()["ai_configured"])
        response = self.client.post("/api/analyze", files={"file": ("notes.txt", b"hello", "text/plain")})
        self.assertEqual(response.status_code, 415)

    def test_pdf_text_is_sent_and_absent_deadline_stays_null(self):
        pdf = fitz.open()
        pdf.new_page().insert_text((72, 72), "Lab report instructions. No date provided.")
        data = pdf.tobytes()
        captured = {}

        async def fake_meta(text, images):
            captured["text"] = text
            captured["images"] = images
            return model_result()

        with patch.object(main, "call_meta", fake_meta):
            response = self.client.post("/api/analyze", files={"file": ("lab.pdf", data, "application/pdf")})
        self.assertEqual(response.status_code, 200, response.text)
        self.assertIn("No date provided", captured["text"])
        self.assertIsNone(captured["images"])
        self.assertIsNone(response.json()["assignments"][0]["extracted_deadline"])

    def test_exact_deadline_quote_is_matched_to_pdf_page(self):
        pdf = fitz.open()
        pdf.new_page().insert_text((72, 72), "Course policies and grading information.")
        pdf.new_page().insert_text((72, 72), "Final paper due November 12, 2026.")
        data = pdf.tobytes()

        async def fake_meta(text, images):
            result = model_result("2026-11-12")
            result["assignments"][0]["deadline_source"] = "Final paper due November 12, 2026."
            return result

        with patch.object(main, "call_meta", fake_meta):
            response = self.client.post("/api/analyze", files={"file": ("syllabus.pdf", data, "application/pdf")})
        self.assertEqual(response.status_code, 200, response.text)
        assignment = response.json()["assignments"][0]
        self.assertEqual(assignment["extracted_deadline"], "2026-11-12")
        self.assertEqual(assignment["source_page"], 2)
        self.assertEqual(assignment["evidence_status"], "source_matched")

    def test_unmatched_deadline_is_cleared_and_marked_for_review(self):
        pdf = fitz.open()
        pdf.new_page().insert_text((72, 72), "Submit the lab report through the course portal.")
        data = pdf.tobytes()

        async def fake_meta(text, images):
            return model_result("2026-11-12")

        with patch.object(main, "call_meta", fake_meta):
            response = self.client.post("/api/analyze", files={"file": ("lab.pdf", data, "application/pdf")})
        assignment = response.json()["assignments"][0]
        self.assertIsNone(assignment["extracted_deadline"])
        self.assertEqual(assignment["deadline_confidence"], "low")
        self.assertEqual(assignment["evidence_status"], "manual_review")
        self.assertTrue(any("manual confirmation" in note for note in assignment["missing_information"]))

    def test_quote_must_contain_the_extracted_date(self):
        pdf = fitz.open(); pdf.new_page().insert_text((72, 72), "Lab report guidelines. Final submission is due December 10, 2026."); data = pdf.tobytes()

        async def fake_meta(text, images):
            result=model_result("2026-11-12")
            result["assignments"][0]["deadline_source"]="Lab report guidelines."
            return result

        with patch.object(main, "call_meta", fake_meta):
            response=self.client.post("/api/analyze", files={"file":("lab.pdf",data,"application/pdf")})
        assignment=response.json()["assignments"][0]
        self.assertIsNone(assignment["extracted_deadline"])
        self.assertEqual(assignment["evidence_status"],"manual_review")

    def test_deadline_on_scanned_image_requires_manual_review(self):
        image = fitz.open()
        image_data = image.new_page().get_pixmap().tobytes("png")

        async def fake_meta(text, images):
            return model_result("2026-11-12")

        with patch.object(main, "call_meta", fake_meta):
            response = self.client.post("/api/analyze", files={"file": ("announcement.png", image_data, "image/png")})
        assignment = response.json()["assignments"][0]
        self.assertEqual(assignment["evidence_status"], "manual_review")
        self.assertEqual(assignment["extracted_deadline"], "2026-11-12")

    def make_image_only_pdf(self, page_count):
        source = fitz.open()
        source.new_page(width=320, height=420).insert_text((50, 70), "Scanned assignment page")
        image = source[0].get_pixmap().tobytes("png")
        source.close()
        scanned = fitz.open()
        for _ in range(page_count):
            page = scanned.new_page(width=320, height=420)
            page.insert_image(page.rect, stream=image)
        data = scanned.tobytes()
        scanned.close()
        return data

    def test_scanned_pdf_pages_are_rendered_for_multimodal_analysis(self):
        captured = {}

        async def fake_meta(text, images):
            captured["text"] = text
            captured["images"] = images
            return model_result()

        with patch.object(main, "call_meta", fake_meta):
            response = self.client.post(
                "/api/analyze",
                files={"file": ("scanned-assignment.pdf", self.make_image_only_pdf(1), "application/pdf")},
            )
        self.assertEqual(response.status_code, 200, response.text)
        self.assertIn("rendered page images", captured["text"])
        page_images = [block for block in captured["images"] if block["type"] == "input_image"]
        self.assertEqual(len(page_images), 1)
        self.assertTrue(page_images[0]["image_url"].startswith("data:image/jpeg;base64,"))
        self.assertIn("Rendered scanned PDF page 1.", [block.get("text") for block in captured["images"]])

    def test_scanned_pdf_rendering_is_capped_at_five_pages(self):
        captured = {}

        async def fake_meta(text, images):
            captured["text"] = text
            captured["images"] = images
            return model_result()

        with patch.object(main, "call_meta", fake_meta):
            response = self.client.post(
                "/api/analyze",
                files={"file": ("long-scanned-syllabus.pdf", self.make_image_only_pdf(7), "application/pdf")},
            )
        self.assertEqual(response.status_code, 200, response.text)
        self.assertEqual(sum(block["type"] == "input_image" for block in captured["images"]), main.MAX_SCANNED_PDF_PAGES)
        self.assertIn("only the first 5 pages are included", captured["text"])

    def test_mixed_pdf_labels_text_pages_and_reports_omitted_scans(self):
        image_source=fitz.open(); image_data=image_source.new_page(width=320,height=420).get_pixmap().tobytes("png"); image_source.close()
        pdf=fitz.open();pdf.new_page().insert_text((72,72),"Course overview page")
        for _ in range(6):
            page=pdf.new_page(width=320,height=420);page.insert_image(page.rect,stream=image_data)
        data=pdf.tobytes();pdf.close();captured={}

        async def fake_meta(text,images):
            captured["text"]=text;captured["images"]=images;return model_result()

        with patch.object(main,"call_meta",fake_meta):
            response=self.client.post("/api/analyze",files={"file":("mixed.pdf",data,"application/pdf")})
        self.assertEqual(response.status_code,200,response.text)
        self.assertIn("[PAGE 1]",captured["text"])
        self.assertIn("Scanned pages not included",captured["text"])
        self.assertEqual(sum(block["type"]=="input_image" for block in captured["images"]),4)

    def test_schema_mismatch_from_model_returns_gateway_error(self):
        pdf = fitz.open(); pdf.new_page().insert_text((72, 72), "Assignment instructions."); data = pdf.tobytes()
        async def malformed_meta(text, images):
            return {"assignments": [{"assignment_title": "Incomplete"}], "daily_plan": []}
        with patch.object(main, "call_meta", malformed_meta):
            response = self.client.post("/api/analyze", files={"file": ("assignment.pdf", data, "application/pdf")})
        self.assertEqual(response.status_code, 502)

    def test_image_is_passed_as_multimodal_input(self):
        captured = {}
        image_doc = fitz.open()
        image_data = image_doc.new_page().get_pixmap().tobytes("png")

        async def fake_meta(text, images):
            captured["text"] = text
            captured["images"] = images
            return model_result()

        with patch.object(main, "call_meta", fake_meta):
            response = self.client.post("/api/analyze", files={"file": ("lms.png", image_data, "image/png")})
        self.assertEqual(response.status_code, 200, response.text)
        self.assertEqual(captured["images"][0]["type"], "input_image")
        self.assertTrue(captured["images"][0]["image_url"].startswith("data:image/png;base64,"))

    def test_rejects_file_with_mismatched_contents(self):
        response = self.client.post("/api/analyze", files={"file": ("notes.pdf", b"not a PDF", "application/pdf")})
        self.assertEqual(response.status_code, 415)

    def test_rejects_unreadable_pdf_with_valid_header(self):
        response = self.client.post("/api/analyze", files={"file": ("broken.pdf", b"%PDF-not-readable", "application/pdf")})
        self.assertEqual(response.status_code, 422)

    def test_malformed_model_json_returns_gateway_error(self):
        class Response:
            is_error = False
            status_code = 200
            def json(self):
                return {"output": [{"type": "message", "content": [{"type": "output_text", "text": "not json"}]}]}

        class Client:
            async def __aenter__(self): return self
            async def __aexit__(self, *args): return False
            async def post(self, *args, **kwargs): return Response()

        with patch.dict(os.environ, {"MODEL_API_KEY": "test-key"}), patch.object(main.httpx, "AsyncClient", lambda **kwargs: Client()):
            with self.assertRaises(HTTPException) as error:
                asyncio.run(main.call_meta("assignment text", None))
        self.assertEqual(error.exception.status_code, 502)

    def test_model_api_failure_returns_gateway_error(self):
        class Response:
            is_error = True
            status_code = 401

        class Client:
            async def __aenter__(self): return self
            async def __aexit__(self, *args): return False
            async def post(self, *args, **kwargs): return Response()

        with patch.dict(os.environ, {"MODEL_API_KEY": "test-key"}), patch.object(main.httpx, "AsyncClient", lambda **kwargs: Client()):
            with self.assertRaises(HTTPException) as error:
                asyncio.run(main.call_meta("assignment text", None))
        self.assertEqual(error.exception.status_code, 502)

    def test_model_api_retries_transient_rate_limit(self):
        class Response:
            def __init__(self, status_code):
                self.status_code = status_code
                self.is_error = status_code >= 400
            def json(self):
                return {"output": [{"type": "message", "content": [{"type": "output_text", "text": json.dumps(model_result())}]}]}

        class Client:
            def __init__(self): self.calls = 0
            async def __aenter__(self): return self
            async def __aexit__(self, *args): return False
            async def post(self, *args, **kwargs):
                self.calls += 1
                return Response(429 if self.calls == 1 else 200)

        client = Client()
        with patch.dict(os.environ, {"MODEL_API_KEY": "test-key"}), patch.object(main.httpx, "AsyncClient", lambda **kwargs: client), patch.object(main.asyncio, "sleep", new_callable=AsyncMock):
            result = asyncio.run(main.call_meta("assignment text", None))
        self.assertIn("assignments", result)
        self.assertEqual(client.calls, 2)

    def test_regenerated_plan_sorts_by_deadline_and_skips_completed_work(self):
        earlier = model_result("2026-11-05")["assignments"][0]
        later = model_result("2026-11-08")["assignments"][0]
        earlier["assignment_title"] = "Earlier task"
        later["assignment_title"] = "Later task"
        later["subtasks"].append({"title": "Already done", "estimated_hours": 0.5, "completed": True})
        response = self.client.post("/api/plan", json={"assignments": [later, earlier], "available_hours_per_day": 3})
        self.assertEqual(response.status_code, 200, response.text)
        result = response.json()
        self.assertEqual(result["assignments"][0]["assignment_title"], "Earlier task")
        self.assertTrue(all("Already done" not in action for action in result["daily_plan"]))


if __name__ == "__main__":
    unittest.main()
