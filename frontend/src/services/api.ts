import type {
  InboundMessage,
  DraftReply,
  MessageDetailResponse,
  StockOrder,
  SQLQueryResponse,
  DemandForecastItem,
  PnLSummary,
  ExecutiveBriefingReport,
  AuditLogItem,
  AppSettings,
  ConnectionTestResult
} from '../types';

const API_BASE = '/api/v1';

export const api = {
  // Messages & Ingestion
  async getMessages(status?: string, intent?: string, priority?: string): Promise<InboundMessage[]> {
    const params = new URLSearchParams();
    if (status) params.append('status', status);
    if (intent) params.append('intent', intent);
    if (priority) params.append('priority', priority);
    const res = await fetch(`${API_BASE}/messages?${params.toString()}`);
    if (!res.ok) throw new Error('Failed to fetch messages');
    return res.json();
  },

  async getMessageDetail(id: number): Promise<MessageDetailResponse> {
    const res = await fetch(`${API_BASE}/messages/${id}`);
    if (!res.ok) throw new Error(`Failed to fetch message detail for ID ${id}`);
    return res.json();
  },

  async simulateInboundMessage(payload: {
    channel: string;
    sender_address: string;
    raw_text: string;
    subject?: string;
  }): Promise<InboundMessage> {
    const res = await fetch(`${API_BASE}/messages/webhook`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    if (!res.ok) throw new Error('Failed to simulate message');
    return res.json();
  },

  async simulateBatch(scenarioIds?: string[]): Promise<{ success: boolean; ingested_count: number; message_ids: number[] }> {
    const params = new URLSearchParams();
    if (scenarioIds) {
      scenarioIds.forEach(id => params.append('scenario_ids', id));
    }
    const res = await fetch(`${API_BASE}/messages/simulate-batch?${params.toString()}`, {
      method: 'POST',
    });
    if (!res.ok) throw new Error('Failed to simulate batch');
    return res.json();
  },

  // Drafts & Human Review
  async getPendingDrafts(): Promise<DraftReply[]> {
    const res = await fetch(`${API_BASE}/drafts/pending`);
    if (!res.ok) throw new Error('Failed to fetch pending drafts');
    return res.json();
  },

  async approveDraft(draftId: number): Promise<DraftReply> {
    const res = await fetch(`${API_BASE}/drafts/${draftId}/approve`, {
      method: 'POST',
    });
    if (!res.ok) throw new Error(`Failed to approve draft ${draftId}`);
    return res.json();
  },

  async editDraft(draftId: number, editedText: string): Promise<DraftReply> {
    const res = await fetch(`${API_BASE}/drafts/${draftId}/edit`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ edited_text: editedText }),
    });
    if (!res.ok) throw new Error(`Failed to edit draft ${draftId}`);
    return res.json();
  },

  async rejectDraft(draftId: number, reason: string): Promise<DraftReply> {
    const res = await fetch(`${API_BASE}/drafts/${draftId}/reject?reason=${encodeURIComponent(reason)}`, {
      method: 'POST',
    });
    if (!res.ok) throw new Error(`Failed to reject draft ${draftId}`);
    return res.json();
  },

  // Stock & Inventory (E2)
  async getInventory(lowStockOnly: boolean = false): Promise<any[]> {
    const res = await fetch(`${API_BASE}/inventory?low_stock_only=${lowStockOnly}`);
    if (!res.ok) throw new Error('Failed to fetch inventory');
    return res.json();
  },

  async getStockOrders(status?: string): Promise<StockOrder[]> {
    const params = status ? `?status=${status}` : '';
    const res = await fetch(`${API_BASE}/stock-orders${params}`);
    if (!res.ok) throw new Error('Failed to fetch stock orders');
    return res.json();
  },

  async approveStockOrder(orderId: number, managerNotes?: string): Promise<StockOrder> {
    const res = await fetch(`${API_BASE}/stock-orders/${orderId}/approve`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ manager_notes: managerNotes }),
    });
    if (!res.ok) throw new Error(`Failed to approve stock order ${orderId}`);
    return res.json();
  },

  // Employee SQL Assistant (E3)
  async queryAssistant(prompt: string, language: string = 'en'): Promise<SQLQueryResponse> {
    const res = await fetch(`${API_BASE}/assistant/query`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ prompt, language }),
    });
    if (!res.ok) throw new Error('Failed to query assistant');
    return res.json();
  },

  // Analytics & Forecast (E4)
  async getDemandForecast(horizonDays: number = 30): Promise<DemandForecastItem[]> {
    const res = await fetch(`${API_BASE}/analytics/demand-forecast?horizon_days=${horizonDays}`);
    if (!res.ok) throw new Error('Failed to fetch forecast');
    return res.json();
  },

  async getPnLSummary(): Promise<PnLSummary> {
    const res = await fetch(`${API_BASE}/analytics/pnl-summary`);
    if (!res.ok) throw new Error('Failed to fetch P&L summary');
    return res.json();
  },

  async generateExecutiveInsights(): Promise<ExecutiveBriefingReport> {
    const res = await fetch(`${API_BASE}/analytics/generate-insights`, {
      method: 'POST',
    });
    if (!res.ok) throw new Error('Failed to generate insights');
    return res.json();
  },

  // Audit & Settings
  async getAuditLogs(limit: number = 50): Promise<AuditLogItem[]> {
    const res = await fetch(`${API_BASE}/audit/logs?limit=${limit}`);
    if (!res.ok) throw new Error('Failed to fetch audit logs');
    return res.json();
  },

  async getSettings(): Promise<AppSettings> {
    const res = await fetch(`${API_BASE}/settings`);
    if (!res.ok) throw new Error('Failed to fetch settings');
    return res.json();
  },

  async updateSettings(update: { use_mock_llm?: boolean; auto_approve_delay_minutes?: number }): Promise<any> {
    const res = await fetch(`${API_BASE}/settings`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(update),
    });
    if (!res.ok) throw new Error('Failed to update settings');
    return res.json();
  },

  async testConnection(): Promise<ConnectionTestResult> {
    const res = await fetch(`${API_BASE}/settings/test-connection`, {
      method: 'POST',
    });
    if (!res.ok) throw new Error('Failed to test LLM connection');
    return res.json();
  },
};
