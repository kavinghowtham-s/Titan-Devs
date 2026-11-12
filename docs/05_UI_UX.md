# UI / UX Design & Wireframes — OpsPilot AI

**Project:** OpsPilot AI (Trentar Pvt Ltd)  
**Document Version:** 1.0.0  
**Target Device:** Modern Desktop Browser (Optimized for 1080p/4K Projector Presentations)  

---

## 1. Visual Direction & Design Tokens

OpsPilot AI uses an **Enterprise High-Contrast Industrial Dark/Light Theme** inspired by mission-control operations software. It is explicitly tailored for projector displays in hackathon auditoriums, avoiding low-contrast grays and ensuring all badges are bold and readable from 20 feet away.

- **Primary Colors:** Deep Slate (`#0F172A`), Industrial Navy (`#1E293B`), Accent Electric Cyan (`#06B6D4` / `#0284C7`).
- **Semantic Status Badges:**
  - `URGENT` / `HIGH RISK`: Crimson Red (`#EF4444` on `#450A0A`)
  - `HIGH PRIORITY` / `WARNING`: Amber Gold (`#F59E0B` on `#451A03`)
  - `AUTO-APPROVED` / `IN-STOCK`: Emerald Green (`#10B981` on `#064E3B`)
  - `PENDING REVIEW`: Cobalt Blue (`#3B82F6` on `#172554`)
- **Typography:** Inter / system-ui for crisp dashboard data rendering; JetBrains Mono / Fira Code for SQL and part numbers (SKUs).

---

## 2. Navigation Architecture & Shell

The application features a persistent **Top Utility Bar** and a **Left Sidebar**:

```
+---------------------------------------------------------------------------------------------------------+
| [TRENTAR OpsPilot AI]  | Model: llama3.3:70b [LIVE] | Demo Mode: [60s Auto-Timer] | Impact: MTTR 2.4m  |
+---------------------------------------------------------------------------------------------------------+
| [SIDEBAR]      | [MAIN WORKSPACE]                                                                       |
|                |                                                                                        |
| [1] Inbox (4)  |  Dynamic Page Container:                                                               |
| [2] Stock POs  |  - Split-Screen Inbox & Draft Approvals                                                |
| [3] Ask AI (Voice) |  - Supplier Stock Reorders                                                        |
| [4] Forecast & P&L |  - Multilingual Frontline Voice Assistant                                          |
| [5] Audit Log  |  - Demand Forecasting & P&L Insights                                                   |
| [6] Demo Admin |  - Compliance Audit Trail                                                              |
+---------------------------------------------------------------------------------------------------------+
```

---

## 3. Page Layouts & Text Wireframes

### 3.1 Page 1: Manager Inbox & Approvals (`/inbox`)
Split-pane interface designed for maximum review speed. The manager processes messages without context switching.

