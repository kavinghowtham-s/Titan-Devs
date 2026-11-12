import React, { useState } from 'react';
import { api } from '../../services/api';
import {
  Sun,
  Moon,
  ChevronDown,
  CheckCircle2,
  Sparkles,
  SendHorizontal
} from 'lucide-react';

interface TopNavProps {
  onMessageCreated?: () => void;
  mockMode: boolean;
  darkMode: boolean;
  onToggleDarkMode: () => void;
  pendingCount: number;
}

export const TopNav: React.FC<TopNavProps> = ({
  onMessageCreated,
  mockMode,
  darkMode,
  onToggleDarkMode,
  pendingCount,
}) => {
  const [simulating, setSimulating] = useState(false);
  const [toast, setToast] = useState<string | null>(null);

  const handleSimulate = async (scenarioId: string, label: string) => {
    setSimulating(true);
    try {
      await api.simulateBatch([scenarioId]);
      setToast(`Received: ${label}`);
      setTimeout(() => setToast(null), 3000);
      if (onMessageCreated) onMessageCreated();
    } catch (err) {
      console.error(err);
    } finally {
      setSimulating(false);
    }
  };

  return (
    <header className="h-14 bg-white dark:bg-slate-900 border-b border-slate-200 dark:border-slate-800 px-5 flex items-center justify-between sticky top-0 z-40 transition-colors">
      {/* Brand & Workspace Title */}
      <div className="flex items-center gap-3">
        <div className="w-7 h-7 rounded bg-blue-700 text-white flex items-center justify-center font-bold text-xs shadow-sm">
          T
        </div>
        <div className="flex items-center gap-2">
          <span className="font-semibold text-sm text-slate-900 dark:text-slate-100 tracking-tight">
            Trentar OpsPilot
          </span>
          <span className="text-slate-300 dark:text-slate-700">/</span>
          <span className="text-xs text-slate-500 dark:text-slate-400 font-normal">
            Operations
          </span>
        </div>
      </div>

      {/* Center Operational Status */}
      <div className="hidden md:flex items-center gap-5 text-xs text-slate-600 dark:text-slate-400">
        <div className="flex items-center gap-2">
          <span className="w-2 h-2 rounded-full bg-emerald-500" />
          <span>System Healthy</span>
        </div>

        <div className="text-slate-300 dark:text-slate-700">|</div>

        <div className="flex items-center gap-1.5">
          <span className="font-medium text-slate-900 dark:text-slate-200 tabular-nums">
            {pendingCount}
          </span>
          <span>pending approvals</span>
        </div>

        <div className="text-slate-300 dark:text-slate-700">|</div>

        {/* Quiet AI Mode Indicator */}
        <div className="flex items-center gap-1.5">
          <Sparkles className="w-3.5 h-3.5 text-blue-600 dark:text-blue-400" />
          <span className="text-xs font-medium text-slate-700 dark:text-slate-300">
            {mockMode ? 'Demo mode (Offline)' : 'Live AI (Ollama Cloud)'}
          </span>
        </div>
      </div>

      {/* Right Actions */}
      <div className="flex items-center gap-2.5">
        {toast && (
          <div className="hidden sm:flex items-center gap-1.5 text-xs text-emerald-700 bg-emerald-50 border border-emerald-200 px-2.5 py-1 rounded dark:bg-emerald-950/60 dark:text-emerald-300 dark:border-emerald-800">
            <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600" />
            <span>{toast}</span>
          </div>
        )}

        {/* Inbound Simulator Menu */}
        <div className="relative group">
          <button
            disabled={simulating}
            className="flex items-center gap-1.5 text-xs font-medium text-slate-700 dark:text-slate-300 bg-slate-100 hover:bg-slate-200 dark:bg-slate-800 dark:hover:bg-slate-700 px-3 py-1.5 rounded transition cursor-pointer disabled:opacity-50"
          >
            <SendHorizontal className="w-3.5 h-3.5 text-slate-500" />
            <span>{simulating ? 'Simulating...' : 'Simulate message'}</span>
            <ChevronDown className="w-3 h-3 opacity-60 ml-0.5" />
          </button>

          <div className="absolute right-0 mt-1 w-60 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-lg shadow-lg py-1 hidden group-hover:block z-50">
            <div className="px-3 py-1 text-[11px] font-medium text-slate-400 uppercase tracking-wider">
              Sample scenarios
            </div>
            <button
              onClick={() => handleSimulate('M01', 'Quotation request (Vikram Patel)')}
              className="w-full text-left px-3 py-1.5 text-xs text-slate-700 dark:text-slate-200 hover:bg-slate-50 dark:hover:bg-slate-800 cursor-pointer flex items-center justify-between"
            >
              <span>M01: Flight controller quote</span>
              <span className="text-[10px] text-slate-400">Quote</span>
            </button>
            <button
              onClick={() => handleSimulate('M02', 'Bulk order with shortfall (Sneha Reddy)')}
              className="w-full text-left px-3 py-1.5 text-xs text-slate-700 dark:text-slate-200 hover:bg-slate-50 dark:hover:bg-slate-800 cursor-pointer flex items-center justify-between"
            >
              <span>M02: Bulk motors (Shortfall)</span>
              <span className="text-[10px] text-amber-600 dark:text-amber-400">Shortfall</span>
            </button>
            <button
              onClick={() => handleSimulate('M03', 'Tamil hexacopter inquiry')}
              className="w-full text-left px-3 py-1.5 text-xs text-slate-700 dark:text-slate-200 hover:bg-slate-50 dark:hover:bg-slate-800 cursor-pointer flex items-center justify-between"
            >
              <span>M03: Tamil inquiry</span>
              <span className="text-[10px] text-slate-400">Tamil</span>
            </button>
            <button
              onClick={() => handleSimulate('M04', 'Hindi battery order')}
              className="w-full text-left px-3 py-1.5 text-xs text-slate-700 dark:text-slate-200 hover:bg-slate-50 dark:hover:bg-slate-800 cursor-pointer flex items-center justify-between"
            >
              <span>M04: Hindi battery order</span>
              <span className="text-[10px] text-slate-400">Hindi</span>
            </button>
            <button
              onClick={() => handleSimulate('M06', 'Hardware defect complaint')}
              className="w-full text-left px-3 py-1.5 text-xs text-slate-700 dark:text-slate-200 hover:bg-slate-50 dark:hover:bg-slate-800 cursor-pointer flex items-center justify-between"
            >
              <span>M06: Damaged RTK complaint</span>
              <span className="text-[10px] text-red-600 dark:text-red-400">Complaint</span>
            </button>
            <button
              onClick={() => handleSimulate('M09', 'Security prompt injection')}
              className="w-full text-left px-3 py-1.5 text-xs text-red-600 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-950/40 cursor-pointer flex items-center justify-between border-t border-slate-100 dark:border-slate-800"
            >
              <span>M09: Prompt injection attempt</span>
              <span className="text-[10px] text-red-500">Security</span>
            </button>
          </div>
        </div>

        {/* Dark/Light Mode Toggle */}
        <button
          onClick={onToggleDarkMode}
          className="p-1.5 rounded text-slate-500 hover:text-slate-800 dark:text-slate-400 dark:hover:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-800 transition cursor-pointer"
          title={darkMode ? 'Switch to light mode' : 'Switch to dark mode'}
        >
          {darkMode ? <Sun className="w-4 h-4" /> : <Moon className="w-4 h-4" />}
        </button>
      </div>
    </header>
  );
};
