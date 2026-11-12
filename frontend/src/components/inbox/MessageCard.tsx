import React from 'react';
import type { InboundMessage } from '../../types';

interface MessageCardProps {
  message: InboundMessage;
  isSelected: boolean;
  onSelect: () => void;
}

export const MessageCard: React.FC<MessageCardProps> = ({
  message,
  isSelected,
  onSelect,
}) => {
  // Compute Avatar Initials
  const getInitials = (address: string) => {
    const raw = address.split('@')[0].replace(/[._-]/g, ' ');
    const parts = raw.trim().split(' ');
    if (parts.length >= 2) {
      return (parts[0][0] + parts[1][0]).toUpperCase();
    }
    return raw.slice(0, 2).toUpperCase();
  };

  // Human relative time
  const getRelativeTime = (isoString: string) => {
    const diffMs = new Date().getTime() - new Date(isoString).getTime();
    const diffMins = Math.floor(diffMs / (1000 * 60));
    if (diffMins < 1) return 'Just now';
    if (diffMins < 60) return `${diffMins}m ago`;
    const diffHours = Math.floor(diffMins / 60);
    if (diffHours < 24) return `${diffHours}h ago`;
    return `${Math.floor(diffHours / 24)}d ago`;
  };

  // Subtle intent label
  const getIntentLabel = (intent: string) => {
    switch (intent) {
      case 'price_quote':
        return 'Quote';
      case 'bulk_order':
        return 'Bulk order';
      case 'stock_inquiry':
        return 'Stock query';
      case 'order_status':
        return 'Tracking';
      case 'complaint':
        return 'Complaint';
      case 'refund':
        return 'Refund';
      default:
        return 'General';
    }
  };

  const isPending = message.processing_status === 'drafted' || message.processing_status === 'received';

  return (
    <div
      onClick={onSelect}
      className={`px-3 py-2.5 rounded-md transition cursor-pointer border-l-2 text-left ${
        isSelected
          ? 'bg-blue-50/70 dark:bg-blue-950/30 border-blue-600 text-slate-900 dark:text-slate-100'
          : 'border-transparent hover:bg-slate-100/70 dark:hover:bg-slate-800/60 text-slate-700 dark:text-slate-300'
      }`}
    >
      <div className="flex items-center justify-between gap-2 mb-1">
        <div className="flex items-center gap-2 min-w-0">
          {/* Status dot */}
          <span
            className={`w-1.5 h-1.5 rounded-full shrink-0 ${
              message.prompt_injection_detected
                ? 'bg-red-500'
                : isPending
                ? 'bg-amber-500'
                : 'bg-slate-300 dark:bg-slate-700'
            }`}
          />

          {/* Avatar circle */}
          <div className="w-5 h-5 rounded-full bg-slate-200 dark:bg-slate-800 text-slate-700 dark:text-slate-300 text-[10px] font-medium flex items-center justify-center shrink-0">
            {getInitials(message.sender_address)}
          </div>

          <span className="font-medium text-xs truncate text-slate-900 dark:text-slate-100">
            {message.sender_address.split('@')[0]}
          </span>
        </div>

        <span className="text-[11px] text-slate-400 shrink-0 tabular-nums">
          {getRelativeTime(message.received_at)}
        </span>
      </div>

      <div className="text-xs font-medium text-slate-800 dark:text-slate-200 truncate mb-0.5 pl-3.5">
        {message.subject || 'Customer Inquiry'}
      </div>

      <div className="flex items-center justify-between gap-2 pl-3.5 mt-1">
        <p className="text-[11px] text-slate-500 dark:text-slate-400 truncate max-w-[200px]">
          {message.raw_text}
        </p>

        <span className="text-[10px] text-slate-500 bg-slate-100 dark:bg-slate-800 px-1.5 py-0.2 rounded font-normal shrink-0">
          {getIntentLabel(message.detected_intent)}
        </span>
      </div>
    </div>
  );
};