```
+----------------------------------------------------------------------------------------------------+
| INBOX & DRAFT APPROVALS                                     [Filter: All v] [Simulate Inbound v]   |
+-------------------------------------+--------------------------------------------------------------+
| INBOUND QUEUE (4 Pending)           | REVIEW & DISPATCH PANE                                       |
+-------------------------------------+--------------------------------------------------------------+
| [!] M02 | Deccan Drones | 2m ago    | INBOUND MESSAGE #M02                                         |
|     Bulk Order: 25x TRN-MOT-8318    | Sender: Sneha Reddy <sneha@deccandrones.in> | Channel: Email |
|     [SHORTFALL DETECTED] [URGENT]   | Received: 10:42 AM (4 mins ago)                              |
|     Language: English | Sent: Neutral|--------------------------------------------------------------|
|-------------------------------------| "Urgent requirement: Need 25 units of TRN-MOT-8318 motors    |
| [*] M03 | Coimbatore AgriTech | 8m  | for our surveillance contract. Deliver within 15 days."      |
|     Stock Inquiry (Tamil)           |--------------------------------------------------------------|
|     [PENDING] [HIGH] [Timer: 52s]   | INVENTORY REALITY CHECK:                                     |
|-------------------------------------| Item: TRN-MOT-8318 Heavy-Lift Motor                          |
| [ ] M05 | Skyline Mapping | 15m     | In-Hand Stock: 8 units | Requested: 25 | SHORTFALL: 17 units  |
|     Order Status Query              | [!] Automated Supplier PO #PO-4092 created for Kavach Drives |
|     [PENDING] [LOW] [Timer: 45s]    |--------------------------------------------------------------|
|-------------------------------------| AI GENERATED DRAFT REPLY [MODEL_DRAFTER]                     |
| [X] M09 | Suspicious Test | 20m     | Auto-Approve Timer: [||||||||||||||||....] 00:52 remaining   |
|     [INJECTION BLOCKED] [ESCALATED] |--------------------------------------------------------------|
|                                     | Dear Sneha,                                                  |
|                                     |                                                              |
|                                     | Thank you for reaching out to Trentar Pvt Ltd. We can        |
|                                     | immediately dispatch 8 units of TRN-MOT-8318 today.          |
|                                     |                                                              |
|                                     | Our procurement team has initiated an express batch order   |
|                                     | for the remaining 17 units from our verified drive supplier, |
|                                     | with scheduled delivery in 10 days. Total unit price is      |
|                                     | Rs. 14,500 + GST.                                            |
|                                     |                                                              |
|                                     | Best regards,                                                |
|                                     | Rajesh Kumar, Trentar Operations                             |
|                                     +--------------------------------------------------------------+
|                                     | [ EDIT DRAFT ]    [ REJECT ]    [ APPROVE & DISPATCH NOW ]   |
+-------------------------------------+--------------------------------------------------------------+
```

---

### 3.2 Page 2: Stock Orders & Shortfall Management (`/stock-orders`)
Displays supplier purchase orders automatically created from customer shortfalls (E2).

```
+----------------------------------------------------------------------------------------------------+
| SUPPLIER PURCHASE ORDERS (AUTOMATED STOCK REORDERS)                [Status: Draft (2) v]           |
+----------------------------------------------------------------------------------------------------+
| PO #            Supplier           Triggered By        Items & Deficit       PO Total     Action   |
+----------------------------------------------------------------------------------------------------+
| PO-2026-0042    Kavach Drives      Msg #M02 (Deccan)   17x TRN-MOT-8318      Rs. 1,51,300 [APPROVE]|
|                 Lead Time: 10d     Status: DRAFT       (Cost: Rs.8,900/ea)                [REJECT] |
+----------------------------------------------------------------------------------------------------+
| PO-2026-0043    Shakti Energy      Msg #M04 (Agro)     14x TRN-BAT-6S22A     Rs. 2,38,000 [APPROVE]|
|                 Lead Time: 18d     Status: DRAFT       (Cost: Rs.17,000/ea)               [REJECT] |
+----------------------------------------------------------------------------------------------------+
| PO-2026-0039    Garuda Composites  Msg #M14 (Indore)   22x TRN-PROP-3010     Rs.   57,200 [SENT OK]|
|                 Lead Time: 14d     Status: DISPATCHED  (Cost: Rs.2,600/ea)                [VIEW PO]|
+----------------------------------------------------------------------------------------------------+
| MODAL PREVIEW (Upon clicking APPROVE):                                                             |
| "Dispatch Purchase Order PO-2026-0042 to orders@kavachdrives.com?"                                 |
| Supplier Contact: Kavach Dynamic Drives | Terms: Net 30 | Delivery Address: Trentar Warehouse #2   |
| [ Cancel ]                                                  [ Confirm & Transmit to Supplier ]     |
+----------------------------------------------------------------------------------------------------+
```

---

### 3.3 Page 3: Ask Trentar AI (Safe Multilingual Voice Assistant — E3)
Designed for shop-floor and desk employees needing instant answers without knowing SQL.

