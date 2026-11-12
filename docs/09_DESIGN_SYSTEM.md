# Design System Specification — OpsPilot AI (v2.0)

**Product:** OpsPilot AI — Trentar Operations Platform  
**Design Philosophy:** Linear / Stripe / Front / Notion inspired. High-density, calm, professional B2B operational workstation.  
**Target Environment:** Desktop Browser (optimized for light theme in brightly-lit conference rooms and 1080p/4K projectors), with dark theme support.  
**Document Version:** 2.0.0 (Full Overhaul)  

---

## 1. Visual Strategy & Principles

1. **Calm, High-Density Utility:** Built as a daily workhorse for operations teams. Whitespace, typography size/weight, and clean 1px borders define structure—not nested cards with heavy glow or neon drop-shadows.
2. **Subtle Brand, Zero Decorative Distractions:** A single restrained **Deep Ink Blue (`#1D4ED8`)** brand accent used selectively for primary calls-to-action (e.g. "Approve & send"). Neutral grays (`#0F172A` down to `#F8FAFC`) handle 95% of the interface.
3. **Semantic Status Only:** Color is strictly reserved for business meaning:
   - **Pending Review:** Amber (`#B45309` on `#FEF3C7`, border `#FDE68A`)
   - **Approved / Dispatched:** Emerald (`#047857` on `#ECFDF5`, border `#A7F3D0`)
   - **Auto-Approved (6-Hour):** Teal (`#0F766E` on `#F0FDFA`, border `#99F6E4`)
   - **Escalated / Needs Review:** Red-Orange (`#B91C1C` on `#FEF2F2`, border `#FECACA`)
   - **Rejected / Discarded:** Slate (`#475569` on `#F1F5F9`, border `#E2E8F0`)
4. **No Internal Leakage or Hacker Cliches:**
   - Monospace font is restricted **only** to SKUs (`TRN-MOT-8318`), system IDs (`PO-2026-0042`), and raw SQL queries.
   - All labels, metrics, buttons, and navigation use natural enterprise sentence/title case with standard letter-spacing.
   - Internal phase markers (`E2`, `E3`), model identifiers (`MODEL_DRAFTER`), and hackathon slogans are removed from customer-facing views.

---

## 2. Color Palette & Surface Hierarchy

### Light Theme (Default & Primary Presentation Mode)

| Role | Hex | Tailwind Token | Usage |
| :--- | :--- | :--- | :--- |
| **App Canvas / Background** | `#F8FAFC` | `bg-slate-50` | Base page background behind all panes |
| **Surface / Card** | `#FFFFFF` | `bg-white` | Active panes, tables, email composer |
| **Sidebar / Chrome Surface**| `#F1F5F9` | `bg-slate-100` | Subtle contrast for persistent side navigation |
| **Border / Divider** | `#E2E8F0` | `border-slate-200` | Clean 1px dividers, zero glowing shadows |
| **Border Subtle** | `#F1F5F9` | `border-slate-100` | Internal list item separators |
| **Text Primary** | `#0F172A` | `text-slate-900` | Headings, sender names, core email body |
| **Text Secondary** | `#475569` | `text-slate-600` | Subtitles, timestamps, metadata labels |
| **Text Tertiary / Muted** | `#94A3B8` | `text-slate-400` | Helper text, placeholder copy |
| **Primary CTA (Ink Blue)** | `#1D4ED8` | `bg-blue-700 hover:bg-blue-800` | "Approve & send" hero button |
| **Secondary Button** | `#FFFFFF` | `bg-white hover:bg-slate-50 border border-slate-300` | Edit, Reject, Filter actions |

### Dark Theme (Toggleable)

| Role | Hex | Tailwind Token |
| :--- | :--- | :--- |
| **Canvas** | `#090D16` | `dark:bg-slate-950` |
| **Surface** | `#0F172A` | `dark:bg-slate-900` |
| **Sidebar** | `#090D16` | `dark:bg-slate-950` |
| **Border** | `#1E293B` | `dark:border-slate-800` |
| **Text Primary** | `#F8FAFC` | `dark:text-slate-100` |
| **Text Secondary** | `#94A3B8` | `dark:text-slate-400` |

---

## 3. Typography & Hierarchy Scale

