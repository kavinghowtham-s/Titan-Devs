# Product Requirements Document (PRD) — OpsPilot AI

**Project Name:** OpsPilot AI  
**Target Organization:** Trentar Private Limited  
**Problem Statement:** PS#601 — "Improve Business Operations and Customer Response Speed Through Digitization and AI"  
**Document Version:** 1.0.0 (Hackathon Architecture Baseline)  
**Status:** Approved for Planning  

---

## 1. Executive Summary & Problem Context

Small and medium-scale industrial manufacturers like Trentar Private Limited handle hundreds of daily B2B communications across emails, WhatsApp, and procurement portals. Today, these operations are governed by manual, fragmented workflows:
- Customer inquiries (specifications, quotes, stock availability, order tracking) sit in shared mailboxes for hours or days.
- Inquiries requiring stock checks trigger manual phone calls or ERP lookups between sales and warehouse staff.
- Routine confirmations and stock reorders require repetitive drafting by busy operational managers, creating severe response latency and stockout risks.

**OpsPilot AI** digitizes and automates these operations. It intercepts incoming customer messages, parses intent, entities, sentiment, and priority via LLMs, logs them into a central operational database, calculates stock availability in real time, auto-drafts customer replies and supplier purchase orders, and provides a safe manager-in-the-loop dashboard with a 6-hour autonomous fail-safe. Frontline employees also gain a safe, multilingual voice-enabled Text-to-SQL assistant, and management receives predictive inventory and profit/loss insights.

---

## 2. Personas

| Persona | Role & Demographics | Goals | Pain Points & Frustrations |
| :--- | :--- | :--- | :--- |
| **Rajesh Kumar** *(Primary)* | Operations Manager, Trentar Pvt Ltd (12 yrs exp.) | Maintain < 1 hr response time, avoid inventory stockouts, review critical business communications without getting bogged down in repetitive typing. | Drowning in 80+ routine emails/day; manually cross-referencing warehouse counts; worried about unaddressed emails during travel or peak shifts. |
| **Ananya Sharma** *(Secondary)* | Frontline Sales & Inventory Coordinator | Quickly answer customer queries regarding past orders, current inventory, and delivery timelines without bugging DBAs or engineers. | Does not know SQL; struggles to extract quick trends from raw database tables; handles multilingual calls (Tamil, Hindi, English). |
| **Vikram Patel** *(External)* | B2B Procurement Officer (Customer / Client) | Receive immediate quotes, confirmed availability, and fast order fulfillment for precision components. | Delayed quotations force him to source from competing vendors; lack of order transparency. |
| **Murugan S.** *(External)* | Component Supplier / Vendor | Receive clean, structured purchase orders with clear part numbers and required delivery dates. | Scrambled, emergency phone-call orders with ambiguous quantities and missing specs. |

---

## 3. User Stories & Acceptance Criteria

### Core Feature 1: Multi-Channel Inbound Logging & Parsing
- **User Story:** As an Operations Manager, I want incoming customer emails and messages to be automatically parsed and classified into a centralized operational queue so that my team never misses a high-priority customer request.
- **Acceptance Criteria:**
  1. Inbound messages from Simulated Email, WhatsApp Stub, or Webhook are ingested and assigned an immutable ID and timestamp.
  2. The Intake LLM extracts: Customer ID/Name, Language (En/Ta/Hi/other), Primary Intent (`price_quote`, `bulk_order`, `order_status`, `complaint`, `stock_inquiry`, `general`), Sentiment (`positive`, `neutral`, `negative`, `frustrated`), Priority (`low`, `medium`, `high`, `urgent`), and Extracted SKUs/Quantities.
  3. Every message is persisted in SQLite with state `received` and displayed in the manager inbox within 1.5 seconds.
  4. Untrusted customer message text is sanitized; prompt injection payloads are neutralized and flagged.

