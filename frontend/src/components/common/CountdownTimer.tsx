import React, { useState, useEffect } from 'react';
import { Clock, Check, AlertCircle } from 'lucide-react';

interface CountdownTimerProps {
  initialSeconds?: number;
  deadlineString: string;
  status: string;
  onExpire?: () => void;
}

export const CountdownTimer: React.FC<CountdownTimerProps> = ({
  initialSeconds,
  deadlineString,
  status,
  onExpire,
}) => {
  const calculateRemaining = () => {
    if (status !== 'pending') return 0;
    const deadline = new Date(deadlineString).getTime();
    const now = new Date().getTime();
    return Math.max(0, Math.floor((deadline - now) / 1000));
  };

  const [seconds, setSeconds] = useState<number>(() => {
    return initialSeconds !== undefined ? initialSeconds : calculateRemaining();
  });

  useEffect(() => {
    if (status !== 'pending') return;

    const interval = setInterval(() => {
      const remaining = calculateRemaining();
      setSeconds(remaining);
      if (remaining <= 0) {
        clearInterval(interval);
        if (onExpire) onExpire();
      }
    }, 1000);

    return () => clearInterval(interval);
  }, [deadlineString, status]);

  if (status === 'approved' || status === 'sent') {
    return (
      <span className="inline-flex items-center gap-1 text-xs text-emerald-700 bg-emerald-50 border border-emerald-200 px-2 py-0.5 rounded font-medium dark:bg-emerald-950/40 dark:text-emerald-400 dark:border-emerald-800">
        <Check className="w-3 h-3" /> Sent
      </span>
    );
  }

  if (status === 'auto_approved') {
    return (
      <span className="inline-flex items-center gap-1 text-xs text-teal-700 bg-teal-50 border border-teal-200 px-2 py-0.5 rounded font-medium dark:bg-teal-950/40 dark:text-teal-300 dark:border-teal-800">
        <Check className="w-3 h-3" /> Auto-approved
      </span>
    );
  }

  if (status === 'escalated') {
    return (
      <span className="inline-flex items-center gap-1 text-xs text-red-700 bg-red-50 border border-red-200 px-2 py-0.5 rounded font-medium dark:bg-red-950/40 dark:text-red-400 dark:border-red-800">
        <AlertCircle className="w-3 h-3" /> Needs manual review
      </span>
    );
  }

  if (status === 'rejected') {
    return (
      <span className="inline-flex items-center gap-1 text-xs text-slate-600 bg-slate-100 border border-slate-200 px-2 py-0.5 rounded font-medium dark:bg-slate-800 dark:text-slate-400 dark:border-slate-700">
        Rejected
      </span>
    );
  }

  // Active Pending State: calm, restrained format
  const mins = Math.floor(seconds / 60);
  const secs = seconds % 60;
  const timeFormatted = mins > 0 ? `${mins}m ${secs}s` : `${secs}s`;

  // Color threshold: subtle amber when < 20s, red when < 5s
  let textClass = 'text-slate-500 dark:text-slate-400';
  if (seconds <= 20 && seconds > 5) {
    textClass = 'text-amber-600 font-medium dark:text-amber-400';
  } else if (seconds <= 5) {
    textClass = 'text-red-600 font-semibold dark:text-red-400';
  }

  return (
    <div className={`inline-flex items-center gap-1.5 text-xs ${textClass}`}>
      <Clock className="w-3.5 h-3.5 opacity-70" />
      <span>Auto-sends in {timeFormatted}</span>
    </div>
  );
};
