# OpsPilot AI — Comprehensive Bug Log & Stabilization Tracker

**Document Version:** 1.1.0  
**Status:** Step 1 (Error Collection) COMPLETE. Step 3 (Root-Cause Fixes) Initiated.  
**Rule:** Fix root causes. Reproduce before fixing, verify after fixing. Zero suppression flags (`ts-ignore`, empty except).

---

## 1. Master Bug Table

| Bug ID | Subsystem | Severity | Symptom | Steps to Reproduce | Root Cause | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **BUG-03** | E1 Auto-Approve | **P0** | `POST /api/v1/drafts/process-expirations` crashes with HTTP 500 (`AttributeError: 'InboundMessage' object has no attribute 'sentiment'`). | Trigger `POST /api/v1/drafts/process-expirations` with pending expired drafts. | In `DraftService.process_expired_drafts`, code accessed `inbound.sentiment` and `inbound.intent`, but database column names on `InboundMessage` model are `detected_sentiment` and `detected_intent`. | **Open** |
| **BUG-08** | E1 Auto-Approve | **P0** | Expired drafts are not automatically evaluated by Orchestrator in the background without explicit external API invocation. | Wait >60s in demo mode with a pending draft. Draft remains in `pending` status indefinitely until manual trigger. | Background periodic worker loop was omitted from FastAPI `lifespan` in `backend/app/main.py`. | **Open** |
| **BUG-01** | Platform | **P1** | No single-command startup script (`run.bat` / `run.sh`) exists in project root. | Check root folder for `run.bat` or `run.sh`. Neither file exists. | Missing script scaffolding for Windows / POSIX environments with port pre-checks. | **Open** |
| **BUG-02** | LLM Drafter | **P1** | Motor inquiry ("Need 25 units of TRN-MOT-8318") generates flight controller quote (`TRN-FC-PRO`). | Call `llm_client.generate_draft` with message "Need 25 units of TRN-MOT-8318". Drafter subject references `TRN-FC-PRO`. | In `mock_llm.py`, condition checked `"5 units" in lower`, which greedily substring-matched `"25 units"`, overriding the motor template. | **Open** |
| **BUG-04** | LLM Client | **P1** | `POST /api/v1/settings/test-connection` takes >12s and can time out client requests. | Call `/api/v1/settings/test-connection` with default HTTP client timeout (10s). Request times out. | `test_connection()` iterates through all 5 model roles sequentially rather than running concurrently via `asyncio.gather`. | **Open** |
| **BUG-05** | Core Inbox | **P1** | Double-clicking "Approve & send" sends duplicate outbound messages and writes multiple audit entries. | Call `POST /api/v1/drafts/{id}/approve` twice on the same draft. Both calls return 200 and add 2 outbox entries. | `DraftService.approve_draft` lacks idempotency guard (`if draft.status in ('sent', 'approved')`). | **Open** |
| **BUG-06** | E2 Stock Orders | **P1** | `POST /api/v1/stock-orders/{id}/reject` is listed in `docs/04_API_AND_AGENTS.md` line 36 but missing from stock API router. | Call `POST /api/v1/stock-orders/1/reject`. Returns HTTP 405 Method Not Allowed or 404. | Endpoint route handler was omitted from `backend/app/api/v1/stock.py`. | **Open** |
| **BUG-09** | E3 Assistant | **P1** | Multi-statement queries could evade single-statement AST validation if semicolons separate statements. | Pass `SELECT 1; DROP TABLE products;` to `validate_and_sanitize_sql`. | Uses `sqlglot.parse_one` rather than strictly checking `len(sqlglot.parse(clean_sql)) == 1`. | **Open** |
| **BUG-11** | Backend Tests | **P1** | Running `pytest backend/tests` fails with `ModuleNotFoundError: No module named 'backend'`. | Run `pytest backend/tests` in repository root. | No `pytest.ini` exists configuring `pythonpath = .`. | **Open** |
| **BUG-12** | Backend Tests | **P1** | `test_phase1.py::test_database_tables_and_seed_data` fails if simulation messages were ingested during runtime (`assert 19 == 15`). | Run tests against development database with simulated messages. | Test checks exact `len(messages) == 15` rather than `>= 15`. | **Open** |
| **BUG-07** | UI Detail Pane | **P2** | When an inbound message has no draft (e.g. security prompt injection flagged), lower half of detail panel is blank. | Click on message M09 (prompt injection) in Inbox. Inbound message is shown with red warning, but no draft card or fallback status appears. | `DraftReviewCard` does not render a dedicated empty state when `draft == null` and message is non-actionable. | **Open** |
| **BUG-10** | Ingestion Audit | **P2** | DRAFT CREATED audit log entry records `entity_id = inbound.id` instead of `draft.id`. | Ingest message, query `GET /api/v1/audit/logs`. DRAFT CREATED row has `entity_id` equal to message ID. | `draft` model instance was not flushed before writing `AuditLog` record in `message_service.py`. | **Open** |
| **BUG-13** | UI Polish | **P2** | `AnalyticsPage` renders an empty space above the charts on initial mount before data resolves. | Navigate to Forecast tab; cards and tables pop into existence abruptly. | Missing clean loading state / skeleton placeholders during initial async fetch. | **Open** |

---

## 2. Priority Fix Execution Order

1. **P0 Fixes (Critical Demo Blockers):**
   - Fix **BUG-03**: Correct attribute names on `InboundMessage` in `DraftService.process_expired_drafts`.
   - Fix **BUG-08**: Wire standing background worker loop for expired drafts in `backend/app/main.py` lifespan.

2. **P1 Fixes (Core Behavior, Safety & Testing):**
   - Fix **BUG-02**: Fix Drafter substring regex/word-boundary check for quantities in `mock_llm.py`.
   - Fix **BUG-05**: Add idempotency guard to `DraftService.approve_draft`.
   - Fix **BUG-06**: Implement `POST /api/v1/stock-orders/{id}/reject` in `stock.py`.
   - Fix **BUG-09**: Harden SQL AST sanitizer to strictly enforce `len(statements) == 1`.
   - Fix **BUG-04**: Convert `test_connection()` to concurrent `asyncio.gather`.
   - Fix **BUG-11**: Add `pytest.ini` with `pythonpath = .`.
   - Fix **BUG-12**: Update test assertion `assert len(messages) >= 15`.
   - Fix **BUG-01**: Create `run.bat` (Windows) and `run.sh` (Linux/macOS) with port checks.

3. **P2 Fixes (Polish & Audit Precision):**
   - Fix **BUG-10**: Flush `draft` before creating DRAFT CREATED `AuditLog` in `message_service.py`.
   - Fix **BUG-07**: Add dedicated non-draft / security status block in `DraftReviewCard.tsx`.
   - Fix **BUG-13**: Add skeleton loading state in `AnalyticsPage.tsx`.
