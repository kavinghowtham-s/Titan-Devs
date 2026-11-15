# OmniBix AI
### Intelligent Business Operations Platform for SMEs

<p align="center">
  <strong>One Intelligence. Every Business Operation.</strong>
</p>

<p align="center">
  Developed by <strong>Team Titan Devs</strong> | Chennai Institute of Technology
</p>

---

##  About the Project

**OmniBix AI** is an AI-powered business operations and management platform designed to help Small and Medium-sized Enterprises (SMEs) improve operational efficiency, automate repetitive tasks, and make smarter business decisions.

Many manufacturing SMEs still depend on manual processes for inventory management, customer communication, procurement, and daily business operations. These traditional approaches often result in delayed responses, inefficient workflows, increased employee workload, and reduced productivity.

OmniBix AI aims to address these challenges by bringing business intelligence, AI-powered assistants, operational monitoring, procurement intelligence, and workflow automation together in one unified platform.

Our vision is to transform traditional business management into a more intelligent, connected, and proactive experience.

## Problem Statement

**PS#601 – Improve Business Operations and Customer Response Speed Through Digitization and AI**

Proposed by **Trentar Private Limited**.

Many small and medium-scale industries rely on manual processes for business operations, communication, and customer support, resulting in delays and reduced productivity.

The challenge is to develop a practical digitalization and AI-based solution that:

- Automates routine business activities.
- Improves operational efficiency.
- Enables faster customer query resolution.
- Reduces repetitive manual work.
- Enhances overall customer satisfaction.

## Our Solution

OmniBix AI acts as an intelligent business copilot that connects different business operations and helps organizations move from reactive management to proactive decision-making.

Instead of functioning as just another chatbot, OmniBix AI combines specialized AI assistants, business monitoring, procurement recommendations, financial insights, and human-approved automation.

## Key Features

### 1. Business Pulse – Proactive Business Intelligence

- Monitors business operations and identifies potential issues.
- Detects critical inventory shortages.
- Highlights delayed orders and pending enquiries.
- Classifies alerts based on severity.
- Provides actionable recommendations.

### 2. Voice-First Regional Language Copilot

- Enables natural communication through voice and text.
- Designed for Tamil, Hindi, Hinglish, and other regional languages.
- Uses AI to understand unstructured messages.
- Extracts useful business information from worker reports.
- Helps record stock shortages, machine downtime, and operational issues.

### 3. Smart RFQ & Intelligent Procurement

- Identifies procurement requirements.
- Generates Request for Quotation (RFQ) drafts.
- Compares multiple suppliers.
- Evaluates price, delivery time, and supplier reliability.
- Recommends suitable suppliers.
- Generates draft Purchase Orders for manager approval.

### 4. Cash Flow Impact Simulator

- Estimates the financial impact of operational delays.
- Calculates blocked customer billings.
- Tracks work-in-progress inventory value.
- Supports what-if financial analysis.
- Helps managers understand the financial implications of delayed production.

### 5. AI Workforce – Specialized AI Assistants

OmniBix AI is designed around five specialized AI assistants:

| AI Assistant | Responsibility |
|---|---|
| Customer Support AI | Customer enquiries and response drafting |
| Operations AI | Production and workflow assistance |
| Procurement AI | Supplier comparisons and purchasing |
| Inventory AI | Stock monitoring and shortage detection |
| Analytics AI | Business insights and financial analysis |

These assistants are designed to work with shared business information through a centralized Business Memory.

### 6. Business Memory

- Centralized business information.
- Customer and supplier records.
- Inventory and order information.
- Enquiry and operational history.
- Context sharing across specialized AI assistants.

### 7. Manager Approval System

- Generates draft business actions.
- Allows managers to review recommendations.
- Supports purchase order approval and rejection.
- Maintains decision history and accountability.

### 8. Digital Dashboard & Analytics

- Business KPI monitoring.
- Inventory and procurement status.
- Customer enquiry tracking.
- Operational alerts.
- Business performance insights.

## System Architecture

OmniBix AI follows a frontend-backend architecture.

```text
             BUSINESS USERS
                   |
                   v
          FRONTEND INTERFACE
          HTML / CSS / JavaScript
                   |
                   v
             FASTAPI BACKEND
                   |
          +--------+--------+
          |                 |
          v                 v
     SQLITE DATABASE    GEMINI API
          |                 |
          v                 v
    BUSINESS DATA      AI PROCESSING
          |                 |
          +--------+--------+
                   |
                   v
          BUSINESS INTELLIGENCE
                   |
                   v
        AUTOMATED RECOMMENDATIONS
          AND MANAGER APPROVAL
```

