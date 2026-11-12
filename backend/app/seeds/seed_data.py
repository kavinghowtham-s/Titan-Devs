import os
import random
from datetime import datetime, timedelta, date, timezone
from sqlalchemy.orm import Session
from backend.app.core.database import SessionLocal, engine, Base
from backend.app.models.customer import Customer
from backend.app.models.supplier import Supplier
from backend.app.models.product import Product
from backend.app.models.message import InboundMessage, DraftReply, OutboxMessage
from backend.app.models.stock import StockOrder, StockOrderItem
from backend.app.models.sales import SalesHistory
from backend.app.models.audit import AuditLog
from backend.app.seeds.sample_messages import SAMPLE_MESSAGES
from backend.app.config import settings

def seed_database():
    print("[SEED] Re-initializing database tables...")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db: Session = SessionLocal()

    try:
        # 1. SEED SUPPLIERS (5 Key Suppliers)
        print("[SEED] Seeding suppliers...")
        suppliers_data = [
            Supplier(
                supplier_code="SUP-GARUDA-01",
                name="Garuda Composites Pvt Ltd",
                contact_person="Ramesh Kannan",
                email="procurement@garudacomposites.in",
                phone="+91 98401 22334",
                category="Airframes & Composites",
                default_lead_time_days=14,
                payment_terms="Net 30"
            ),
            Supplier(
                supplier_code="SUP-KAVACH-02",
                name="Kavach Dynamic Drives",
                contact_person="Vikram Rao",
                email="orders@kavachdrives.com",
                phone="+91 99805 44321",
                category="Motors & ESCs",
                default_lead_time_days=10,
                payment_terms="Net 15"
            ),
            Supplier(
                supplier_code="SUP-NAVIX-03",
                name="NaviX Precision Avionics",
                contact_person="Dr. Sunita Sen",
                email="b2b@navixavionics.com",
                phone="+91 94432 88991",
                category="Avionics & Sensors",
                default_lead_time_days=21,
                payment_terms="Net 45"
            ),
            Supplier(
                supplier_code="SUP-SHAKTI-04",
                name="Shakti Energy Solutions",
                contact_person="Arun Chaudhary",
                email="supply@shaktienergy.co.in",
                phone="+91 98221 77665",
                category="Power & Batteries",
                default_lead_time_days=18,
                payment_terms="Net 30"
            ),
            Supplier(
                supplier_code="SUP-BHARAT-05",
                name="Bharat Micro Fasteners & CNC",
                contact_person="Mahesh Agarwal",
                email="sales@bharatfasteners.in",
                phone="+91 97112 55443",
                category="Hardware & Fasteners",
                default_lead_time_days=5,
                payment_terms="Net 15"
            )
        ]
        db.add_all(suppliers_data)
        db.commit()

        # 2. SEED PRODUCTS (30 Trentar Industrial Items)
        print("[SEED] Seeding 30 Trentar industrial products...")
        products_data = [
            # Motors & ESCs (Supplier 2 - Kavach)
            Product(sku="TRN-MOT-4014", name="High-Torque 4014 BLDC Motor", category="Motors", description="High efficiency 380KV drone motor for 10-15kg payload hexacopters", unit_selling_price=3800.0, unit_cost_price=2200.0, current_stock=45, min_reorder_level=15, lead_time_days=7, supplier_id=2),
            Product(sku="TRN-MOT-8318", name="Heavy-Lift 8318 100KV Industrial Motor", category="Motors", description="Industrial drone propulsion motor for heavy payloads up to 30kg", unit_selling_price=14500.0, unit_cost_price=8900.0, current_stock=8, min_reorder_level=10, lead_time_days=10, supplier_id=2),
            Product(sku="TRN-MOT-6215", name="Precision 6215 170KV Agricultural Motor", category="Motors", description="IP67 waterproof agricultural crop-spraying motor", unit_selling_price=6800.0, unit_cost_price=4100.0, current_stock=32, min_reorder_level=15, lead_time_days=10, supplier_id=2),
            Product(sku="TRN-ESC-80A", name="Opto-Isolated 80A 12S ESC", category="Motors", description="High-frequency telemetry ESC with active braking", unit_selling_price=4200.0, unit_cost_price=2400.0, current_stock=60, min_reorder_level=20, lead_time_days=7, supplier_id=2),
            Product(sku="TRN-ESC-120A", name="Telemetry 120A High-Voltage ESC", category="Motors", description="Industrial heavy ESC supporting up to 14S LiPo systems", unit_selling_price=7800.0, unit_cost_price=4600.0, current_stock=12, min_reorder_level=15, lead_time_days=10, supplier_id=2),
            Product(sku="TRN-ESC-40A4", name="4-in-1 Compact 40A Flight ESC", category="Motors", description="Compact survey quadcopter integrated motor speed controller", unit_selling_price=3400.0, unit_cost_price=1950.0, current_stock=28, min_reorder_level=12, lead_time_days=7, supplier_id=2),

            # Avionics & Sensors (Supplier 3 - NaviX)
            Product(sku="TRN-FC-PRO", name="Trentar Triple-Redundant Flight Controller", category="Avionics", description="Triple IMU redundant navigation computer with ArduPilot/PX4 support", unit_selling_price=34000.0, unit_cost_price=21000.0, current_stock=14, min_reorder_level=8, lead_time_days=15, supplier_id=3),
            Product(sku="TRN-FC-LITE", name="Survey Mini Autopilot Flight Computer", category="Avionics", description="Lightweight industrial navigation autopilot for mapping drones", unit_selling_price=18500.0, unit_cost_price=11000.0, current_stock=22, min_reorder_level=10, lead_time_days=15, supplier_id=3),
            Product(sku="TRN-SEN-RTK", name="Multi-Band RTK GNSS Receiver Module", category="Avionics", description="Centimeter-level positioning module with helical antenna", unit_selling_price=28000.0, unit_cost_price=18500.0, current_stock=5, min_reorder_level=8, lead_time_days=21, supplier_id=3),
            Product(sku="TRN-SEN-OPTO", name="Optical Flow & Obstacle Avoidance Lidar", category="Avionics", description="Dual-band laser altimeter and indoor obstacle rangefinder", unit_selling_price=12000.0, unit_cost_price=7500.0, current_stock=22, min_reorder_level=10, lead_time_days=14, supplier_id=3),
            Product(sku="TRN-SEN-AIR", name="Digital Pitot Tube Airspeed Sensor", category="Avionics", description="High accuracy differential pressure sensor for fixed-wing drones", unit_selling_price=4800.0, unit_cost_price=2800.0, current_stock=35, min_reorder_level=12, lead_time_days=12, supplier_id=3),
            Product(sku="TRN-SEN-MAG", name="External Industrial Magnetometer Compass", category="Avionics", description="Anti-interference 3-axis digital compass module", unit_selling_price=3200.0, unit_cost_price=1700.0, current_stock=40, min_reorder_level=15, lead_time_days=10, supplier_id=3),

            # Airframes & Composites (Supplier 1 - Garuda)
            Product(sku="TRN-FRM-HEX", name="Hexacopter Carbon Fiber 1200mm Frame Kit", category="Airframes", description="Heavy-duty 3K weave folding carbon frame for industrial sensors", unit_selling_price=42000.0, unit_cost_price=26000.0, current_stock=4, min_reorder_level=5, lead_time_days=18, supplier_id=1),
            Product(sku="TRN-FRM-QUAD", name="Quadcopter Survey Frame 650mm", category="Airframes", description="Compact foldable inspection airframe with vibration isolated gimbal plate", unit_selling_price=18500.0, unit_cost_price=11200.0, current_stock=25, min_reorder_level=10, lead_time_days=12, supplier_id=1),
            Product(sku="TRN-FRM-VTOL", name="Tandem Wing Hybrid VTOL Airframe 2400mm", category="Airframes", description="Long-range fixed-wing VTOL composite airframe with 2hr endurance", unit_selling_price=95000.0, unit_cost_price=62000.0, current_stock=3, min_reorder_level=4, lead_time_days=25, supplier_id=1),
            Product(sku="TRN-CF-TUBE25", name="3K Twill Carbon Fiber Tube (25mm x 500mm)", category="Airframes", description="High-modulus carbon tube for drone arms and landing skids", unit_selling_price=1450.0, unit_cost_price=850.0, current_stock=110, min_reorder_level=30, lead_time_days=5, supplier_id=1),
            Product(sku="TRN-CF-TUBE30", name="Heavy Carbon Tube (30mm x 600mm)", category="Airframes", description="Heavy industrial carbon arm tube with pre-drilled CNC holes", unit_selling_price=2100.0, unit_cost_price=1250.0, current_stock=75, min_reorder_level=20, lead_time_days=7, supplier_id=1),
            Product(sku="TRN-CF-PLATE", name="3mm Toray Carbon Fiber Plate 400x400", category="Airframes", description="High rigidity CNC-machinable carbon center plate sheet", unit_selling_price=3800.0, unit_cost_price=2300.0, current_stock=42, min_reorder_level=15, lead_time_days=8, supplier_id=1),

            # Propellers & Payloads
            Product(sku="TRN-PROP-3010", name="30x10.5 Folding Carbon Propeller Pair", category="Propellers", description="Dynamic balanced ultra-light carbon folding blades (CW + CCW)", unit_selling_price=4500.0, unit_cost_price=2600.0, current_stock=18, min_reorder_level=20, lead_time_days=8, supplier_id=1),
            Product(sku="TRN-PROP-2208", name="22x8 Carbon Fiber Direct-Drive Propellers", category="Propellers", description="Precision matched carbon propellers for survey multicopters", unit_selling_price=3100.0, unit_cost_price=1750.0, current_stock=55, min_reorder_level=25, lead_time_days=6, supplier_id=1),
            Product(sku="TRN-PROP-1855", name="18x5.5 High-Speed Propeller Set", category="Propellers", description="High RPM balanced composite blades", unit_selling_price=2200.0, unit_cost_price=1200.0, current_stock=80, min_reorder_level=30, lead_time_days=5, supplier_id=1),
            Product(sku="TRN-CAM-4KTH", name="Dual 4K EO / 640 Thermal Gimbal Payload", category="Payloads", description="3-axis stabilized military-grade dual sensor optical/thermal payload", unit_selling_price=145000.0, unit_cost_price=98000.0, current_stock=2, min_reorder_level=3, lead_time_days=30, supplier_id=3),
            Product(sku="TRN-CAM-ZOOM", name="30X Optical Zoom Daylight Gimbal", category="Payloads", description="Target tracking long-range zoom camera for powerline inspection", unit_selling_price=82000.0, unit_cost_price=54000.0, current_stock=5, min_reorder_level=4, lead_time_days=20, supplier_id=3),

            # Power & Batteries (Supplier 4 - Shakti)
            Product(sku="TRN-BAT-6S22A", name="22.2V 6S 22,000mAh Solid-State LiPo Pack", category="Power", description="High energy density battery for heavy commercial multicopters", unit_selling_price=26500.0, unit_cost_price=17000.0, current_stock=6, min_reorder_level=12, lead_time_days=18, supplier_id=4),
            Product(sku="TRN-BAT-12S16A", name="44.4V 12S 16,000mAh Smart Industrial Pack", category="Power", description="Integrated battery management system with CAN bus telemetry", unit_selling_price=39000.0, unit_cost_price=25500.0, current_stock=7, min_reorder_level=8, lead_time_days=20, supplier_id=4),
            Product(sku="TRN-PDB-500A", name="High Current 500A Power Distribution Board", category="Power", description="Dual voltage regulated PCB with 12S/14S support", unit_selling_price=5600.0, unit_cost_price=3200.0, current_stock=38, min_reorder_level=15, lead_time_days=10, supplier_id=4),

            # Fasteners & Hardware (Supplier 5 - Bharat)
            Product(sku="TRN-FAS-M3TI", name="Grade 5 Titanium M3 Fastener Kit (100 pcs)", category="Fasteners", description="Corrosion resistant lightweight aerospace titanium hex screws", unit_selling_price=1200.0, unit_cost_price=600.0, current_stock=150, min_reorder_level=40, lead_time_days=4, supplier_id=5),
            Product(sku="TRN-FAS-M4CNC", name="Anodized Aluminium M4 Locknut Set (50 pcs)", category="Fasteners", description="High tensile vibration proof self-locking aircraft hardware", unit_selling_price=850.0, unit_cost_price=420.0, current_stock=210, min_reorder_level=50, lead_time_days=4, supplier_id=5),
            Product(sku="TRN-MNT-MOT", name="CNC Machined 6061-T6 Quick-Release Motor Mount", category="Hardware", description="Vibration dampening universal motor clamp plate", unit_selling_price=2400.0, unit_cost_price=1350.0, current_stock=64, min_reorder_level=20, lead_time_days=6, supplier_id=5),
            Product(sku="TRN-MNT-ANT", name="Folding GPS Helical Mast Antenna Bracket", category="Hardware", description="Quick fold CNC mast for RTK and compass modules", unit_selling_price=950.0, unit_cost_price=480.0, current_stock=90, min_reorder_level=30, lead_time_days=5, supplier_id=5)
        ]
        db.add_all(products_data)
        db.commit()

        # 3. SEED CUSTOMERS (40 Indian B2B Industrial Clients)
        print("[SEED] Seeding 40 B2B customers...")
        cities_states = [
            ("Chennai", "Tamil Nadu"), ("Bangalore", "Karnataka"), ("Pune", "Maharashtra"),
            ("Coimbatore", "Tamil Nadu"), ("Hyderabad", "Telangana"), ("New Delhi", "Delhi NCR"),
            ("Ahmedabad", "Gujarat"), ("Jaipur", "Rajasthan"), ("Bhopal", "Madhya Pradesh"),
            ("Kochi", "Kerala"), ("Indore", "Madhya Pradesh"), ("Madurai", "Tamil Nadu")
        ]
        customers_data = []
        now_dt = datetime.now(timezone.utc)
        for i in range(1, 41):
            city, state = random.choice(cities_states)
            cust = Customer(
                customer_code=f"CUST-TRN-{i:03d}",
                name=f"Customer Rep {i}",
                email=f"client{i}@indiatrendustries{i}.in",
                phone=f"+91 {random.randint(90000, 99999)} {random.randint(10000, 99999)}",
                company_name=f"Indo-Aero Dynamics {i} Ltd",
                city=city,
                state=state,
                created_at=now_dt - timedelta(days=random.randint(60, 365))
            )
            customers_data.append(cust)

        # Explicitly map known sample message contacts
        customers_data[0].name = "Vikram Patel"
        customers_data[0].email = "vikram@aerospacelabs.in"
        customers_data[0].company_name = "AeroSpace Labs India"
        customers_data[0].city = "Bangalore"

        customers_data[1].name = "Sneha Reddy"
        customers_data[1].email = "sneha@deccandrones.in"
        customers_data[1].company_name = "Deccan Drones Pvt Ltd"
        customers_data[1].city = "Hyderabad"

        customers_data[2].name = "Karthik Ramanathan"
        customers_data[2].email = "karthik@coimbatoreagri.com"
        customers_data[2].company_name = "Coimbatore AgriTech Solutions"
        customers_data[2].city = "Coimbatore"

        customers_data[3].name = "Rajeshwar Singh"
        customers_data[3].email = "rajeshwar@agroviman.com"
        customers_data[3].company_name = "AgroViman Uttar Pradesh"
        customers_data[3].city = "Lucknow"

        customers_data[4].name = "Arvind Swamy"
        customers_data[4].email = "arvind@skylinemapping.in"
        customers_data[4].company_name = "Skyline Geospatial Mapping"
        customers_data[4].city = "Chennai"

        customers_data[5].name = "Amit Bansal"
        customers_data[5].email = "amit@apexdefense.com"
        customers_data[5].company_name = "Apex Defense Dynamics"
        customers_data[5].city = "Pune"

        db.add_all(customers_data)
        db.commit()

        # 4. SEED 12 MONTHS REALISTIC SALES HISTORY (~450 Transactions)
        print("[SEED] Generating 12-month sales history...")
        sales_records = []
        today = date.today()
        all_products = db.query(Product).all()
        all_customers = db.query(Customer).all()

        for day_offset in range(365, 0, -1):
            sale_dt = today - timedelta(days=day_offset)
            num_sales = random.randint(1, 3) if sale_dt.weekday() < 5 else random.randint(0, 1)

            for _ in range(num_sales):
                prod = random.choice(all_products)
                cust = random.choice(all_customers)
                
                if prod.sku in ["TRN-MOT-4014", "TRN-PROP-3010", "TRN-CF-TUBE25", "TRN-FAS-M3TI"]:
                    qty = random.randint(3, 12)
                elif prod.sku in ["TRN-CAM-4KTH", "TRN-FRM-VTOL"]:
                    qty = 1
                else:
                    qty = random.randint(1, 5)

                unit_sale_price = prod.unit_selling_price
                unit_cost = prod.unit_cost_price
                total_rev = round(unit_sale_price * qty, 2)
                total_c = round(unit_cost * qty, 2)
                gross_p = round(total_rev - total_c, 2)

                sales_records.append(SalesHistory(
                    product_id=prod.id,
                    customer_id=cust.id,
                    quantity_sold=qty,
                    unit_sale_price=unit_sale_price,
                    total_revenue=total_rev,
                    total_cost=total_c,
                    gross_profit=gross_p,
                    sale_date=sale_dt
                ))

        db.add_all(sales_records)
        db.commit()

        # 5. SEED SAMPLE MESSAGES & DRAFTS (The 15 Test Scenarios)
        print("[SEED] Seeding 15 sample customer messages and contextual drafts...")
        from backend.app.llm.mock_llm import MockLLMRegistry
        from backend.app.schemas.message_dto import IntakeClassificationResult
        from backend.app.schemas.draft_dto import DrafterResponse

        for idx, sample in enumerate(SAMPLE_MESSAGES):
            matched_cust = db.query(Customer).filter(Customer.email == sample["sender_address"]).first()
            cust_id = matched_cust.id if matched_cust else None

            classification = MockLLMRegistry.resolve("MODEL_INTAKE", sample["raw_text"], IntakeClassificationResult)

            msg_received_at = now_dt - timedelta(minutes=(idx + 1) * 6)

            inbound = InboundMessage(
                customer_id=cust_id,
                channel=sample["channel"],
                sender_address=sample["sender_address"],
                subject=sample["subject"],
                raw_text=sample["raw_text"],
                language=classification.language,
                detected_intent=classification.detected_intent,
                detected_sentiment=classification.sentiment,
                priority=classification.priority,
                prompt_injection_detected=classification.is_prompt_injection,
                processing_status="flagged" if classification.is_prompt_injection else "received",
                received_at=msg_received_at
            )
            db.add(inbound)
            db.flush()

            if classification.is_prompt_injection:
                db.add(AuditLog(
                    entity_type="SECURITY",
                    entity_id=inbound.id,
                    action="BLOCKED",
                    actor_type="INTAKE_AGENT",
                    actor_id="SECURITY_GUARDRAIL",
                    details_json=f'{{"reason": "Prompt injection tokens neutralized in message {sample["scenario_id"]}"}}',
                    timestamp=msg_received_at
                ))
                continue

            # Check stock shortfall
            catalog_lines = []
            stock_lines = []
            for req in classification.requirements:
                if req.sku:
                    prod = db.query(Product).filter(Product.sku == req.sku).first()
                    if prod:
                        catalog_lines.append(f"SKU: {prod.sku} | Name: {prod.name} | Unit Price: Rs. {prod.unit_selling_price}")
                        stock_lines.append(f"SKU: {prod.sku} | In-Hand: {prod.current_stock} | Requested: {req.quantity}")

                        if req.quantity > prod.current_stock:
                            deficit = req.quantity - prod.current_stock
                            po_cost = round(deficit * prod.unit_cost_price, 2)
                            
                            stock_order = StockOrder(
                                order_number=f"PO-2026-{1000 + inbound.id}",
                                inbound_message_id=inbound.id,
                                supplier_id=prod.supplier_id,
                                status="draft",
                                total_estimated_cost=po_cost,
                                manager_notes=f"Shortfall order for {sample['sender_name']} requirement."
                            )
                            db.add(stock_order)
                            db.flush()

                            db.add(StockOrderItem(
                                stock_order_id=stock_order.id,
                                product_id=prod.id,
                                requested_quantity=req.quantity,
                                in_hand_stock=prod.current_stock,
                                shortfall_quantity=deficit,
                                estimated_unit_cost=prod.unit_cost_price,
                                subtotal=po_cost
                            ))

            # Contextual Draft Prompt
            cust_display_name = matched_cust.name if matched_cust else sample["sender_name"]
            user_prompt = (
                f"Customer Name: {cust_display_name}\n"
                f"Language: {classification.language}\n"
                f"Customer Inquiry:\n{sample['raw_text']}\n\n"
                f"Catalog Context:\n{chr(10).join(catalog_lines)}\n"
                f"Stock Context:\n{chr(10).join(stock_lines)}"
            )

            draft_res = MockLLMRegistry.resolve("MODEL_DRAFTER", user_prompt, DrafterResponse)

            # Deadlines set dynamically into the future so countdowns are active and realistic
            # 1 minute demo override: set between 45 seconds and 300 seconds from now
            deadline = now_dt + timedelta(seconds=60 + (idx * 25))

            draft_reply = DraftReply(
                inbound_message_id=inbound.id,
                draft_text=draft_res.body,
                status="pending",
                confidence_score=0.96,
                auto_approve_deadline=deadline,
                created_at=msg_received_at
            )
            db.add(draft_reply)
            inbound.processing_status = "drafted"

            db.add(AuditLog(
                entity_type="DRAFT",
                entity_id=inbound.id,
                action="CREATED",
                actor_type="MANAGER",
                actor_id="MODEL_DRAFTER",
                details_json=f'{{"scenario": "{sample["scenario_id"]}", "subject": "{draft_res.subject}"}}',
                timestamp=msg_received_at
            ))

        db.commit()
        print("[SEED] Successfully re-seeded Trentar database with active countdowns and accurate drafts!")
    except Exception as e:
        db.rollback()
        print(f"[SEED ERROR] Seeding failed: {e}")
        raise e
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
