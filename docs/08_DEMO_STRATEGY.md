# Hackathon Demo Strategy & Script — OpsPilot AI

**Project:** OpsPilot AI (Trentar Pvt Ltd)  
**Target Event:** Hackathon Presentation (Judges Panel)  
**Total Presentation Window:** 5 Minutes (3.5 mins live demo + 1.5 mins Q&A defense)  
**Document Version:** 1.0.0  

---

## 1. Minute-by-Minute Live Demo Script

```mermaid
journey
    title 5-Minute Hackathon Demo Narrative Flow
    section The Problem (0:00 - 0:45)
      Hook: SME Manufacturing Inefficiency : 5: Speaker
      Show Shared Inbox Chaos & Lag : 3: Judges
    section Core + Stock Shortfall E2 (0:45 - 1:45)
      Ingest Bulk Order M02 (Deccan Drones) : 5: System
      Show In-Hand Stock vs Shortfall : 5: Judges
      Generate Supplier PO for Kavach Drives : 5: Manager UI
    section 6-Hour Auto-Approval E1 (1:45 - 2:45)
      Show 60s Demo Countdown on Routine Draft : 4: Screen
      Auto-Approval Dispatches at 00:00 : 5: Judges
      Show Angry Complaint Escalated for Safety : 5: System
    section Voice Employee Assistant E3 (2:45 - 3:45)
      Speak Tamil Query to Ask Trentar AI : 5: Presenter
      Execute Read-Only SQL & Spoken Audio : 5: Judges
    section Forecast E4 & Impact Close (3:45 - 5:00)
      Show 30-Day Demand Chart & AI Briefing : 4: Screen
      Present Live PS#601 Impact Scorecard : 5: Judges
```

---

### Segment 1: The Hook & Real-World Context (0:00 – 0:45)
- **Speaker Action:** Stand center stage, address judges directly with confidence.
- **Spoken Script:**  
  *"Good morning judges. In India, medium-scale precision manufacturers like Trentar Pvt Ltd power our defense, drone, and industrial supply chains. But behind high-tech manufacturing lies an operational nightmare: managers spend 4 to 5 hours every single day manually sorting emails, calling warehouses to check inventory, calculating shortfalls on scraps of paper, and typing repetitive quotes.*  
  *When customer responses take 18 hours, deals are lost. When stockouts aren't caught instantly, production lines stop.*  
  *Meet **OpsPilot AI** — an autonomous operational co-pilot built specifically for Trentar to digitize customer response, automate inventory reordering, and safeguard operations."*
- **Screen Action:** Display the **OpsPilot AI** Command Center dashboard. Show the top impact banner: `Baseline MTTR: 14 hrs -> OpsPilot MTTR: 2.4 mins`.

---

### Segment 2: Core Ingestion + Stock Shortfall Automation [E2] (0:45 – 1:45)
- **Speaker Action:** Click the "Simulate Inbound" trigger for **Message #M02 (Deccan Drones)**.
- **Spoken Script:**  
  *"Let's look at a live customer order. Deccan Drones sends an urgent inquiry: they need 25 heavy-lift motors (`TRN-MOT-8318`) within 15 days.*  
  *Notice what OpsPilot AI did in under two seconds:  
  First, our Intake Agent extracted the SKU, quantity, and priority.  
  Second, our Stock Engine checked real-time warehouse inventory: Trentar only has 8 units in stock — a shortfall of 17 units!  
  Third, the Drafter LLM composed an intelligent, honest customer reply: confirming immediate dispatch of the 8 available units today, while reassuring them the remainder is in production.*  
  *And look at this: it didn't just write a draft — it automatically created **Supplier Purchase Order PO-2026-0042** for our verified motor supplier, Kavach Drives, with exact wholesale costing. With one click, Manager Rajesh approves both."*
- **Screen Action:**  
  1. Click into Message #M02. Show side-by-side view with inventory deficit highlighted in amber.
  2. Switch to **Stock Orders** tab; click **[Approve PO]**. Show instant status transition to `DISPATCHED_TO_SUPPLIER`.

---

### Segment 3: Autonomous 6-Hour Auto-Approval & Safety Guardian [E1] (1:45 – 2:45)
- **Speaker Action:** Point to the countdown timer on pending routine inquiry **Message #M05**.
- **Spoken Script:**  
  *"Now, what happens if Manager Rajesh is on the factory floor or traveling? In traditional operations, emails sit unanswered.  
  OpsPilot AI has a built-in 6-hour autonomous fail-safe. For demo purposes, we have dialed the timer down to 60 seconds.*  
  *Watch Message M05 — a routine order status request. The timer reaches zero... and our **Safety Orchestrator Agent** kicks in. It audits the draft against strict corporate rules: sentiment is polite, no unauthorized discounts, no legal exposure. Verdict: PASS. It automatically dispatches the email!*  
  *But what about hostile or sensitive messages? Look at Message M06 — an angry customer reporting a damaged sensor pin. The Orchestrator immediately caught the negative sentiment, BLOCKED auto-approval, and escalated it with a red urgent badge. Complete AI autonomy with 100% human-in-the-loop safety."*
