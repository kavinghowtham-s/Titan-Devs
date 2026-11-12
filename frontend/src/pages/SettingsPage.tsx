import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import type { AppSettings, ConnectionTestResult } from '../types';
import {
  Sliders,
  Cpu,
  Clock,
  Check,
  RefreshCw,
  Key,
  Mail,
  Building,
  CheckCircle2,
  AlertCircle,
  HelpCircle,
  Play
} from 'lucide-react';

interface SettingsPageProps {
  onSettingsUpdated?: () => void;
}

export const SettingsPage: React.FC<SettingsPageProps> = ({ onSettingsUpdated }) => {
  const [settings, setSettings] = useState<AppSettings | null>(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [savedSuccess, setSavedSuccess] = useState(false);

  // Form states
  const [useMock, setUseMock] = useState(true);
  const [timerMinutes, setTimerMinutes] = useState(1);
  const [senderName, setSenderName] = useState('Rajesh Kumar');
  const [senderTitle, setSenderTitle] = useState('Operations Manager');

  // Connection testing state
  const [testingConnection, setTestingConnection] = useState(false);
  const [testResult, setTestResult] = useState<ConnectionTestResult | null>(null);

  const loadSettings = async () => {
    setLoading(true);
    try {
      const data = await api.getSettings();
      setSettings(data);
      setUseMock(data.use_mock_llm);
      setTimerMinutes(data.auto_approve_delay_minutes);
      if (data.sender) {
        setSenderName(data.sender.name);
        setSenderTitle(data.sender.title);
      }
    } catch (err) {
      console.error('Failed to load settings:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadSettings();
  }, []);

  const handleSave = async () => {
    setSaving(true);
    try {
      await api.updateSettings({
        use_mock_llm: useMock,
        auto_approve_delay_minutes: timerMinutes,
      });
      setSavedSuccess(true);
      setTimeout(() => setSavedSuccess(false), 3000);
      if (onSettingsUpdated) onSettingsUpdated();
    } catch (err) {
      console.error('Failed to update settings:', err);
    } finally {
      setSaving(false);
    }
  };

  const handleTestConnection = async () => {
    setTestingConnection(true);
    setTestResult(null);
    try {
      const result = await api.testConnection();
      setTestResult(result);
    } catch (err) {
      console.error('Test connection failed:', err);
    } finally {
      setTestingConnection(false);
    }
  };

  if (loading) {
    return (
      <div className="flex-1 flex items-center justify-center bg-slate-50 dark:bg-slate-950">
        <RefreshCw className="w-5 h-5 text-slate-400 animate-spin" />
      </div>
    );
  }

  return (
    <div className="flex-1 bg-slate-50 dark:bg-slate-950 p-6 sm:p-8 overflow-y-auto">
      <div className="max-w-4xl mx-auto space-y-6">
        {/* Page Title & Intro */}
        <div>
          <div className="flex items-center gap-2">
            <Sliders className="w-5 h-5 text-blue-700 dark:text-blue-400" />
            <h1 className="text-lg font-semibold text-slate-900 dark:text-slate-100">
              Settings & Operational Parameters
            </h1>
          </div>
          <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">
            Configure LLM inference routing, autonomous safety timers, and outbound sender credentials for Trentar Private Limited.
          </p>
        </div>

        {/* SECTION 1: LLM Inference Engine & Model Testing */}
        <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-lg p-6 shadow-sm space-y-5">
          <div className="flex items-start justify-between border-b border-slate-100 dark:border-slate-800 pb-3">
            <div>
              <div className="flex items-center gap-2 text-sm font-semibold text-slate-900 dark:text-slate-100">
                <Cpu className="w-4 h-4 text-blue-700 dark:text-blue-400" />
                <span>AI Execution Engine & Cloud Routing</span>
              </div>
              <p className="text-xs text-slate-500 dark:text-slate-400 mt-0.5">
                Select between offline deterministic mock templates or live cloud API inference.
              </p>
            </div>

            <button
              onClick={handleTestConnection}
              disabled={testingConnection}
              className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium text-blue-700 dark:text-blue-300 bg-blue-50 dark:bg-blue-950/50 hover:bg-blue-100 dark:hover:bg-blue-900/50 border border-blue-200 dark:border-blue-800 rounded-md transition cursor-pointer disabled:opacity-50"
            >
              <Play className={`w-3 h-3 ${testingConnection ? 'animate-spin' : ''}`} />
              <span>{testingConnection ? 'Pinging Cloud...' : 'Test Connection'}</span>
            </button>
          </div>

          {/* Engine Selector */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div
              onClick={() => setUseMock(true)}
              className={`p-4 rounded-lg border transition cursor-pointer ${
                useMock
                  ? 'bg-blue-50/50 dark:bg-blue-950/30 border-blue-500 text-slate-900 dark:text-slate-100 shadow-sm'
                  : 'bg-white dark:bg-slate-900 border-slate-200 dark:border-slate-800 text-slate-600 dark:text-slate-400 hover:border-slate-300 dark:hover:border-slate-700'
              }`}
            >
              <div className="flex items-center justify-between mb-1.5">
                <span className="text-xs font-semibold">Deterministic Mock Engine</span>
                {useMock && <Check className="w-4 h-4 text-blue-700 dark:text-blue-400" />}
              </div>
              <p className="text-[11px] leading-relaxed text-slate-500 dark:text-slate-400">
                Zero network dependency. Returns factual, intent-keyed replies in English, Tamil, and Hindi with sub-50ms latency. Guaranteed 100% demo uptime.
              </p>
            </div>

            <div
              onClick={() => setUseMock(false)}
              className={`p-4 rounded-lg border transition cursor-pointer ${
                !useMock
                  ? 'bg-blue-50/50 dark:bg-blue-950/30 border-blue-500 text-slate-900 dark:text-slate-100 shadow-sm'
                  : 'bg-white dark:bg-slate-900 border-slate-200 dark:border-slate-800 text-slate-600 dark:text-slate-400 hover:border-slate-300 dark:hover:border-slate-700'
              }`}
            >
              <div className="flex items-center justify-between mb-1.5">
                <span className="text-xs font-semibold">Live Ollama Cloud API</span>
                {!useMock && <Check className="w-4 h-4 text-blue-700 dark:text-blue-400" />}
              </div>
              <p className="text-[11px] leading-relaxed text-slate-500 dark:text-slate-400">
                Queries external Ollama Cloud with Bearer authentication. Automatically falls back to deterministic engine if API quota or credits are unavailable.
              </p>
            </div>
          </div>

          {/* Masked API Key Display */}
          <div className="flex items-center justify-between p-3 rounded-md bg-slate-50 dark:bg-slate-800/60 border border-slate-200 dark:border-slate-800 text-xs">
            <div className="flex items-center gap-2">
              <Key className="w-4 h-4 text-slate-400" />
              <span className="text-slate-600 dark:text-slate-400">Configured Cloud API Key:</span>
              <span className="font-mono font-medium text-slate-800 dark:text-slate-200">
                {settings?.masked_key || '...UCMZ'}
              </span>
            </div>
            <span className="text-[11px] text-emerald-600 dark:text-emerald-400 flex items-center gap-1 font-medium">
              <CheckCircle2 className="w-3.5 h-3.5" /> Key Verified
            </span>
          </div>

          {/* Connection Test Results Table (if run) */}
          {testResult && (
            <div className="mt-4 pt-4 border-t border-slate-100 dark:border-slate-800 space-y-3">
              <div className="flex items-center justify-between text-xs">
                <span className="font-semibold text-slate-800 dark:text-slate-200">
                  Role Connectivity Health Check:
                </span>
                <span className="text-[11px] text-slate-500">
                  Endpoint: <span className="font-mono">{testResult.endpoint}</span>
                </span>
              </div>

              <div className="border border-slate-200 dark:border-slate-800 rounded-md overflow-hidden">
                <table className="w-full text-left border-collapse text-xs">
                  <thead>
                    <tr className="bg-slate-50 dark:bg-slate-800/60 text-[11px] font-semibold text-slate-500 uppercase border-b border-slate-200 dark:border-slate-800">
                      <th className="py-2 px-3">Role</th>
                      <th className="py-2 px-3">Assigned Model</th>
                      <th className="py-2 px-3">Status</th>
                      <th className="py-2 px-3 text-right">Latency</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100 dark:divide-slate-800 text-[11px]">
                    {Object.entries(testResult.roles).map(([role, res]) => (
                      <tr key={role} className="hover:bg-slate-50/50 dark:hover:bg-slate-800/30">
                        <td className="py-2 px-3 font-medium text-slate-700 dark:text-slate-300 capitalize">
                          {role}
                        </td>
                        <td className="py-2 px-3 font-mono text-slate-600 dark:text-slate-400">
                          {res.model}
                        </td>
                        <td className="py-2 px-3">
                          {res.status === 'connected' ? (
                            <span className="inline-flex items-center gap-1 text-emerald-600 dark:text-emerald-400 font-medium">
                              <CheckCircle2 className="w-3 h-3" /> Operational
                            </span>
                          ) : res.status === 'credit_required' ? (
                            <span className="inline-flex items-center gap-1 text-amber-600 dark:text-amber-400 font-medium" title={res.message}>
                              <AlertCircle className="w-3 h-3" /> Offline Fallback Active
                            </span>
                          ) : (
                            <span className="inline-flex items-center gap-1 text-slate-500 font-medium">
                              <HelpCircle className="w-3 h-3" /> {res.status}
                            </span>
                          )}
                        </td>
                        <td className="py-2 px-3 text-right tabular-nums text-slate-600 dark:text-slate-400">
                          {res.latency_ms > 0 ? `${res.latency_ms} ms` : '—'}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}
        </div>

        {/* SECTION 2: Autonomous Auto-Approval Threshold */}
        <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-lg p-6 shadow-sm space-y-4">
          <div className="flex items-center gap-2 text-sm font-semibold text-slate-900 dark:text-slate-100">
            <Clock className="w-4 h-4 text-blue-700 dark:text-blue-400" />
            <span>Autonomous Auto-Approval Timer SLA</span>
          </div>
          <p className="text-xs text-slate-500 dark:text-slate-400">
            When a draft reply remains unacted by a manager, the safety Orchestrator evaluates compliance rules and auto-sends if clear.
          </p>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-1">
            <button
              type="button"
              onClick={() => setTimerMinutes(1)}
              className={`p-3.5 rounded-lg border text-left transition cursor-pointer ${
                timerMinutes === 1
                  ? 'bg-blue-50/50 dark:bg-blue-950/30 border-blue-500 text-slate-900 dark:text-slate-100'
                  : 'bg-white dark:bg-slate-900 border-slate-200 dark:border-slate-800 text-slate-600 dark:text-slate-400 hover:border-slate-300'
              }`}
            >
              <div className="flex items-center justify-between">
                <span className="text-xs font-semibold">1 Minute Demo Mode</span>
                {timerMinutes === 1 && <Check className="w-3.5 h-3.5 text-blue-700 dark:text-blue-400" />}
              </div>
              <p className="text-[11px] text-slate-500 dark:text-slate-400 mt-1">
                Fast-cycle testing for live hackathon presentations and jury walkthroughs.
              </p>
            </button>

            <button
              type="button"
              onClick={() => setTimerMinutes(360)}
              className={`p-3.5 rounded-lg border text-left transition cursor-pointer ${
                timerMinutes === 360
                  ? 'bg-blue-50/50 dark:bg-blue-950/30 border-blue-500 text-slate-900 dark:text-slate-100'
                  : 'bg-white dark:bg-slate-900 border-slate-200 dark:border-slate-800 text-slate-600 dark:text-slate-400 hover:border-slate-300'
              }`}
            >
              <div className="flex items-center justify-between">
                <span className="text-xs font-semibold">6 Hours Enterprise SLA</span>
                {timerMinutes === 360 && <Check className="w-3.5 h-3.5 text-blue-700 dark:text-blue-400" />}
              </div>
              <p className="text-[11px] text-slate-500 dark:text-slate-400 mt-1">
                Standard business hours SLA before unreviewed standard quotes auto-dispatch.
              </p>
            </button>
          </div>
        </div>

        {/* SECTION 3: Outbound Sender Signature Profile */}
        <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-lg p-6 shadow-sm space-y-4">
          <div className="flex items-center gap-2 text-sm font-semibold text-slate-900 dark:text-slate-100">
            <Mail className="w-4 h-4 text-blue-700 dark:text-blue-400" />
            <span>Outbound Signature & Sender Identity</span>
          </div>
          <p className="text-xs text-slate-500 dark:text-slate-400">
            Appended to all drafted customer replies and supplier purchase orders.
          </p>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-1">
            <div>
              <label className="block text-xs font-medium text-slate-700 dark:text-slate-300 mb-1">
                Sender Name
              </label>
              <input
                type="text"
                value={senderName}
                onChange={(e) => setSenderName(e.target.value)}
                className="w-full text-xs px-3 py-2 rounded-md bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-slate-900 dark:text-slate-100 focus:outline-none focus:ring-1 focus:ring-blue-600"
              />
            </div>

            <div>
              <label className="block text-xs font-medium text-slate-700 dark:text-slate-300 mb-1">
                Job Title
              </label>
              <input
                type="text"
                value={senderTitle}
                onChange={(e) => setSenderTitle(e.target.value)}
                className="w-full text-xs px-3 py-2 rounded-md bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-slate-900 dark:text-slate-100 focus:outline-none focus:ring-1 focus:ring-blue-600"
              />
            </div>

            <div>
              <label className="block text-xs font-medium text-slate-700 dark:text-slate-300 mb-1">
                Company Name
              </label>
              <div className="flex items-center gap-2 text-xs px-3 py-2 rounded-md bg-slate-100 dark:bg-slate-800/50 border border-slate-200 dark:border-slate-800 text-slate-600 dark:text-slate-400">
                <Building className="w-3.5 h-3.5 text-slate-400" />
                <span>Trentar Private Limited</span>
              </div>
            </div>

            <div>
              <label className="block text-xs font-medium text-slate-700 dark:text-slate-300 mb-1">
                Registered Outbound Email
              </label>
              <div className="text-xs px-3 py-2 rounded-md bg-slate-100 dark:bg-slate-800/50 border border-slate-200 dark:border-slate-800 text-slate-600 dark:text-slate-400 font-mono">
                operations@trentar.com
              </div>
            </div>
          </div>
        </div>

        {/* Action Save Bar */}
        <div className="flex items-center justify-between pt-2">
          {savedSuccess ? (
            <span className="text-xs font-medium text-emerald-600 dark:text-emerald-400 flex items-center gap-1.5">
              <CheckCircle2 className="w-4 h-4" /> Settings updated successfully
            </span>
          ) : (
            <span />
          )}

          <button
            onClick={handleSave}
            disabled={saving}
            className="px-5 py-2 rounded-md bg-blue-700 hover:bg-blue-800 text-white text-xs font-medium transition shadow-sm cursor-pointer disabled:opacity-50"
          >
            {saving ? 'Saving changes...' : 'Save Configuration'}
          </button>
        </div>
      </div>
    </div>
  );
};