```
+----------------------------------------------------------------------------------------------------+
| ASK TRENTAR AI — EMPLOYEE DATA ASSISTANT (SAFE TEXT-TO-SQL)                                        |
+----------------------------------------------------------------------------------------------------+
| Select Language: [ Tamil (தமிழ்) v ]   [ (•) Microphone Active ]    Mode: Read-Only SQLite (Safe)  |
+----------------------------------------------------------------------------------------------------+
|                                                                                                    |
| Voice Input / Prompt:                                                                              |
| [ "கடந்த 3 மாதங்களில் அதிக விற்பனையான பொருள் எது?"                                             ] [ASK] |
|                                                                                                    |
| [AUDIO OUTPUT]: [ > PLAY VOICE REPLY (Tamil Web Speech TTS) ]                                      |
|                                                                                                    |
| NATURAL LANGUAGE ANSWER:                                                                           |
| "கடந்த 3 மாதங்களில் அதிக விற்பனையான பொருள் 'High-Torque 4014 BLDC Motor' (SKU: TRN-MOT-4014) ஆகும்.     |
| மொத்தம் 185 யூனிட்கள் விற்பனை செய்யப்பட்டு, ரூ. 7,03,000 வருவாய் ஈட்டப்பட்டுள்ளது."               |
|                                                                                                    |
| DATA RESULTS TABLE:                                                                                |
| +---------------------+------------------------------+-------------+---------------+---------------+
| | SKU                 | Product Name                 | Total Sold  | Total Revenue | Avg Margin    |
| +---------------------+------------------------------+-------------+---------------+---------------+
| | TRN-MOT-4014        | High-Torque 4014 BLDC Motor  | 185 units   | Rs. 7,03,000  | 42.1%         |
| +---------------------+------------------------------+-------------+---------------+---------------+
|                                                                                                    |
| [v] EXECUTED SQL QUERY INSPECTOR (Audited & Whitelisted):                                          |
| SELECT p.sku, p.name, SUM(s.quantity_sold) as total_sold, SUM(s.total_revenue) as total_revenue    |
| FROM sales_history s JOIN products p ON s.product_id = p.id                                        |
| WHERE s.sale_date >= DATE('now', '-90 days') GROUP BY p.id ORDER BY total_sold DESC LIMIT 1;     |
+----------------------------------------------------------------------------------------------------+
```

---

### 3.4 Page 4: Predictive Forecast & Profit/Loss (E4)
Combines visual charts with an LLM executive narrative.

```
+----------------------------------------------------------------------------------------------------+
| PREDICTIVE DEMAND & FINANCIAL INTELLIGENCE (30-DAY OUTLOOK)              [Export Executive PDF]    |
+----------------------------------------------------------------------------------------------------+
| [ KEY OPERATIONAL METRICS ]                                                                        |
| Projected 30-Day Rev: Rs. 14.8 Lakhs | Projected COGS: Rs. 9.4 Lakhs | Gross Margin: 36.4% (+2.1%) |
| High Stockout Risk Items: 3 SKUs     | Recommended Reorders: 5 POs   | Working Capital: Healthy    |
+----------------------------------------------------------------------------------------------------+
| DEMAND FORECAST & BURN RATE CHART (Recharts) | TOP STOCKOUT RISKS                                  |
|                                              |                                                     |
| [ 100 |                     * Forecast       | 1. TRN-MOT-8318 (8318 100KV Motor)                  |
|   80  |            *-------*                 |    Stock: 8 | Lead Time: 14d | RISK: 85% [RED]     |
|   60  |        *--*                          | 2. TRN-BAT-6S22A (6S 22Ah Battery)                  |
|   40  |    *--*                              |    Stock: 6 | Lead Time: 18d | RISK: 78% [RED]     |
|   20  |*--*                                  | 3. TRN-SEN-RTK (RTK GNSS Receiver)                  |
|    0  +------------------------------------  |    Stock: 5 | Lead Time: 21d | RISK: 64% [AMBER]   |
|         Nov   Dec   Jan   Feb   Mar (Proj)   |                                                     |
+----------------------------------------------+-----------------------------------------------------+
| AI EXECUTIVE BRIEFING [MODEL_INSIGHTS]:                                                            |
| "Supply Chain Alert for Trentar Pvt Ltd:                                                           |
| 1. High-Torque 8318 Motors and 6S Solid-State Batteries are experiencing 40% surge in Q1 demand.    |
| 2. Current warehouse stock will deplete within 11 days, creating potential Rs. 3.2L revenue loss.  |
| 3. Immediate Action: Approve pending supplier PO-2026-0042 and PO-2026-0043 to lock in delivery."   |
+----------------------------------------------------------------------------------------------------+
```