### Core Feature 2: Contextual Draft Generation & Manager-in-the-Loop Review
- **User Story:** As an Operations Manager, I want the system to generate an accurate, professional draft reply referencing our real catalog and inventory data, so that I can review, edit, and send it with one click.
- **Acceptance Criteria:**
  1. The Drafter LLM produces a context-aware response incorporating customer tone, product pricing, and inventory reality.
  2. The Manager Dashboard presents a side-by-side view: original message, extracted metadata, draft reply, and action buttons (`Approve`, `Edit`, `Reject`).
  3. Clicking `Approve` dispatches the message via the corresponding channel adapter and updates status to `approved` -> `sent`.
  4. Clicking `Edit` allows in-place rich text editing before dispatch; changes are logged in the audit trail.
  5. Clicking `Reject` prompts for an optional rejection reason, cancels dispatch, and moves the item to `rejected`.

---

### Extra 1 (E1): 6-Hour Autonomous Safety-Governed Auto-Approval
- **User Story:** As a Business Owner, I want routine customer drafts to be safely auto-approved and dispatched if the manager does not act within 6 hours, so that response times remain world-class even outside business hours.
- **Acceptance Criteria:**
  1. An asynchronous background scheduler monitors pending drafts with `age >= 6 hours` (configurable via `AUTO_APPROVE_DELAY_MINUTES`; 1-minute demo override supported).
  2. Pending drafts exceeding the threshold trigger the Orchestrator/Safety LLM to perform rule-based compliance checks:
     - Is the customer sentiment non-negative (no complaints/legal threats)?
     - Is the intent routine (e.g. stock inquiry, standard pricing, catalog request)?
     - Does the draft avoid unauthorized discounts (> 5%) and speculative delivery dates?
     - Is prompt injection confidence == 0?
  3. If all safety rules pass: status transitions to `auto_approved` -> `sent`, and an audit event is logged.
  4. If safety rules fail: status transitions to `escalated`, priority escalates to `urgent`, and the manager is notified with an explicit risk flag.
  5. The UI shows an active countdown timer on each pending draft that visually updates and turns amber/red as expiry nears.

---

### Extra 2 (E2): Automated Stock Check, Shortfall Computation & Supplier PO Generation
- **User Story:** As an Operations Manager, when a customer requests items in quantities exceeding our warehouse stock, I want the system to automatically compute the shortfall and generate a Supplier Purchase Order draft, so that reordering happens instantaneously.
- **Acceptance Criteria:**
  1. During ingestion of `bulk_order` or `stock_inquiry`, the system extracts SKU and requested quantity, cross-referencing `products.current_stock`.
  2. If `requested_qty > current_stock`, the system calculates: `shortfall = requested_qty - current_stock + safety_buffer`.
  3. The system maps the SKU to its primary vendor from `suppliers` and generates a structured `Stock Order Draft` with unit cost, total PO amount, and vendor contact info.
  4. The Manager Dashboard features a dedicated "Stock Orders" tab showing pending POs linked to the originating customer message.
  5. Upon manager approval, the PO is marked `approved` -> `dispatched_to_supplier` and recorded in the audit log.

---

### Extra 3 (E3): Safe Multilingual Text-to-SQL Employee Assistant
- **User Story:** As a Frontline Employee, I want to ask questions in plain English, Tamil, or Hindi using text or voice and receive accurate data insights from our database, so that I can resolve operational questions in seconds without technical knowledge.
- **Acceptance Criteria:**
  1. Accepts text input or browser Web Speech API voice input in English (`en-IN`), Tamil (`ta-IN`), and Hindi (`hi-IN`).
  2. Uses a schema-aware SQL Agent with strict security guardrails: Read-Only SQLite connection, AST validation ensuring `SELECT` only (rejects `INSERT`, `UPDATE`, `DELETE`, `DROP`, `ALTER`, `ATTACH`, `PRAGMA`), and mandatory `LIMIT 50`.
  3. Executes the query against Trentar's operational database and returns:
     - Executed SQL query (for full transparency in a collapsible developer drawer).
     - Clean tabular data result.
     - Natural language conversational answer in the query's input language.
  4. Provides browser Web Speech Synthesis audio playback of the response in the matched language.

---