## Technology Stack

| Component | Technology |
|---|---|
| Frontend | HTML, CSS, JavaScript |
| UI Styling | Tailwind CSS |
| Data Visualization | Chart.js |
| Backend | Python, FastAPI |
| Database | SQLite |
| AI Integration | Google Gemini API |
| API Communication | REST APIs |
| Version Control | Git and GitHub |

*The technology list describes the project stack and intended integrations. Refer to the actual implementation and configuration for the components currently operational.*

## Project Structure

```text
Titan-Devs/
│
├── frontend/
│   ├── index.html
│   ├── assets/
│   └── ...
│
├── backend/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── gemini.py
│   └── ...
│
├── docs/
│   └── ...
│
├── scripts/
│   └── ...
│
├── .gitignore
└── README.md
```

*The structure above is illustrative. Refer to the repository for the actual filenames and folders.*

## Getting Started

### Prerequisites

Before running the project, install:

- Python 3.10 or later.
- Git.
- Visual Studio Code or another code editor.
- A Google Gemini API key if Gemini integration is enabled.

### 1. Clone the Repository

```bash
git clone https://github.com/kavinghowtham-s/Titan-Devs.git
```

Navigate into the project:

```bash
cd Titan-Devs
```

### 2. Set Up the Backend

Navigate to the backend directory:

```bash
cd backend
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file inside the backend directory.

Add your Gemini API key:

```env
GEMINI_API_KEY=your_gemini_api_key
```

**Important:** Never upload your API key or `.env` file to GitHub.

### 4. Start the Backend

If the FastAPI entry point is `main.py`:

```bash
uvicorn main:app --reload
```

The backend will be available at:

```text
http://127.0.0.1:8000
```

FastAPI interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

### 5. Run the Frontend

Open the frontend directory and launch the application using a local development server.

For example:

```bash
python -m http.server 5500
```

Open:

```text
http://localhost:5500
```

*Adjust the commands if your actual entry point, dependency file, or frontend setup differs.*

## Example Use Case

**Scenario: Inventory Shortage in a Manufacturing Unit**

1. A shop-floor worker reports an electric motor shortage through a regional-language message.
2. The Voice Copilot interprets the message.
3. Relevant inventory information is extracted and recorded.
4. Business Pulse identifies the shortage.
5. Smart Procurement compares available suppliers.
6. The Cash Flow Simulator estimates the financial impact of production delays.
7. The AI Workforce provides recommendations.
8. A manager reviews and approves the proposed purchase order.
9. The decision is recorded for future reference.

This workflow demonstrates how different business operations can work together through a unified AI-powered platform.

## Innovation & Differentiation

What makes OmniBix AI different is its integrated approach to business automation.

- **Proactive Intelligence:** Identifies business problems instead of waiting for manual reports.
- **Regional Language Accessibility:** Makes AI-powered business tools more accessible to shop-floor workers.
- **Specialized AI Workforce:** Uses multiple role-specific assistants instead of relying on a single general-purpose chatbot.
- **Intelligent Procurement:** Considers supplier reliability and delivery time alongside pricing.
- **Financial Awareness:** Helps managers understand the potential financial impact of operational delays.
- **Human-in-the-Loop Automation:** Keeps managers involved in important business decisions.

## Future Scope

Potential future enhancements include:

- Full WhatsApp Business API integration.
- Advanced demand forecasting.
- Predictive maintenance.
- Real-time inventory integration.
- Advanced financial forecasting.
- Additional regional languages.
- Multi-branch business management.
- Role-based access control.
- Advanced analytics and reporting.

## Team Titan Devs

**Institution:** Chennai Institute of Technology

| Team Member | Role |
|---|---|
| Sanjay Kumar | Team Lead / AI Architecture |
| S Kavin Ghowtham | Backend Pipelines |
| P S Rahul Gowtham | UI/UX & Business |
| G M Mukesh | Data Analytics & QA |

## Hackathon

**Event:** INDUSTRIX'26 – INDUSTRIX IBH  
**Organized by:** ASME  
**Venue:** B. S. Abdur Rahman Crescent Institute of Science and Technology  
**Problem Statement Organization:** Trentar Private Limited

## Repository

GitHub: https://github.com/kavinghowtham-s/Titan-Devs

---

<p align="center">
  <strong>OmniBix AI – One Intelligence. Every Business Operation.</strong>
  <br>
  Built with innovation by Team Titan Devs 
</p>