---

### 3.5 Page 5: Audit Log (`/audit-logs`)
Chronological record proving AI governance, prompt-injection blocks, and auto-approval actions.

```
+----------------------------------------------------------------------------------------------------+
| SYSTEM COMPLIANCE & AUDIT TRAIL                             [Filter: System v] [Search: PO-...]   |
+----------------------------------------------------------------------------------------------------+
| Timestamp    Entity      Action          Actor                 Details                             |
+----------------------------------------------------------------------------------------------------+
| 10:43:10 AM  MSG #M09    INJECTION_BLOCK Guardrail Engine      Blocked injection payload in prompt |
| 10:42:15 AM  DRAFT #12   AUTO_APPROVED   SYSTEM_ORCHESTRATOR   Passed rules (Confidence: 0.98)    |
| 10:40:02 AM  PO #4042    CREATED         Stock Shortfall Eng   17 units shortfall for Deccan Drones|
| 10:35:40 AM  DRAFT #11   MANUAL_APPROVED Manager Rajesh        Sent to Vikram Patel via Email      |
| 10:30:12 AM  DRAFT #10   ESCALATED       SYSTEM_ORCHESTRATOR   Failed rule: Negative Sentiment     |
+----------------------------------------------------------------------------------------------------+
```

---

### 3.6 Page 6: Demo Control Center & Settings (`/settings`)
Interactive controls allowing the presenter to switch modes and demonstrate features in seconds.

```
+----------------------------------------------------------------------------------------------------+
| DEMO CONTROL CENTER & RUNTIME SETTINGS                                                             |
+----------------------------------------------------------------------------------------------------+
| LLM ENGINE MODE:                                                                                   |
| ( ) Live Ollama Cloud API (Bearer Key Active)                                                      |
| (*) Deterministic Offline Mock LLM (Zero Network Dependency - 100% Reliable Demo)                  |
|                                                                                                    |
| E1 AUTO-APPROVAL TIMER SPEED:                                                                      |
| ( ) Production Mode: 6 Hours (360 Minutes)                                                         |
| (*) Demo Presentation Mode: 60 Seconds (1 Minute Override)                                         |
|                                                                                                    |
| ONE-CLICK DEMO INGESTION TRIGGER:                                                                  |
| [ Ingest Normal Quote (M01) ]   [ Ingest Bulk Shortfall (M02) ]   [ Ingest Tamil Query (M03) ]     |
| [ Ingest Hindi Battery (M04) ]  [ Ingest Angry Complaint (M06) ]  [ Ingest Prompt Attack (M09) ]   |
+----------------------------------------------------------------------------------------------------+
```

---

## 4. Key Interactive Components & State Behaviors

### 4.1 Countdown Timer Component (`CountdownTimer.tsx`)
- Displays time remaining before the Orchestrator evaluates the draft for autonomous approval.
- **Visual Thresholds:**
  - `> 30% time remaining`: Soft Blue / Slate progress bar (`text-blue-400`).
  - `10% to 30% remaining`: Pulsing Amber indicator (`text-amber-400 animate-pulse`).
  - `< 10% remaining`: Urgent Crimson Red with warning icon (`text-red-500 font-bold`).
- Upon reaching `00:00`, the component triggers a background query invalidation; the card flips to show either `[AUTO-APPROVED - DISPATCHED]` or `[ESCALATED TO MANAGER]`.

### 4.2 Loading, Empty, and Error States
- **Loading:** Shimmering skeleton loaders preserving exact card dimensions to prevent cumulative layout shift (CLS).
- **Empty Inbox:** Clean vector illustration with label: *"All customer communications processed. Operations running at 100% efficiency."*
- **Error Banner:** Non-blocking top toast alert with retry button: *"LLM connection slow. Switched to deterministic response cache."*