### Extra 4 (E4): Predictive Stock Analysis & Profit/Loss Forecasting
- **User Story:** As an Executive/Manager, I want to view demand forecasts, stock-out probabilities, recommended reorder quantities, and projected profit/loss with an AI-generated briefing, so that our supply chain remains resilient and profitable.
- **Acceptance Criteria:**
  1. Computes 30-day forward demand forecast per product using weighted moving averages and historical run-rates from 12 months of sales records.
  2. Computes **Stock-out Risk Score (0-100%)** based on current inventory, lead time, and forecasted burn rate.
  3. Displays Reorder Recommendations: `Reorder Point = (Daily Demand * Lead Time) + Safety Stock`.
  4. Displays financial metrics: Projected Gross Revenue, Cost of Goods Sold (COGS), Projected Gross Margin, and Net Profit.
  5. Integrates an "AI Executive Insights" card summarizing top risks, fastest-moving SKUs, and immediate recommended procurement actions.

---

## 4. Scope & Feature Classification (MoSCoW for 24-Hour Hackathon)

| Priority | Feature Component | Hackathon Scope Details |
| :--- | :--- | :--- |
| **MUST HAVE** | Core Ingestion & Extraction | Email simulator, intent/sentiment/priority classification, SQLite persistence. |
| **MUST HAVE** | Core Drafter & Approval UI | LLM contextual reply generation, split-screen Manager Inbox with Approve/Edit/Reject. |
| **MUST HAVE** | Mock LLM Architecture | Deterministic, zero-dependency offline mode selectable via `.env` or UI toggle. |
| **MUST HAVE** | E1: 6-Hour Auto-Approval | APScheduler job, safety Orchestrator check, 1-minute demo override, active countdown UI. |
| **MUST HAVE** | E2: Stock Check & Supplier PO | SKU shortfall detection, automated supplier PO draft creation, manager PO approval flow. |
| **SHOULD HAVE**| E3: Safe Text-to-SQL Engine | Read-only connection, AST parser validation, table whitelist, result table + natural reply. |
| **SHOULD HAVE**| E3: Web Speech Voice I/O | Browser native Web Speech API for Tamil, Hindi, and English voice input and output. |
| **COULD HAVE** | E4: Predictive Demand & P&L | 30-day forecast formula, Recharts visualization, AI summary card. |
| **COULD HAVE** | Real SMTP/IMAP Adapter | Optional background worker connecting to live Gmail/Outlook if credentials provided. |
| **WON'T HAVE** | Full ERP Integration | Direct SAP/Oracle connectors (simulated via local SQLite schema). |
| **WON'T HAVE** | Custom Fine-Tuned LLM | Training or fine-tuning weights; prompt engineering + Ollama cloud models used exclusively. |
| **WON'T HAVE** | Payment Gateway | Real payment gateway processing for invoices or purchase orders. |

---

## 5. Problem Statement PS#601 Outcome Mapping & Demo Impact Metrics

The dashboard features a live **"Impact Scorecard"** widget specifically highlighting metrics aligned with PS#601 judging criteria:

| PS#601 Outcome | Trentar Operational Metric | Baseline Manual Process | OpsPilot AI Target | Dashboard Display Widget |
| :--- | :--- | :--- | :--- | :--- |
| **Faster Customer Response** | Mean Time to Respond (MTTR) | 4 to 18 hours | **< 3 minutes** (manager) / **Immediate** (auto) | Live MTTR Clock & Delta Tracker |
| **Operational Efficiency** | Manual Drafting Hours Saved | ~4.5 hours / manager / day | **85% reduction** (< 40 mins / day) | "Hours Saved This Week" Counter |
| **Routine Activity Automation** | % Inquiries Auto-Processed | 0% (100% manual) | **40-60%** routine auto-approval rate | "Autonomous Resolution Rate" Pie Gauge |
| **Supply Chain Continuity** | Stockout Shortfall Detection Time | 1 to 2 business days | **Real-Time (< 5 seconds)** | "Shortfall POs Automated" Counter |
| **Customer Satisfaction** | First-Contact Resolution (FCR) | 42% | **88%+** | Customer Sentiment Trend Graph |
