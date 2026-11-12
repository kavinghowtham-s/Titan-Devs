import React from 'react';
import type { MessageDetailResponse } from '../../types';
import { User, Building, MapPin, Mail, Phone, PackageCheck, AlertTriangle, ExternalLink } from 'lucide-react';

interface ContextPanelProps {
  detail: MessageDetailResponse;
  onNavigateToStock?: () => void;
}

export const ContextPanel: React.FC<ContextPanelProps> = ({ detail, onNavigateToStock }) => {
  const { customer, stock_order, message } = detail;

  return (
    <div className="w-80 bg-white dark:bg-slate-900 border-l border-slate-200 dark:border-slate-800 flex flex-col h-full overflow-y-auto p-4 space-y-5 text-xs text-slate-700 dark:text-slate-300 transition-colors">
      {/* 1. Customer Information */}
      <div>
        <div className="text-[11px] font-semibold text-slate-400 dark:text-slate-500 uppercase tracking-wider mb-2.5">
          Customer
        </div>
        <div className="bg-slate-50 dark:bg-slate-800/60 border border-slate-200/80 dark:border-slate-700/60 rounded-lg p-3 space-y-2">
          <div className="flex items-center gap-2">
            <User className="w-4 h-4 text-slate-400" />
            <span className="font-semibold text-slate-900 dark:text-slate-100">
              {customer?.name || message.sender_address.split('@')[0]}
            </span>
          </div>

          {customer?.company_name && (
            <div className="flex items-center gap-2 text-slate-600 dark:text-slate-400">
              <Building className="w-3.5 h-3.5 text-slate-400" />
              <span>{customer.company_name}</span>
            </div>
          )}

          {customer?.city && (
            <div className="flex items-center gap-2 text-slate-600 dark:text-slate-400">
              <MapPin className="w-3.5 h-3.5 text-slate-400" />
              <span>{customer.city}, {customer.state}</span>
            </div>
          )}

          <div className="flex items-center gap-2 text-slate-600 dark:text-slate-400 truncate">
            <Mail className="w-3.5 h-3.5 text-slate-400" />
            <span className="truncate">{message.sender_address}</span>
          </div>

          {customer?.phone && (
            <div className="flex items-center gap-2 text-slate-600 dark:text-slate-400">
              <Phone className="w-3.5 h-3.5 text-slate-400" />
              <span className="tabular-nums">{customer.phone}</span>
            </div>
          )}
        </div>
      </div>

      {/* 2. Stock & Inventory Context */}
      <div>
        <div className="text-[11px] font-semibold text-slate-400 dark:text-slate-500 uppercase tracking-wider mb-2.5">
          Inventory Status
        </div>

        {stock_order ? (
          <div className="bg-amber-50 dark:bg-amber-950/30 border border-amber-200 dark:border-amber-900/60 rounded-lg p-3 space-y-2">
            <div className="flex items-center gap-1.5 text-amber-800 dark:text-amber-300 font-semibold">
              <AlertTriangle className="w-4 h-4 text-amber-600 dark:text-amber-400 shrink-0" />
              <span>Inventory Shortfall</span>
            </div>

            <p className="text-[11px] text-amber-800/90 dark:text-amber-300/80 leading-relaxed">
              Order exceeds warehouse stock. An automated purchase order was prepared for supplier fulfillment.
            </p>

            <div className="pt-2 border-t border-amber-200/80 dark:border-amber-900/60 space-y-1 text-[11px]">
              <div className="flex justify-between">
                <span className="text-amber-700 dark:text-amber-400">PO Number:</span>
                <span className="font-mono font-medium text-amber-900 dark:text-amber-200">{stock_order.order_number}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-amber-700 dark:text-amber-400">Estimated Cost:</span>
                <span className="font-medium text-amber-900 dark:text-amber-200 tabular-nums">
                  ₹{stock_order.total_estimated_cost.toLocaleString()}
                </span>
              </div>
            </div>

            {onNavigateToStock && (
              <button
                onClick={onNavigateToStock}
                className="w-full mt-1 pt-1 text-center text-xs text-blue-700 dark:text-blue-400 hover:underline flex items-center justify-center gap-1 cursor-pointer"
              >
                <span>View Supplier Orders</span>
                <ExternalLink className="w-3 h-3" />
              </button>
            )}
          </div>
        ) : (
          <div className="bg-slate-50 dark:bg-slate-800/60 border border-slate-200/80 dark:border-slate-700/60 rounded-lg p-3 space-y-1.5">
            <div className="flex items-center gap-1.5 text-emerald-700 dark:text-emerald-400 font-medium">
              <PackageCheck className="w-4 h-4 text-emerald-600 dark:text-emerald-400" />
              <span>Sufficient Warehouse Stock</span>
            </div>
            <p className="text-[11px] text-slate-500 dark:text-slate-400 leading-relaxed">
              Requested items are fully covered by in-hand warehouse inventory. Ready for immediate dispatch upon approval.
            </p>
          </div>
        )}
      </div>

      {/* 3. Operational Routing Metadata */}
      <div>
        <div className="text-[11px] font-semibold text-slate-400 dark:text-slate-500 uppercase tracking-wider mb-2">
          Routing details
        </div>
        <div className="space-y-1.5 text-[11px] text-slate-500 dark:text-slate-400">
          <div className="flex justify-between">
            <span>Channel:</span>
            <span className="text-slate-800 dark:text-slate-200 capitalize">{message.channel}</span>
          </div>
          <div className="flex justify-between">
            <span>Language:</span>
            <span className="text-slate-800 dark:text-slate-200 uppercase">{message.language}</span>
          </div>
          <div className="flex justify-between">
            <span>Priority:</span>
            <span className="text-slate-800 dark:text-slate-200 capitalize">{message.priority}</span>
          </div>
          <div className="flex justify-between">
            <span>Received:</span>
            <span className="text-slate-800 dark:text-slate-200 tabular-nums">
              {new Date(message.received_at).toLocaleDateString()}
            </span>
          </div>
        </div>
      </div>
    </div>
  );
};
