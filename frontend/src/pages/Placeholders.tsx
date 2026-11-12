import React from 'react';
import { Package, ShieldAlert, TrendingUp, Mic } from 'lucide-react';

export const StockOrdersPlaceholder: React.FC = () => (
  <div className="flex-1 bg-slate-950 p-8 flex flex-col items-center justify-center text-center">
    <Package className="w-12 h-12 text-amber-500 mb-3" />
    <h2 className="text-lg font-bold text-white">Stock Orders & Shortfall Management (E2)</h2>
    <p className="text-xs text-slate-400 max-w-md mt-1">
      Automated Supplier Purchase Order generation for Kavach Drives, Garuda Composites, and Shakti Energy.
      Scheduled for Phase 4 activation.
    </p>
  </div>
);

export const AssistantPlaceholder: React.FC = () => (
  <div className="flex-1 bg-slate-950 p-8 flex flex-col items-center justify-center text-center">
    <Mic className="w-12 h-12 text-sky-400 mb-3" />
    <h2 className="text-lg font-bold text-white">Ask Trentar AI — Frontline Voice Assistant (E3)</h2>
    <p className="text-xs text-slate-400 max-w-md mt-1">
      Safe, read-only Text-to-SQL engine with browser Web Speech synthesis in English, Tamil, and Hindi.
      Scheduled for Phase 5 activation.
    </p>
  </div>
);

export const AnalyticsPlaceholder: React.FC = () => (
  <div className="flex-1 bg-slate-950 p-8 flex flex-col items-center justify-center text-center">
    <TrendingUp className="w-12 h-12 text-emerald-400 mb-3" />
    <h2 className="text-lg font-bold text-white">Predictive Forecast & Profit/Loss (E4)</h2>
    <p className="text-xs text-slate-400 max-w-md mt-1">
      30-day weighted moving average demand curve, stock-out risk analysis, and AI executive briefings.
      Scheduled for Phase 6 activation.
    </p>
  </div>
);

export const AuditLogPlaceholder: React.FC = () => (
  <div className="flex-1 bg-slate-950 p-8 flex flex-col items-center justify-center text-center">
    <ShieldAlert className="w-12 h-12 text-purple-400 mb-3" />
    <h2 className="text-lg font-bold text-white">Compliance Audit Trail & Security Logs</h2>
    <p className="text-xs text-slate-400 max-w-md mt-1">
      Immutable tracking of human approvals, auto-approval timers, and blocked prompt-injection attempts.
    </p>
  </div>
);

