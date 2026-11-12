export interface Customer {
  id: number;
  customer_code: string;
  name: string;
  email: string;
  phone: string;
  company_name: string;
  city: string;
  state: string;
}

export interface InboundMessage {
  id: number;
  customer_id?: number | null;
  channel: string;
  sender_address: string;
  subject?: string;
  raw_text: string;
  language: "en" | "ta" | "hi" | string;
  detected_intent: "price_quote" | "bulk_order" | "stock_inquiry" | "order_status" | "complaint" | "refund" | "general" | string;
  detected_sentiment: "positive" | "neutral" | "negative" | "frustrated" | string;
  priority: "low" | "medium" | "high" | "urgent" | string;
  prompt_injection_detected: boolean;
  processing_status: "received" | "drafted" | "flagged" | "processed" | string;
  received_at: string;
}

export interface DraftReply {
  id: number;
  inbound_message_id: number;
  draft_text: string;
  edited_text?: string | null;
  status: "pending" | "approved" | "rejected" | "auto_approved" | "escalated" | "sent" | string;
  confidence_score: number;
  safety_evaluation_notes?: string | null;
  auto_approve_deadline: string;
  reviewed_at?: string | null;
  reviewed_by?: string | null;
  sent_at?: string | null;
  created_at: string;
  seconds_remaining?: number;
}

export interface MessageDetailResponse {
  message: InboundMessage;
  draft?: DraftReply | null;
  stock_order?: StockOrder | null;
  customer?: Customer | null;
}

export interface StockOrderItem {
  id: number;
  product_id: number;
  product_sku?: string;
  product_name?: string;
  requested_quantity: number;
  in_hand_stock: number;
  shortfall_quantity: number;
  estimated_unit_cost: number;
  subtotal: number;
}

export interface StockOrder {
  id: number;
  order_number: string;
  inbound_message_id?: number | null;
  supplier_id: number;
  supplier_name?: string;
  supplier_email?: string;
  status: "draft" | "approved" | "rejected" | "sent" | string;
  total_estimated_cost: number;
  manager_notes?: string | null;
  created_at: string;
  approved_at?: string | null;
  items: StockOrderItem[];
}

export interface SQLQueryResponse {
  sql_query: string;
  explanation: string;
  natural_response: string;
  results: Record<string, any>[];
  row_count: number;
  execution_time_ms: number;
  speech_ready: boolean;
}

export interface DemandForecastItem {
  product_id: number;
  sku: string;
  product_name: string;
  category: string;
  current_stock: number;
  forecast_30d_demand: number;
  daily_run_rate: number;
  stockout_risk_pct: number;
  reorder_point: number;
  reorder_recommended: boolean;
  status: "CRITICAL" | "WARNING" | "HEALTHY";
}

export interface PnLSummary {
  total_sales_volume: number;
  total_revenue: number;
  total_cogs: number;
  total_gross_profit: number;
  gross_margin_pct: number;
  projected_month_revenue: number;
  projected_month_cogs: number;
  projected_month_profit: number;
}

export interface ExecutiveInsight {
  category: "procurement" | "revenue_risk" | "fast_mover" | "margin_optimization";
  severity: "info" | "warning" | "critical";
  finding: string;
  recommended_action: string;
}

export interface ExecutiveBriefingReport {
  headline: string;
  executive_summary_markdown: string;
  actionable_insights: ExecutiveInsight[];
  generated_at: string;
}

export interface AuditLogItem {
  id: number;
  entity_type: string;
  entity_id: number;
  action: string;
  actor_type: string;
  actor_id: string;
  details_json?: string | null;
  timestamp: string;
}

export interface AppSettings {
  app_env: string;
  use_mock_llm: boolean;
  llm_mock_config?: boolean;
  api_key_configured?: boolean;
  masked_key?: string;
  auto_approve_delay_minutes: number;
  sender?: {
    name: string;
    title: string;
    company: string;
    email: string;
  };
  models: {
    intake: string;
    drafter: string;
    orchestrator: string;
    sql: string;
    insights: string;
  };
}

export interface ModelRoleStatus {
  model: string;
  status: 'connected' | 'credit_required' | 'mock' | 'error' | 'network_error';
  latency_ms: number;
  message: string;
}

export interface ConnectionTestResult {
  endpoint: string;
  api_key_configured: boolean;
  masked_key: string;
  is_mock_active: boolean;
  roles: Record<string, ModelRoleStatus>;
}