- **Screen Action:**  
  1. Show countdown timer hit `00:00` on M05 -> card flashes green `[AUTO-APPROVED & SENT]`.
  2. Point to M06 showing red `[ESCALATED: HIGH SENTIMENT RISK]`.

---

### Segment 4: Frontline Multilingual Voice Assistant [E3] (2:45 – 3:45)
- **Speaker Action:** Navigate to **"Ask Trentar AI"**. Select Tamil (`தமிழ்`) and click the Microphone icon (or sample query pill).
- **Spoken Script:**  
  *"Operations aren't just managers in offices; frontline warehouse staff need answers fast, and they don't know SQL. Ananya on the shop floor can simply speak in her native language."*
- **Voice Query (Spoken or Clicked):**  
  *"கடந்த 3 மாதங்களில் அதிக விற்பனையான பொருள் எது?"* (Which item sold the most in the last 3 months?)
- **System Output:**  
  - The UI generates the exact SQL query in the inspector drawer.
  - The data table renders the top motor (`TRN-MOT-4014`, 185 units, ₹7.03L).
  - The browser speaks aloud in crisp Tamil: *"கடந்த 3 மாதங்களில் அதிக விற்பனையான பொருள் High-Torque 4014 BLDC Motor ஆகும்..."*
- **Spoken Script:**  
  *"Notice the architecture: this is executed through a sandboxed, read-only SQLite connection with AST statement whitelisting. It is impossible to drop tables or inject malicious queries."*

---

### Segment 5: Predictive Analytics [E4] & Impact Close (3:45 – 5:00)
- **Speaker Action:** Click on **"Forecast & P&L"** tab.
- **Spoken Script:**  
  *"Finally, OpsPilot AI shifts Trentar from reactive fire-fighting to proactive intelligence.  
  Using 12 months of sales records, our forecasting engine models 30-day demand curves and stockout probabilities.  
  Our AI Executive Briefing immediately flags that heavy-lift motors and solid-state batteries are on course to stock out within 11 days, risking ₹3.2 Lakhs in lost revenue — and tells management exactly which POs to authorize.*  
  *To summarize our impact on Problem Statement PS#601:*  
  - **Response Time:** Reduced from 18 hours to under 3 minutes.  
  - **Manual Effort:** 85% reduction in routine operational drafting.  
  - **Supply Chain Continuity:** Real-time stockout shortfall detection.  
  *OpsPilot AI turns manual SME operations into an intelligent, digitized powerhouse. Thank you, and we welcome your questions."*

---

## 2. Alignment with Judging Criteria

| Judging Dimension | What Judges Care About | How OpsPilot AI Wins the Category |
| :--- | :--- | :--- |
| **Innovation (25%)** | Novel application of AI beyond generic wrappers. | Two-tiered agent architecture (Drafter + Safety Orchestrator) with autonomous fail-safe auto-approval and multi-language voice SQL engine. |
| **Practicality & Feasibility (25%)** | Can an SME actually deploy this without millions in budget? | Zero-cost local footprint: uses SQLite, browser-native Web Speech API, and Ollama Cloud/Local models. Single-command startup. |
| **Problem Statement Impact (20%)** | Direct alignment with PS#601 objectives. | Explicitly addresses customer response speed (MTTR), operational manual overhead, and supplier coordination in one unified system. |
| **Technical Scalability & Security (15%)**| Robustness, security guardrails, resilience. | AST-validated read-only SQL, prompt-injection neutralization, persistent database-driven timer (survives crashes), WAL concurrency. |
| **UX & Presentation Polish (15%)** | High-clarity visuals and demo fluency. | High-contrast industrial UI, live visual countdown timers, instant optimistic updates, and crisp multilingual voice interaction. |

---

## 3. Bulletproof Demo Fallback Protocol

To guarantee a zero-fail demo even in adversarial venue conditions, the team follows this tiered contingency protocol:

```
[ LEVEL 1: FULL CLOUD LIVE ]
  - Live Ollama Cloud API (Bearer key in .env).
  - Web Speech API microphone input.
  - Live background APScheduler timer.

        | (If Wi-Fi drops or latency > 5s)
        v

[ LEVEL 2: DETERMINISTIC MOCK MODE ]
  - Toggle 'USE_MOCK_LLM=true' in UI or press 'Ctrl+M'.
  - Backend returns instantaneous, high-fidelity mock JSON for all 15 pre-seeded scenarios.
  - Zero external HTTP calls; runs 100% locally on localhost:8000 and localhost:5173.

        | (If microphone echo or permission issue occurs)
        v

[ LEVEL 3: PRE-SET AUDIO & QUERY PILLS ]
  - Click the quick-query pill: "Top 3 Selling Motors (Tamil)".
  - Browser executes exact SQL query and triggers local Web Speech synthesis without microphone.
```

