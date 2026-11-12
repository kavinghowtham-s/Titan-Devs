import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import type { AuditLogItem } from '../types';
import {
  ShieldCheck,
  RefreshCw,
  Search,
  Filter,
  Code,
  X,
  Clock,
  User,
  Bot,
  AlertTriangle,
  CheckCircle2,
  FileText
} from 'lucide-react';

export const AuditLogPage: React.FC = () => {
  const [logs, setLogs] = useState<AuditLogItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [entityFilter, setEntityFilter] = useState<string>('ALL');
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedLog, setSelectedLog] = useState<AuditLogItem | null>(null);

  const fetchLogs = async () => {
    setLoading(true);
    try {
      const data = await api.getAuditLogs(100);
      setLogs(data);
    } catch (err) {
      console.error('Failed to load audit logs:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchLogs();
  }, []);

  const filteredLogs = logs.filter((log) => {
    if (entityFilter !== 'ALL' && log.entity_type !== entityFilter) {
      return false;
    }
    if (searchQuery.trim()) {
      const q = searchQuery.toLowerCase();
      const matchAction = log.action.toLowerCase().includes(q);
      const matchActor = log.actor_id.toLowerCase().includes(q) || log.actor_type.toLowerCase().includes(q);
      const matchDetails = log.details_json ? log.details_json.toLowerCase().includes(q) : false;
      const matchEntity = `${log.entity_type} #${log.entity_id}`.toLowerCase().includes(q);
      return matchAction || matchActor || matchDetails || matchEntity;
    }
    return true;
  });

  const getActionBadge = (action: string) => {
    switch (action.toUpperCase()) {
      case 'APPROVED':
        return (
          <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded text-[11px] font-medium bg-emerald-50 text-emerald-700 border border-emerald-200 dark:bg-emerald-950/50 dark:text-emerald-300 dark:border-emerald-800">
            <CheckCircle2 className="w-3 h-3 text-emerald-600" />
            Approved
          </span>
        );
      case 'AUTO_APPROVED':
        return (
          <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded text-[11px] font-medium bg-blue-50 text-blue-700 border border-blue-200 dark:bg-blue-950/50 dark:text-blue-300 dark:border-blue-800">
            <Bot className="w-3 h-3 text-blue-600" />
            Auto-approved
          </span>
        );
      case 'ESCALATED':
        return (
          <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded text-[11px] font-medium bg-amber-50 text-amber-700 border border-amber-200 dark:bg-amber-950/50 dark:text-amber-300 dark:border-amber-800">
            <AlertTriangle className="w-3 h-3 text-amber-600" />
            Escalated
          </span>
        );
      case 'REJECTED':
      case 'SECURITY_BLOCKED':
        return (
          <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded text-[11px] font-medium bg-red-50 text-red-700 border border-red-200 dark:bg-red-950/50 dark:text-red-300 dark:border-red-800">
            <X className="w-3 h-3 text-red-600" />
            {action.replace('_', ' ')}
          </span>
        );
      case 'CREATED':
        return (
          <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded text-[11px] font-medium bg-slate-100 text-slate-700 border border-slate-200 dark:bg-slate-800 dark:text-slate-300 dark:border-slate-700">
            Created
          </span>
        );
      default:
        return (
          <span className="inline-flex items-center px-2 py-0.5 rounded text-[11px] font-medium bg-slate-100 text-slate-600 dark:bg-slate-800 dark:text-slate-300">
            {action}
          </span>
        );
    }
  };

  const getActorPill = (actorType: string, actorId: string) => {
    const isBot = actorType.toLowerCase().includes('model') || actorType.toLowerCase().includes('orchestrator') || actorType.toLowerCase().includes('system') || actorId.includes('MODEL');
    return (
      <span className="inline-flex items-center gap-1.5 text-xs text-slate-700 dark:text-slate-300">
        {isBot ? (
          <Bot className="w-3.5 h-3.5 text-slate-400" />
        ) : (
          <User className="w-3.5 h-3.5 text-slate-400" />
        )}
        <span>{actorId || actorType}</span>
      </span>
    );
  };

  const formatTimestamp = (iso: string) => {
    try {
      const d = new Date(iso);
      return d.toLocaleTimeString('en-US', {
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        hour12: true,
      }) + `, ${d.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}`;
    } catch {
      return iso;
    }
  };

  const formatDetailsPreview = (jsonStr?: string | null) => {
    if (!jsonStr) return '—';
    try {
      const parsed = JSON.parse(jsonStr);
      if (parsed.subject) return parsed.subject;
      if (parsed.scenario) return `Scenario: ${parsed.scenario}`;
      if (parsed.reason) return `Reason: ${parsed.reason}`;
      if (parsed.notes) return parsed.notes;
      if (parsed.action) return parsed.action;
      return Object.entries(parsed)
        .slice(0, 2)
        .map(([k, v]) => `${k}: ${v}`)
        .join(' · ');
    } catch {
      return jsonStr;
    }
  };

  return (
    <div className="flex-1 flex flex-col h-full bg-slate-50 dark:bg-slate-950 overflow-hidden">
      {/* Page Header */}
      <div className="bg-white dark:bg-slate-900 border-b border-slate-200 dark:border-slate-800 px-6 py-4 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
        <div>
          <div className="flex items-center gap-2">
            <ShieldCheck className="w-5 h-5 text-blue-700 dark:text-blue-400" />
            <h1 className="text-base font-semibold text-slate-900 dark:text-slate-100">
              Activity & Compliance Audit Log
            </h1>
          </div>
          <p className="text-xs text-slate-500 dark:text-slate-400 mt-0.5">
            Immutable tracking of approvals, automated actions, supplier orders, and security events.
          </p>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={fetchLogs}
            disabled={loading}
            className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium text-slate-700 dark:text-slate-200 bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-md hover:bg-slate-50 dark:hover:bg-slate-700 transition cursor-pointer disabled:opacity-50"
          >
            <RefreshCw className={`w-3.5 h-3.5 text-slate-500 ${loading ? 'animate-spin' : ''}`} />
            <span>Refresh</span>
          </button>
        </div>
      </div>

      {/* Filter / Search Bar */}
      <div className="bg-white dark:bg-slate-900 border-b border-slate-200 dark:border-slate-800 px-6 py-2.5 flex flex-wrap items-center justify-between gap-3">
        <div className="flex items-center gap-2">
          <Filter className="w-3.5 h-3.5 text-slate-400" />
          <span className="text-xs text-slate-500 dark:text-slate-400">Filter entity:</span>
          <div className="flex items-center gap-1 bg-slate-100 dark:bg-slate-800 p-0.5 rounded-md text-xs">
            {['ALL', 'DRAFT', 'MESSAGE', 'STOCK_ORDER', 'SYSTEM'].map((filter) => (
              <button
                key={filter}
                onClick={() => setEntityFilter(filter)}
                className={`px-2.5 py-1 rounded text-xs font-medium transition cursor-pointer ${
                  entityFilter === filter
                    ? 'bg-white dark:bg-slate-900 text-slate-900 dark:text-slate-100 shadow-sm'
                    : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-200'
                }`}
              >
                {filter === 'ALL' ? 'All Events' : filter.replace('_', ' ')}
              </button>
            ))}
          </div>
        </div>

        <div className="relative min-w-[220px]">
          <Search className="w-3.5 h-3.5 text-slate-400 absolute left-2.5 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            placeholder="Search action, actor, details..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full text-xs pl-8 pr-3 py-1.5 rounded-md bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-slate-900 dark:text-slate-100 placeholder-slate-400 focus:outline-none focus:ring-1 focus:ring-blue-600"
          />
        </div>
      </div>

      {/* Main Table Content */}
      <div className="flex-1 overflow-auto p-6">
        <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-lg shadow-sm overflow-hidden">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="border-b border-slate-200 dark:border-slate-800 bg-slate-50/75 dark:bg-slate-800/50 text-[11px] font-semibold text-slate-600 dark:text-slate-400 uppercase tracking-wider">
                <th className="py-2.5 px-4 w-44">Timestamp</th>
                <th className="py-2.5 px-4 w-36">Action</th>
                <th className="py-2.5 px-4 w-36">Entity</th>
                <th className="py-2.5 px-4 w-44">Actor</th>
                <th className="py-2.5 px-4">Event Summary</th>
                <th className="py-2.5 px-4 w-20 text-right">Details</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 dark:divide-slate-800 text-xs">
              {loading && logs.length === 0 ? (
                <tr>
                  <td colSpan={6} className="py-12 text-center text-slate-400">
                    <RefreshCw className="w-5 h-5 animate-spin mx-auto mb-2 text-slate-400" />
                    <span>Loading audit records...</span>
                  </td>
                </tr>
              ) : filteredLogs.length === 0 ? (
                <tr>
                  <td colSpan={6} className="py-12 text-center text-slate-400">
                    <FileText className="w-6 h-6 mx-auto mb-2 opacity-40" />
                    <span>No audit log records match the current filters.</span>
                  </td>
                </tr>
              ) : (
                filteredLogs.map((log) => (
                  <tr
                    key={log.id}
                    onClick={() => setSelectedLog(log)}
                    className="hover:bg-slate-50/75 dark:hover:bg-slate-800/40 cursor-pointer transition-colors"
                  >
                    <td className="py-3 px-4 text-slate-600 dark:text-slate-400 whitespace-nowrap">
                      <div className="flex items-center gap-1.5">
                        <Clock className="w-3.5 h-3.5 text-slate-400" />
                        <span className="tabular-nums">{formatTimestamp(log.timestamp)}</span>
                      </div>
                    </td>
                    <td className="py-3 px-4 whitespace-nowrap">
                      {getActionBadge(log.action)}
                    </td>
                    <td className="py-3 px-4 font-mono text-[11px] text-slate-800 dark:text-slate-200 whitespace-nowrap">
                      {log.entity_type} #{log.entity_id}
                    </td>
                    <td className="py-3 px-4 whitespace-nowrap">
                      {getActorPill(log.actor_type, log.actor_id)}
                    </td>
                    <td className="py-3 px-4 text-slate-600 dark:text-slate-300 max-w-md truncate">
                      {formatDetailsPreview(log.details_json)}
                    </td>
                    <td className="py-3 px-4 text-right">
                      <button
                        onClick={(e) => {
                          e.stopPropagation();
                          setSelectedLog(log);
                        }}
                        className="p-1 rounded text-slate-400 hover:text-slate-700 dark:hover:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-800 transition"
                        title="View raw JSON"
                      >
                        <Code className="w-3.5 h-3.5" />
                      </button>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>

      {/* Raw Payload Drawer / Modal */}
      {selectedLog && (
        <div className="fixed inset-0 bg-slate-900/50 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-lg shadow-xl w-full max-w-xl overflow-hidden animate-in fade-in-50 zoom-in-95 duration-150">
            <div className="flex items-center justify-between px-5 py-3.5 border-b border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-800/50">
              <div className="flex items-center gap-2">
                <Code className="w-4 h-4 text-blue-700 dark:text-blue-400" />
                <h3 className="text-sm font-semibold text-slate-900 dark:text-slate-100">
                  Audit Record #{selectedLog.id} Detail
                </h3>
              </div>
              <button
                onClick={() => setSelectedLog(null)}
                className="p-1 rounded text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-800"
              >
                <X className="w-4 h-4" />
              </button>
            </div>

            <div className="p-5 space-y-4 text-xs">
              <div className="grid grid-cols-2 gap-3 pb-3 border-b border-slate-100 dark:border-slate-800">
                <div>
                  <span className="text-slate-400 block text-[11px]">Action</span>
                  <span className="font-semibold text-slate-800 dark:text-slate-200">{selectedLog.action}</span>
                </div>
                <div>
                  <span className="text-slate-400 block text-[11px]">Entity Target</span>
                  <span className="font-mono text-slate-800 dark:text-slate-200">{selectedLog.entity_type} #{selectedLog.entity_id}</span>
                </div>
                <div>
                  <span className="text-slate-400 block text-[11px]">Actor</span>
                  <span className="text-slate-800 dark:text-slate-200">{selectedLog.actor_id} ({selectedLog.actor_type})</span>
                </div>
                <div>
                  <span className="text-slate-400 block text-[11px]">Timestamp</span>
                  <span className="tabular-nums text-slate-800 dark:text-slate-200">{selectedLog.timestamp}</span>
                </div>
              </div>

              <div>
                <span className="text-slate-500 dark:text-slate-400 font-medium block mb-1.5 text-[11px]">
                  Raw Details JSON Payload
                </span>
                <pre className="bg-slate-900 text-slate-100 p-3.5 rounded-md font-mono text-[11px] overflow-x-auto leading-relaxed max-h-60 border border-slate-800">
                  {selectedLog.details_json
                    ? (() => {
                        try {
                          return JSON.stringify(JSON.parse(selectedLog.details_json), null, 2);
                        } catch {
                          return selectedLog.details_json;
                        }
                      })()
                    : 'null'}
                </pre>
              </div>
            </div>

            <div className="px-5 py-3 border-t border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-800/30 flex justify-end">
              <button
                onClick={() => setSelectedLog(null)}
                className="px-4 py-1.5 rounded bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-xs font-medium text-slate-700 dark:text-slate-200 hover:bg-slate-50 cursor-pointer"
              >
                Close
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
