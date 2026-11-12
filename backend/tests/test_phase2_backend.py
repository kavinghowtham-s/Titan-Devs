import pytest
from httpx import AsyncClient, ASGITransport
from backend.app.main import app
from backend.app.core.database import SessionLocal
from backend.app.models.message import OutboxMessage

@pytest.mark.asyncio
async def test_health_check_endpoint():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        res = await client.get("/health")
        assert res.status_code == 200
        data = res.json()
        assert data["status"] == "healthy"
        assert data["company"] == "Trentar Private Limited"

@pytest.mark.asyncio
async def test_webhook_ingestion_and_draft_creation():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        payload = {
            "channel": "email",
            "sender_address": "vikram@aerospacelabs.in",
            "subject": "Quote Request: Flight Controller",
            "raw_text": "Need quotation for 5 units of TRN-FC-PRO flight controller."
        }
        res = await client.post("/api/v1/messages/webhook", json=payload)
        assert res.status_code == 200
        data = res.json()
        assert data["id"] is not None
        assert data["detected_intent"] == "price_quote"
        assert data["processing_status"] in ["received", "drafted"]

@pytest.mark.asyncio
async def test_pending_drafts_and_manager_approval():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Get pending drafts
        res = await client.get("/api/v1/drafts/pending")
        assert res.status_code == 200
        drafts = res.json()
        assert len(drafts) > 0
        target_draft = drafts[0]
        draft_id = target_draft["id"]

        # Edit draft
        edit_payload = {"edited_text": "Updated draft with custom 2% partner discount."}
        res_edit = await client.put(f"/api/v1/drafts/{draft_id}/edit", json=edit_payload)
        assert res_edit.status_code == 200
        assert res_edit.json()["edited_text"] == edit_payload["edited_text"]

        # Approve draft
        res_approve = await client.post(f"/api/v1/drafts/{draft_id}/approve")
        assert res_approve.status_code == 200
        approved_data = res_approve.json()
        assert approved_data["status"] == "sent"
        assert approved_data["reviewed_by"] == "MANAGER_RAJESH"

        # Verify OutboxMessage was recorded in database
        db = SessionLocal()
        try:
            outbox = db.query(OutboxMessage).filter(OutboxMessage.draft_reply_id == draft_id).first()
            assert outbox is not None
            assert outbox.delivery_status == "DELIVERED"
            assert "Updated draft" in outbox.body_text
        finally:
            db.close()

