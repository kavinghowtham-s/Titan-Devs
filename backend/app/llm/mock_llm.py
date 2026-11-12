import re
from typing import Type, Any, Dict, Optional, List
from pydantic import BaseModel
from backend.app.config import settings
from backend.app.schemas.message_dto import IntakeClassificationResult, ExtractedRequirement
from backend.app.schemas.draft_dto import DrafterResponse, OrchestratorSafetyEvaluation, SafetyRuleCheck
from backend.app.schemas.assistant_dto import SQLAssistantResult
from backend.app.schemas.analytics_dto import ExecutiveBriefingReport, ExecutiveInsight

class MockLLMRegistry:
    """Deterministic, template-driven mock engine keyed on intent + real DB facts."""

    @classmethod
    def resolve(cls, role_model: str, user_prompt: str, response_schema: Type[BaseModel]) -> BaseModel:
        lower_prompt = user_prompt.lower()

        # 1. INTAKE CLASSIFIER AGENT
        if response_schema == IntakeClassificationResult:
            return cls._resolve_intake(user_prompt, lower_prompt)

        # 2. DRAFTER AGENT
        elif response_schema == DrafterResponse:
            return cls._resolve_drafter(user_prompt, lower_prompt)

        # 3. SAFETY ORCHESTRATOR AGENT
        elif response_schema == OrchestratorSafetyEvaluation:
            return cls._resolve_orchestrator(user_prompt, lower_prompt)

        # 4. SQL ASSISTANT AGENT
        elif response_schema == SQLAssistantResult:
            return cls._resolve_sql(user_prompt, lower_prompt)

        # 5. EXECUTIVE INSIGHTS AGENT
        elif response_schema == ExecutiveBriefingReport:
            return cls._resolve_insights(user_prompt, lower_prompt)

        return response_schema()

    @classmethod
    def _resolve_intake(cls, text: str, lower: str) -> IntakeClassificationResult:
        # Prompt injection detection
        if any(term in lower for term in ["system override", "ignore all", "ignore previous", "drop table", "reveal sqlite", "admin token"]):
            return IntakeClassificationResult(
                language="en",
                detected_intent="general",
                sentiment="neutral",
                priority="urgent",
                requirements=[],
                is_prompt_injection=True,
                confidence=0.99
            )

        # Language detection
        lang = "en"
        if any('\u0b80' <= c <= '\u0bff' for c in text):
            lang = "ta"
        elif any('\u0900' <= c <= '\u097f' for c in text):
            lang = "hi"

        # Complaint / Refund detection
        if any(w in lower for w in ["cracked", "damaged", "broken", "disappointed", "complaint", "defect", "गलत", "रिफंड", "பாதிக்க"]):
            intent = "refund" if any(w in lower for w in ["refund", "रिफंड", "பணம்"]) else "complaint"
            return IntakeClassificationResult(
                language=lang,
                detected_intent=intent,
                sentiment="frustrated",
                priority="urgent",
                requirements=[],
                is_prompt_injection=False,
                confidence=0.97
            )

        # M01: Price quote for TRN-FC-PRO (5 units) and TRN-PROP-3010 (10 pairs)
        if "trn-fc-pro" in lower or "flight controller" in lower:
            return IntakeClassificationResult(
                language=lang,
                detected_intent="price_quote",
                sentiment="neutral",
                priority="medium",
                requirements=[
                    ExtractedRequirement(sku="TRN-FC-PRO", product_name_raw="Triple-Redundant Flight Controller", quantity=5),
                    ExtractedRequirement(sku="TRN-PROP-3010", product_name_raw="30x10.5 Folding Carbon Propeller Pair", quantity=10)
                ],
                is_prompt_injection=False,
                confidence=0.98
            )

        # M02: Bulk order for TRN-MOT-8318 (25 units)
        if "8318" in lower or "motor" in lower:
            qty_match = re.search(r'(\d+)\s*(?:units|sets|pieces|pcs|மோட்டார்|पीस)', text, re.IGNORECASE)
            qty = int(qty_match.group(1)) if qty_match else 25
            return IntakeClassificationResult(
                language=lang,
                detected_intent="bulk_order",
                sentiment="neutral",
                priority="high",
                requirements=[ExtractedRequirement(sku="TRN-MOT-8318", product_name_raw="8318 Heavy-Lift Industrial Motor", quantity=qty)],
                is_prompt_injection=False,
                confidence=0.95
            )

        # M04: Hindi bulk order for TRN-BAT-6S22A (20 units)
        if "6s22a" in lower or "battery" in lower or "बैटरी" in lower:
            qty_match = re.search(r'(\d+)\s*(?:units|sets|pieces|pcs|पैक)', text, re.IGNORECASE)
            qty = int(qty_match.group(1)) if qty_match else 20
            return IntakeClassificationResult(
                language=lang,
                detected_intent="bulk_order",
                sentiment="neutral",
                priority="high",
                requirements=[ExtractedRequirement(sku="TRN-BAT-6S22A", product_name_raw="Solid-State LiPo Pack", quantity=qty)],
                is_prompt_injection=False,
                confidence=0.94
            )

        # M03: Tamil stock inquiry for TRN-FRM-HEX (6 sets)
        if "trn-frm-hex" in lower or "1200mm" in lower or "hexacopter" in lower or "பிரேம்" in lower:
            return IntakeClassificationResult(
                language=lang,
                detected_intent="stock_inquiry",
                sentiment="neutral",
                priority="medium",
                requirements=[ExtractedRequirement(sku="TRN-FRM-HEX", product_name_raw="Hexacopter Carbon Frame Kit", quantity=6)],
                is_prompt_injection=False,
                confidence=0.96
            )

        # M05: Order status / tracking
        if any(w in lower for w in ["tracking", "po-4091", "shipped", "status"]):
            return IntakeClassificationResult(
                language=lang,
                detected_intent="order_status",
                sentiment="positive",
                priority="low",
                requirements=[],
                is_prompt_injection=False,
                confidence=0.96
            )

        # Default fallback
        return IntakeClassificationResult(
            language=lang,
            detected_intent="general",
            sentiment="neutral",
            priority="medium",
            requirements=[],
            is_prompt_injection=False,
            confidence=0.90
        )

    @classmethod
    def _resolve_drafter(cls, text: str, lower: str) -> DrafterResponse:
        # Extract customer name from user prompt
        name_match = re.search(r"Customer Name:\s*([^\n]+)", text)
        cust_name = name_match.group(1).strip() if name_match else "Client"
        if not cust_name or cust_name.lower() in ["none", "customer"]:
            cust_name = "Client"

        sign_off = f"Best regards,\n{settings.SENDER_NAME}\n{settings.SENDER_TITLE}, {settings.SENDER_COMPANY}"

        # 1. TAMIL TEMPLATES (e.g. M03 Hexacopter)
        if any('\u0b80' <= c <= '\u0bff' for c in text):
            if "பிரேம்" in text or "trn-frm-hex" in lower or "1200mm" in lower:
                return DrafterResponse(
                    subject="டிரெண்டார்: TRN-FRM-HEX இருப்பு மற்றும் விலை விவரம்",
                    body=(
                        f"வணக்கம் {cust_name},\n\n"
                        "டிரெண்டார் பிரைவேட் லிமிடெட்டைத் தொடர்புகொண்டதற்கு நன்றி.\n\n"
                        "நீங்கள் கேட்ட TRN-FRM-HEX 1200mm Hexacopter Frame எங்கள் கிடங்கில் தற்போது 4 செட் உடனடியாக அனுப்பும் நிலையில் உள்ளது. "
                        "தங்களின் தேவை 6 செட்கள் என்பதால், மீதமுள்ள 2 செட்கள் புதிய தொகுப்பில் இருந்து 7 வேலை நாட்களில் டெலிவரி செய்யப்படும்.\n\n"
                        "விலை விவரம்:\n"
                        "- ஒரு செட்டின் யூனிட் விலை: ரூ. 42,000 (GST கூடுதல்)\n"
                        "- கிடைக்கும் இருப்பு: 4 செட்கள் (உடனடி டிஸ்பாட்ச்)\n\n"
                        "ஆர்டரை உறுதிப்படுத்த proforma invoice தயார் செய்யலாமா என்பதைத் தெரிவிக்கவும்.\n\n"
                        f"அன்புடன்,\n{settings.SENDER_NAME}\n{settings.SENDER_TITLE}, {settings.SENDER_COMPANY}"
                    ),
                    estimated_delivery_days=7,
                    discount_offered_pct=0.0,
                    requires_manager_special_attention=False
                )
            else:
                return DrafterResponse(
                    subject="டிரெண்டார் பிரைவேட் லிமிடெட் - உங்களின் கோரிக்கை விவரம்",
                    body=(
                        f"வணக்கம் {cust_name},\n\n"
                        "தங்களின் தொடர்புக்கு நன்றி. உங்கள் கோரிக்கையை எங்கள் உற்பத்தி மற்றும் இருப்புப் பிரிவினர் சரிபார்த்துள்ளனர். "
                        "எங்கள் சென்னை உற்பத்தி மையத்தில் தரமான உதிரிபாகங்கள் தயார் நிலையில் உள்ளன.\n\n"
                        f"அன்புடன்,\n{settings.SENDER_NAME}\n{settings.SENDER_TITLE}, {settings.SENDER_COMPANY}"
                    ),
                    estimated_delivery_days=3,
                    discount_offered_pct=0.0,
                    requires_manager_special_attention=False
                )

        # 2. HINDI TEMPLATES (e.g. M04 Battery Pack or M08 Refund)
        if any('\u0900' <= c <= '\u097f' for c in text):
            if "बैटरी" in text or "6s22a" in lower or "battery" in lower:
                return DrafterResponse(
                    subject="TRN-BAT-6S22A बैटरी पैक कोटेशन एवं स्टॉक स्थिति - ट्रेंटार",
                    body=(
                        f"नमस्ते {cust_name} जी,\n\n"
                        "ट्रेंटार प्राइवेट लिमिटेड से संपर्क करने के लिए धन्यवाद।\n\n"
                        "आपके 20 बैटरी पैक TRN-BAT-6S22A के ऑर्डर के संदर्भ में स्टॉक स्थिति निम्नलिखित है:\n"
                        "- हमारे वेयरहाउस में तत्काल उपलब्ध स्टॉक: 6 यूनिट्स (तुरंत प्रेषण)\n"
                        "- यूनिट मूल्य: ₹26,500 प्रति पैक (GST अतिरिक्त)\n"
                        "- शेष 14 यूनिट्स के लिए सप्लायर से नया बैच 18 दिनों में उपलब्ध होगा।\n\n"
                        "कृपया पुष्टि करें कि क्या आप 6 यूनिट्स का प्रारंभिक शिपमेंट तुरंत स्वीकार करना चाहेंगे?\n\n"
                        f"सादर,\n{settings.SENDER_NAME}\n{settings.SENDER_TITLE}, {settings.SENDER_COMPANY}"
                    ),
                    estimated_delivery_days=18,
                    discount_offered_pct=0.0,
                    requires_manager_special_attention=True
                )
            elif "गलत" in text or "रिफंड" in text:
                return DrafterResponse(
                    subject="असुविधा के लिए खेद: पार्ट प्रतिस्थापन एवं समाधान - ट्रेंटार",
                    body=(
                        f"नमस्ते {cust_name} जी,\n\n"
                        "गलत प्रोपेलर साइज मिलने के कारण आपको हुई असुविधा के लिए हम क्षमाप्रार्थी हैं।\n\n"
                        "हमने सही पार्ट (TRN-PROP-3010) का तत्काल डिस्पैच प्रोसेस कर दिया है। "
                        "गलत पार्सल की वापसी के लिए हमारी लॉजिस्टिक्स टीम आज आपसे संपर्क करेगी।\n\n"
                        f"सादर,\n{settings.SENDER_NAME}\n{settings.SENDER_TITLE}, {settings.SENDER_COMPANY}"
                    ),
                    estimated_delivery_days=2,
                    discount_offered_pct=0.0,
                    requires_manager_special_attention=True
                )

        # 3. ENGLISH COMPLAINT / DEFECT (e.g. M06)
        if any(w in lower for w in ["cracked", "damaged", "broken", "complaint"]):
            return DrafterResponse(
                subject=f"Urgent: Replacement Processing for TRN-SEN-RTK - Trentar Operations",
                body=(
                    f"Dear {cust_name},\n\n"
                    "We sincerely apologize for the damaged connector pin on your recently delivered TRN-SEN-RTK module. "
                    "Quality and operational readiness are our highest priorities at Trentar.\n\n"
                    "We have initiated an immediate warranty replacement from our verified stock buffer. "
                    "A new tested unit will be dispatched via priority express courier today, and tracking details will follow within 2 hours. "
                    "A return airway bill has also been generated for the defective unit.\n\n"
                    f"{sign_off}"
                ),
                estimated_delivery_days=1,
                discount_offered_pct=0.0,
                requires_manager_special_attention=True
            )

        # 4. ENGLISH SPECIFIC PRICE QUOTE FOR TRN-FC-PRO (e.g. M01 Vikram Patel)
        if "trn-fc-pro" in lower or "flight controller" in lower or "5 units" in lower:
            return DrafterResponse(
                subject="Quotation & Availability: TRN-FC-PRO Flight Controllers - Trentar Pvt Ltd",
                body=(
                    f"Dear {cust_name},\n\n"
                    "Thank you for contacting Trentar Private Limited regarding your requirement for flight controller units.\n\n"
                    "We are pleased to confirm that we have 14 units of TRN-FC-PRO in stock, which fully covers your requirement of 5 units. "
                    "We also have 18 pairs of TRN-PROP-3010 carbon propellers available for immediate dispatch.\n\n"
                    "Quotation Details:\n"
                    "- TRN-FC-PRO Triple-Redundant Flight Controller: ₹34,000 per unit (5 units = ₹1,70,000)\n"
                    "- TRN-PROP-3010 30x10.5 Folding Carbon Propeller Pair: ₹4,500 per pair (10 pairs = ₹45,000)\n"
                    "- Total Commercial Value: ₹2,15,000 (exclusive of applicable GST)\n"
                    "- Delivery Timeline to Bangalore: 2 business days via road express upon purchase order receipt.\n\n"
                    "Please let us know if you would like us to generate the formal Proforma Invoice.\n\n"
                    f"{sign_off}"
                ),
                estimated_delivery_days=2,
                discount_offered_pct=0.0,
                requires_manager_special_attention=False
            )

        # 5. ENGLISH BULK ORDER WITH SHORTFALL (e.g. M02 Sneha Reddy)
        if "8318" in lower or "deccan" in lower or "25 units" in lower:
            return DrafterResponse(
                subject="Quotation & Delivery Timeline: TRN-MOT-8318 Motors - Trentar Pvt Ltd",
                body=(
                    f"Dear {cust_name},\n\n"
                    "Thank you for reaching out to Trentar Private Limited regarding your requirement of 25 units of TRN-MOT-8318 Heavy-Lift Industrial Motors.\n\n"
                    "We can immediately dispatch 8 units currently available in our warehouse today. "
                    "For the remaining 17 units, we have initiated an express procurement order with our drive supplier, "
                    "with guaranteed dispatch within 10 business days.\n\n"
                    "Commercial Pricing:\n"
                    "- Unit Price: ₹14,500 (exclusive of GST)\n"
                    "- Total Order Value: ₹3,62,500 + GST\n\n"
                    "Please confirm if you would like us to process the split dispatch so you can begin initial integration right away.\n\n"
                    f"{sign_off}"
                ),
                estimated_delivery_days=10,
                discount_offered_pct=0.0,
                requires_manager_special_attention=True
            )

        # 6. ROUTINE ORDER STATUS (e.g. M05 Arvind Swamy)
        if "po-4091" in lower or "tracking" in lower or "shipped" in lower:
            return DrafterResponse(
                subject=f"Shipment Tracking Details for PO-4091 - Trentar Pvt Ltd",
                body=(
                    f"Dear {cust_name},\n\n"
                    "Thank you for checking in on the status of PO-4091.\n\n"
                    "Your consignment was dispatched via Blue Dart Express under Airway Bill #BD-TRN-8849102 on Tuesday. "
                    "Current transit tracking indicates scheduled arrival at your Chennai survey facility by tomorrow at 2:00 PM.\n\n"
                    f"{sign_off}"
                ),
                estimated_delivery_days=1,
                discount_offered_pct=0.0,
                requires_manager_special_attention=False
            )

        # 7. GENERAL BUSINESS INQUIRY
        return DrafterResponse(
            subject=f"Response to Your Inquiry - Trentar Private Limited",
            body=(
                f"Dear {cust_name},\n\n"
                "Thank you for contacting Trentar Private Limited. We have received your inquiry and matched it with our technical catalog.\n\n"
                "Our team is available to assist with component specifications, pricing tiers, and delivery schedules. "
                "Please let us know if you require technical data-sheets or commercial proforma invoices.\n\n"
                f"{sign_off}"
            ),
            estimated_delivery_days=3,
            discount_offered_pct=0.0,
            requires_manager_special_attention=False
        )

    @classmethod
    def _resolve_orchestrator(cls, text: str, lower: str) -> OrchestratorSafetyEvaluation:
        # Negative / Complaint / Refund / Injection -> FAIL & ESCALATE
        if any(w in lower for w in ["cracked", "damaged", "complaint", "defect", "angry", "frustrated", "refund", "system override", "injection"]):
            return OrchestratorSafetyEvaluation(
                verdict="FAIL",
                safety_score=0.20,
                rule_checks=[
                    SafetyRuleCheck(rule_name="sentiment_neutral_or_positive", passed=False, reason="Customer expressed dissatisfaction / hardware defect"),
                    SafetyRuleCheck(rule_name="no_unauthorized_discount", passed=True, reason="No pricing concession offered"),
                    SafetyRuleCheck(rule_name="no_legal_or_complaint_risk", passed=False, reason="Hardware replacement dispute requires human manager verification")
                ],
                escalation_reason="High-risk customer defect complaint requires manual manager review before sending.",
                recommended_action="escalate_to_manager"
            )

        # Routine Quote / Status -> PASS
        return OrchestratorSafetyEvaluation(
            verdict="PASS",
            safety_score=0.98,
            rule_checks=[
                SafetyRuleCheck(rule_name="sentiment_neutral_or_positive", passed=True, reason="Professional, polite tone"),
                SafetyRuleCheck(rule_name="no_unauthorized_discount", passed=True, reason="Standard catalog pricing adhered to"),
                SafetyRuleCheck(rule_name="no_legal_or_complaint_risk", passed=True, reason="Routine operational information response")
            ],
            escalation_reason=None,
            recommended_action="auto_approve_and_send"
        )

    @classmethod
    def _resolve_sql(cls, text: str, lower: str) -> SQLAssistantResult:
        # Extract the actual employee question from the prompt
        if "Employee Question:" in text:
            raw_q = text.split("Employee Question:")[-1].strip()
        elif "employee question:" in lower:
            idx = lower.find("employee question:")
            raw_q = text[idx + len("employee question:"):].strip()
        else:
            raw_q = text.strip()

        q_lower = raw_q.lower().strip()
        q_clean = q_lower.strip("?!., \t\r\n")

        # 1. Greetings & Conversational Questions
        greetings = {"hey", "hi", "hello", "good morning", "good evening", "good afternoon", "help", "who are you", "what can you do", "yo", "sup", "hey there", "test"}
        if q_clean in greetings or any(q_clean.startswith(g) for g in ["hey ", "hello ", "hi ", "help "]):
            return SQLAssistantResult(
                sql_query="SELECT count(*) AS total_skus, sum(current_stock) AS total_inventory_units FROM products;",
                explanation_en="System introduction and active catalog overview.",
                natural_response="Hello! I am Trentar's OpsPilot AI Assistant. I can query our warehouse inventory, sales records, customer accounts, and supplier purchase orders in English, Tamil, or Hindi. Try asking: 'Show our suppliers and lead times', 'What is our total revenue?', 'Show low stock products', or 'Which products are top sellers?'."
            )

        # 2. Tamil Language Queries (தமிழ்)
        if any('\u0b80' <= c <= '\u0bff' for c in raw_q):
            if any(k in raw_q for k in ["விற்பனை", "அதிகமான", "டாப்"]):
                return SQLAssistantResult(
                    sql_query="SELECT p.sku, p.name, sum(s.quantity_sold) AS total_sold, round(sum(s.total_revenue), 2) AS total_revenue FROM sales_history s JOIN products p ON s.product_id = p.id GROUP BY p.id ORDER BY total_sold DESC LIMIT 5;",
                    explanation_en="Aggregates sales volume per product and retrieves the top items.",
                    natural_response="கடந்த காலத்தில் அதிக விற்பனையான பொருள் 'High-Torque 4014 BLDC Motor' (SKU: TRN-MOT-4014) ஆகும். மொத்தம் 163 யூனிட்கள் விற்பனை செய்யப்பட்டு, ரூ. 21,98,870 வருவாய் ஈட்டப்பட்டுள்ளது."
                )
            if any(k in raw_q for k in ["ஸ்டாக்", "குறைந்த", "இருப்பு"]):
                return SQLAssistantResult(
                    sql_query="SELECT sku, name, current_stock, min_reorder_level FROM products WHERE current_stock <= min_reorder_level ORDER BY current_stock ASC LIMIT 10;",
                    explanation_en="Filters products table for items where current stock is below reorder level.",
                    natural_response="கிடங்கில் 9 தயாரிப்புகள் குறைந்த இருப்பில் உள்ளன: TRN-CAM-4KTH (2 யூனிட்கள்), TRN-FRM-VTOL (3 யூனிட்கள்), TRN-FRM-HEX (4 யூனிட்கள்), மற்றும் TRN-SEN-RTK (5 யூனிட்கள்)."
                )
            if any(k in raw_q for k in ["சப்ளையர்", "வழங்குநர்", "பார்ட்னர்"]):
                return SQLAssistantResult(
                    sql_query="SELECT name, category, default_lead_time_days FROM suppliers ORDER BY default_lead_time_days ASC;",
                    explanation_en="Lists registered suppliers in Tamil.",
                    natural_response="நமது பதிவு செய்யப்பட்ட சப்ளையர்கள்: Bharat Micro Fasteners (5 நாட்கள்), Kavach Dynamic Drives (10 நாட்கள்), Garuda Composites (14 நாட்கள்), Shakti Energy (18 நாட்கள்), NaviX Avionics (21 நாட்கள்)."
                )
            return SQLAssistantResult(
                sql_query="SELECT count(*) AS total_skus, sum(current_stock) AS total_inventory_units FROM products;",
                explanation_en="General Tamil assistant response.",
                natural_response="வணக்கம்! நான் ட்ரென்டார் நிறுவனத்தின் OpsPilot AI உதவியாளர். சரக்கு இருப்பு, விற்பனை விவரங்கள் அல்லது சப்ளையர்கள் பற்றிய தகவல்களை என்னிடம் கேட்கலாம்."
            )

        # 3. Hindi Language Queries (हिंदी)
        if any('\u0900' <= c <= '\u097f' for c in raw_q):
            if any(k in raw_q for k in ["स्टॉक", "कमी", "कम"]):
                return SQLAssistantResult(
                    sql_query="SELECT sku, name, current_stock, min_reorder_level FROM products WHERE current_stock <= min_reorder_level ORDER BY current_stock ASC LIMIT 10;",
                    explanation_en="Filters products table for items where current stock is below reorder level.",
                    natural_response="वेयरहाउस में 9 उत्पादों का स्टॉक न्यूनतम स्तर से कम है: TRN-CAM-4KTH (2 पीस), TRN-FRM-VTOL (3 पीस), TRN-FRM-HEX (4 पीस), और TRN-SEN-RTK (5 पीस)।"
                )
            if any(k in raw_q for k in ["बिक्री", "सबसे ज्यादा", "टॉप"]):
                return SQLAssistantResult(
                    sql_query="SELECT p.sku, p.name, sum(s.quantity_sold) AS total_sold, round(sum(s.total_revenue), 2) AS total_revenue FROM sales_history s JOIN products p ON s.product_id = p.id GROUP BY p.id ORDER BY total_sold DESC LIMIT 5;",
                    explanation_en="Aggregates sales volume per product and retrieves the top items.",
                    natural_response="सबसे अधिक बिकने वाला उत्पाद 'High-Torque 4014 BLDC Motor' (SKU: TRN-MOT-4014) है, जिसकी कुल 163 यूनिट्स बिकी हैं और ₹21,98,870 का राजस्व प्राप्त हुआ है।"
                )
            if any(k in raw_q for k in ["सप्लायर", "आपूर्तिकर्ता"]):
                return SQLAssistantResult(
                    sql_query="SELECT name, category, default_lead_time_days FROM suppliers ORDER BY default_lead_time_days ASC;",
                    explanation_en="Lists registered suppliers in Hindi.",
                    natural_response="हमारे 5 पंजीकृत सप्लायर्स हैं: भारत माइक्रो फास्टनर्स (5 दिन), कवच डायनेमिक ड्राइव्स (10 दिन), गरुड़ कंपोजिट्स (14 दिन), और शक्ति एनर्जी सॉल्यूशंस (18 दिन)।"
                )
            return SQLAssistantResult(
                sql_query="SELECT count(*) AS total_skus, sum(current_stock) AS total_inventory_units FROM products;",
                explanation_en="General Hindi assistant response.",
                natural_response="नमस्ते! मैं ट्रेंटार का OpsPilot AI सहायक हूँ। आप वेयरहाउस स्टॉक, बिक्री डेटा या सप्लायर लीड टाइम के बारे में मुझसे पूछ सकते हैं।"
            )

        # 4. Suppliers & Procurement Lead Times (English)
        if any(w in q_lower for w in ["supplier", "vendor", "lead time", "who supplies", "procurement source"]):
            return SQLAssistantResult(
                sql_query="SELECT id, name, category, default_lead_time_days FROM suppliers ORDER BY default_lead_time_days ASC;",
                explanation_en="Lists all registered suppliers, their component categories, and fulfillment lead times.",
                natural_response="Trentar has 5 registered suppliers: Bharat Micro Fasteners & CNC (5 days lead time), Kavach Dynamic Drives (10 days), Garuda Composites (14 days), Shakti Energy Solutions (18 days), and NaviX Precision Avionics (21 days)."
            )

        # 5. Customers & Regional Client Accounts (English)
        if any(w in q_lower for w in ["customer", "client", "buyer", "city", "cities", "location", "who bought"]):
            if "bangalore" in q_lower or "bengaluru" in q_lower:
                return SQLAssistantResult(
                    sql_query="SELECT id, name, company_name, city, state FROM customers WHERE city LIKE '%Bangalore%' OR city LIKE '%Bengaluru%' LIMIT 10;",
                    explanation_en="Filters customers located in Bangalore / Bengaluru.",
                    natural_response="Displaying enterprise clients in Bangalore, including AeroSpace Labs India and DroneDynamics Tech."
                )
            if "chennai" in q_lower:
                return SQLAssistantResult(
                    sql_query="SELECT id, name, company_name, city, state FROM customers WHERE city LIKE '%Chennai%' LIMIT 10;",
                    explanation_en="Filters customers located in Chennai.",
                    natural_response="Displaying enterprise clients in Chennai, including Skyline Geospatial Mapping and Coastal Surveillance Drones."
                )
            if "hyderabad" in q_lower:
                return SQLAssistantResult(
                    sql_query="SELECT id, name, company_name, city, state FROM customers WHERE city LIKE '%Hyderabad%' LIMIT 10;",
                    explanation_en="Filters customers located in Hyderabad.",
                    natural_response="Displaying enterprise clients in Hyderabad, including Deccan Drones Pvt Ltd."
                )
            return SQLAssistantResult(
                sql_query="SELECT id, name, company_name, city, state FROM customers ORDER BY id ASC LIMIT 10;",
                explanation_en="Lists enterprise clients and customer accounts.",
                natural_response="Trentar serves 40 enterprise customers across India, including AeroSpace Labs India (Bangalore), Deccan Drones (Hyderabad), and Coimbatore AgriTech Solutions."
            )

        # 6. Sales, Total Revenue, Margins & Profit (English)
        if any(w in q_lower for w in ["revenue", "turnover", "profit", "margin", "how much sold", "earnings", "financial"]) or ("sales" in q_lower and "top" not in q_lower and "best" not in q_lower):
            return SQLAssistantResult(
                sql_query="SELECT count(*) AS total_transactions, round(sum(quantity_sold), 0) AS total_units_sold, round(sum(total_revenue), 2) AS total_revenue_inr, round(sum(gross_profit), 2) AS total_gross_profit_inr FROM sales_history;",
                explanation_en="Aggregates historical sales volume, revenue, and gross profit across all 589 transactions.",
                natural_response="Total recorded sales volume is ₹2,68,80,300 across 589 transactions with 2,017 units sold and ₹99,61,450 in gross profit (37.1% blended margin)."
            )

        # 7. Top Selling / Best Sellers / Popular Products (English)
        if any(w in q_lower for w in ["top", "best", "most sold", "highest sales", "popular", "fastest moving"]):
            return SQLAssistantResult(
                sql_query="SELECT p.sku, p.name, sum(s.quantity_sold) AS units_sold, round(sum(s.total_revenue), 2) AS total_revenue FROM sales_history s JOIN products p ON s.product_id = p.id GROUP BY p.id ORDER BY units_sold DESC LIMIT 5;",
                explanation_en="Calculates top 5 products by historical units sold and generated revenue.",
                natural_response="Our top 3 best-selling products are: 1) High-Torque 4014 BLDC Motor (163 units, ₹21.98 Lakhs), 2) 3K Twill Carbon Fiber Tube (142 units, ₹6.39 Lakhs), and 3) Grade 5 Titanium M3 Fastener Kit (127 units, ₹4.44 Lakhs)."
            )

        # 8. Category Lookups: Motors
        if any(w in q_lower for w in ["motor", "bldc", "kv"]):
            return SQLAssistantResult(
                sql_query="SELECT sku, name, current_stock, unit_selling_price FROM products WHERE category = 'Motors' OR name LIKE '%Motor%' ORDER BY current_stock ASC;",
                explanation_en="Queries inventory for electric drone propulsion motors.",
                natural_response="Displaying motor inventory: High-Torque 4014 BLDC Motor (34 in stock at ₹13,500), and Heavy-Lift 8318 100KV Industrial Motor (8 in stock at ₹38,000)."
            )

        # 9. Category Lookups: Batteries & Power
        if any(w in q_lower for w in ["battery", "batteries", "lipo", "power", "cell", "mah"]):
            return SQLAssistantResult(
                sql_query="SELECT sku, name, current_stock, unit_selling_price FROM products WHERE category = 'Power' OR name LIKE '%Pack%' OR name LIKE '%Battery%' ORDER BY current_stock ASC;",
                explanation_en="Queries inventory for industrial drone battery packs and energy solutions.",
                natural_response="Displaying power packs: 22.2V 6S 22,000mAh Solid-State LiPo Pack (6 in stock at ₹28,500), and 44.4V 12S 16,000mAh Smart Industrial Pack (7 in stock at ₹48,000)."
            )

        # 10. Category Lookups: Frames & Airframes
        if any(w in q_lower for w in ["frame", "airframe", "carbon", "vtol", "hexacopter"]):
            return SQLAssistantResult(
                sql_query="SELECT sku, name, current_stock, unit_selling_price FROM products WHERE category = 'Airframes' OR name LIKE '%Frame%' OR name LIKE '%VTOL%' ORDER BY current_stock ASC;",
                explanation_en="Queries inventory for carbon fiber airframes and structural kits.",
                natural_response="Displaying airframes: Tandem Wing Hybrid VTOL Airframe 2400mm (3 in stock at ₹95,000), and Hexacopter Carbon Fiber 1200mm Frame Kit (4 in stock at ₹42,000)."
            )

        # 11. Category Lookups: Cameras, Payloads & Sensors
        if any(w in q_lower for w in ["camera", "payload", "gimbal", "sensor", "thermal", "rtk", "avionics"]):
            return SQLAssistantResult(
                sql_query="SELECT sku, name, current_stock, unit_selling_price FROM products WHERE category IN ('Payloads', 'Avionics') OR name LIKE '%Gimbal%' OR name LIKE '%Sensor%' ORDER BY current_stock ASC;",
                explanation_en="Queries inventory for sensor payloads, gimbals, and avionics modules.",
                natural_response="Displaying sensor payloads: Dual 4K EO / 640 Thermal Gimbal (2 in stock at ₹1,45,000), Multi-Band RTK GNSS Receiver (5 in stock at ₹28,000), and 30X Optical Zoom Gimbal (14 in stock at ₹82,000)."
            )

        # 12. Category Lookups: Propellers
        if any(w in q_lower for w in ["propeller", "prop", "folding"]):
            return SQLAssistantResult(
                sql_query="SELECT sku, name, current_stock, unit_selling_price FROM products WHERE category = 'Propellers' OR name LIKE '%Propeller%' ORDER BY current_stock ASC;",
                explanation_en="Queries inventory for carbon fiber propeller pairs.",
                natural_response="Displaying propeller sets: 30x10.5 Folding Carbon Propeller Pair (18 in stock at ₹8,500) and 22x7.2 Carbon Propellers (42 in stock at ₹4,800)."
            )

        # 13. Price / Cost / Expensive Queries
        if any(w in q_lower for w in ["expensive", "costliest", "highest price", "highest cost", "cheapest", "lowest price"]):
            if "cheapest" in q_lower or "lowest" in q_lower:
                return SQLAssistantResult(
                    sql_query="SELECT sku, name, category, unit_selling_price, current_stock FROM products ORDER BY unit_selling_price ASC LIMIT 5;",
                    explanation_en="Retrieves lowest-priced products in catalog.",
                    natural_response="The lowest priced catalog items are fastener kits and wiring accessories, starting from ₹1,200."
                )
            return SQLAssistantResult(
                sql_query="SELECT sku, name, category, unit_selling_price, current_stock FROM products ORDER BY unit_selling_price DESC LIMIT 5;",
                explanation_en="Retrieves top 5 highest-priced products in catalog.",
                natural_response="The highest priced product in our catalog is the Dual 4K EO / 640 Thermal Gimbal Payload (TRN-CAM-4KTH) at ₹1,45,000, followed by the Tandem Wing Hybrid VTOL Airframe (TRN-FRM-VTOL) at ₹95,000."
            )

        # 14. Stock Orders / Purchase Orders (POs)
        if any(w in q_lower for w in ["order", "purchase order", "po"]):
            return SQLAssistantResult(
                sql_query="SELECT so.order_number, s.name AS supplier, so.status, so.total_estimated_cost FROM stock_orders so JOIN suppliers s ON so.supplier_id = s.id ORDER BY so.id DESC LIMIT 5;",
                explanation_en="Retrieves recent supplier purchase orders and fulfillment status.",
                natural_response="Displaying active supplier purchase orders: PO-2026-0042 (Kavach Dynamic Drives, ₹3,80,000), PO-2026-0043 (Shakti Energy Solutions, ₹1,71,000), and PO-2026-0044 (Garuda Composites, ₹1,68,000)."
            )

        # 15. Count / Catalog Size / Total Products
        if any(w in q_lower for w in ["how many", "total products", "catalog size", "inventory count", "total items"]):
            return SQLAssistantResult(
                sql_query="SELECT count(*) AS total_skus, sum(current_stock) AS total_inventory_units, round(avg(unit_selling_price), 2) AS average_price FROM products;",
                explanation_en="Aggregates active catalog product count and total physical units in warehouse.",
                natural_response="Trentar's catalog contains 30 active SKUs across 8 component categories, with 748 total units currently held in warehouse stock."
            )

        # 16. Low Stock / Stock Shortages / Reorder Warning (English)
        if any(w in q_lower for w in ["low stock", "stock", "shortage", "reorder", "critical", "below", "deficit"]):
            return SQLAssistantResult(
                sql_query="SELECT sku, name, current_stock, min_reorder_level, unit_selling_price FROM products WHERE current_stock <= min_reorder_level ORDER BY current_stock ASC LIMIT 10;",
                explanation_en="Filters products where inventory has reached or breached the minimum reorder threshold.",
                natural_response="9 products currently require reordering: Dual 4K Thermal Gimbal (2 units), Hybrid VTOL Airframe (3 units), Hexacopter Frame (4 units), RTK GNSS Receiver (5 units), and 6S 22Ah Solid-State LiPo (6 units)."
            )

        # 17. Keyword Search Fallback
        search_kw = q_clean.replace("show", "").replace("what is", "").replace("what are", "").replace("find", "").replace("me", "").strip()
        if search_kw:
            return SQLAssistantResult(
                sql_query=f"SELECT sku, name, category, current_stock, unit_selling_price FROM products WHERE lower(name) LIKE '%{search_kw}%' OR lower(category) LIKE '%{search_kw}%' LIMIT 10;",
                explanation_en=f"Searches product catalog for items matching '{search_kw}'.",
                natural_response=f"Found products matching your inquiry '{search_kw}'. Review the table below for warehouse quantities and catalog pricing."
            )

        # 18. Default Overview
        return SQLAssistantResult(
            sql_query="SELECT sku, name, category, current_stock, unit_selling_price FROM products ORDER BY current_stock ASC LIMIT 5;",
            explanation_en="Retrieves products with lowest current inventory counts.",
            natural_response="The 5 products with the lowest warehouse stock are TRN-CAM-4KTH (2 units), TRN-FRM-HEX (4 units), TRN-SEN-RTK (5 units), TRN-BAT-6S22A (6 units), and TRN-MOT-8318 (8 units)."
        )

    @classmethod
    def _resolve_insights(cls, text: str, lower: str) -> ExecutiveBriefingReport:
        return ExecutiveBriefingReport(
            headline="Trentar Operations Intelligence: Q1 Supply Chain & Shortfall Outlook",
            executive_summary_markdown=(
                "### Operations Intelligence Briefing — Trentar Pvt Ltd\n\n"
                "**1. Heavy-Lift Propulsion & Power Cells:**\n"
                "Demand for Heavy-Lift Motors (`TRN-MOT-8318`) and Solid-State LiPo Packs (`TRN-BAT-6S22A`) has accelerated by 42% over the last 60 days due to surveillance drone procurement contracts. "
                "Current warehouse inventory will deplete within 9 business days.\n\n"
                "**2. Financial Margins & Working Capital:**\n"
                "- Projected 30-Day Gross Revenue: **₹14.85 Lakhs**\n"
                "- Projected Cost of Goods Sold: **₹9.42 Lakhs**\n"
                "- Blended Gross Margin: **36.5%**\n\n"
                "**3. Immediate Managerial Interventions Recommended:**\n"
                "- Authorize pending Supplier Purchase Orders **PO-2026-0042** (Kavach Drives) and **PO-2026-0043** (Shakti Energy) today to avoid 14-day client delivery delays.\n"
                "- Maintain buffer stock on Grade 5 Titanium fasteners (`TRN-FAS-M3TI`) which currently operate at peak 92% availability."
            ),
            actionable_insights=[
                ExecutiveInsight(
                    category="revenue_risk",
                    severity="critical",
                    finding="TRN-MOT-8318 inventory deficit of 17 units creates immediate risk of contract SLA penalty.",
                    recommended_action="Execute PO-2026-0042 to Kavach Drives immediately with express air-freight."
                ),
                ExecutiveInsight(
                    category="procurement",
                    severity="warning",
                    finding="Solid-state battery cells require 18-day procurement lead time from Shakti Energy.",
                    recommended_action="Increase minimum reorder point from 12 to 25 units."
                ),
                ExecutiveInsight(
                    category="fast_mover",
                    severity="info",
                    finding="TRN-MOT-4014 continues as Trentar's top-volume driver with 185 units sold last quarter.",
                    recommended_action="Negotiate volume discount tier with component supplier."
                )
            ]
        )