- **Primary Typeface:** `Inter`, `-apple-system`, `BlinkMacSystemFont`, `"Segoe UI"`, `sans-serif`. Tabular figures enabled (`font-variant-numeric: tabular-nums;`) for all numerical counts, prices, and timestamps.
- **Code & SKU Typeface:** `JetBrains Mono`, `monospace` (SKUs, IDs, SQL queries only).
- **Type Scale:**
  - `Display / KPI`: 24px (1.5rem), font-semibold, tracking-tight
  - `Title (H1)`: 18px (1.125rem), font-semibold, tracking-tight
  - `Section (H2)`: 15px (0.9375rem), font-semibold
  - `Body / Composer`: 14px (0.875rem), font-normal, line-height 1.6
  - `Caption / Meta`: 12px-13px (0.75rem - 0.8125rem), font-normal / font-medium
  - `Micro Tag`: 11px (0.6875rem), font-medium

---

## 4. Layout Architecture (Three-Pane Inbox)

```
+-----------------------------------------------------------------------------------------------------------------------+
|  [Logo] Trentar OpsPilot  |  Live AI  |  3 pending drafts  |  Settings                                                 |
+-----------------------------------------------------------------------------------------------------------------------+
| Sidebar (200px) | Message List (360px)   | Conversation & Draft Composer (Flex)     | Context Inspector (320px)       |
|                 |                        |                                          |                                 |
| - Inbox (3)     | [Search...]            | RE: Quotation for TRN-FC-PRO             | Customer Profile                |
| - Supplier Orders| [All / Unread / Short] | Vikram Patel <vikram@aerospacelabs.in>   | AeroSpace Labs India (Bangalore)|
| - Ask AI        | ---------------------- | ---------------------------------------- |                                 |
| - Forecast      | • Vikram Patel         | Customer Message:                        | Inventory Reality Check         |
| - Activity Log  |   Quote for TRN-FC-PRO | "Need quotation for 5 units..."          | TRN-FC-PRO Flight Controller    |
| - Settings      |   12 min ago  [Quote]  | ---------------------------------------- | In-Hand: 14 units (Sufficient)  |
|                 | • Sneha Reddy          | AI Drafted Reply:                        | Unit Price: ₹34,000             |
|                 |   Bulk 8318 Motors     | [Subject: Quotation & Availability...]   | Reorder Point: 8                |
|                 |   25 min ago [Shortfall]| "Dear Vikram, We confirm 14 units..."   |                                 |
|                 |                        | ---------------------------------------- | Linked Supplier PO              |
|                 |                        | [Approve & send]  [Edit]  [Reject]       | None required (In stock)        |
+-----------------------------------------------------------------------------------------------------------------------+
```

---

## 5. Component Patterns

### 5.1 Inbox List Item (`MessageCard`)
- Left unread indicator dot (`w-2 h-2 rounded-full bg-blue-600` if pending).
- Avatar circle with two initials (`VP`, `SR`) in quiet slate `#E2E8F0`.
- Bold sender name + subtle relative time (`14 min ago`).
- Subject line with 1-line message excerpt.
- Single quiet pill for intent (e.g. `Quote`, `Bulk order`, `Inquiry`, `Complaint`).

### 5.2 Email Composer & Hero Draft Card (`DraftReviewCard`)
- Structured like a modern email client (Front / Superhuman / Outlook Web).
- Header: To recipient, Subject line, Customer company.
- Top section: The original customer message in a clean, indented quotation block.
- Summary bar: Clean horizontal pill row showing Detected Intent, Matched Product, In-hand Stock vs Requested, and Price.
- Draft body: Clean white card, generous line height (1.6), clear paragraph spacing, real customer name and real sign-off.
- Footer action bar:
  - **Hero CTA:** `Approve & send` (Primary Ink Blue, right-aligned with checkmark icon, shortcut hint `Alt+A`).
  - **Secondary Actions:** `Edit` (opens clean textarea), `Reject` (muted outline button).
  - Quiet footer note: `AI-drafted using verified catalog data • Auto-approval in 42s` (calm font, amber/red text only when < 20s).

### 5.3 Data Tables (`StockOrders`, `AuditLog`, `Analytics`)
- Sticky table header (`bg-slate-50 text-slate-500 font-medium text-xs border-b`).
- Zebra-free, clean row hover (`hover:bg-slate-50/80`).
- Numerical columns right-aligned with tabular figures.
- Explicit visual badges with soft backgrounds and matching borders (no stark high-contrast neon).
