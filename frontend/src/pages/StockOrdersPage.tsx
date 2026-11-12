import React, { useState, useEffect } from 'react';
import type { StockOrder } from '../types';
import { api } from '../services/api';
import {
  CheckCircle2,
  RefreshCw,
  Send,
  Check
} from 'lucide-react';

export const StockOrdersPage: React.FC = () => {
  const [orders, setOrders] = useState<StockOrder[]>([]);
  const [loading, setLoading] = useState(true);
  const [filterStatus, setFilterStatus] = useState<string>('all');
  const [selectedOrder, setSelectedOrder] = useState<StockOrder | null>(null);
  const [managerNotes, setManagerNotes] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [successToast, setSuccessToast] = useState<string | null>(null);

  const loadOrders = async () => {
    setLoading(true);
    try {
      const data = await api.getStockOrders();
      setOrders(data);
    } catch (err) {
      console.error('Failed to load stock orders:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadOrders();
  }, []);

  const handleApprove = async () => {
    if (!selectedOrder) return;
    setSubmitting(true);
    try {
      await api.approveStockOrder(selectedOrder.id, managerNotes);
      setSuccessToast(`Purchase Order ${selectedOrder.order_number} approved and dispatched!`);
      setTimeout(() => setSuccessToast(null), 3000);
      setSelectedOrder(null);
      setManagerNotes('');
      loadOrders();
    } catch (err) {
      console.error('Failed to approve stock order:', err);
    } finally {
      setSubmitting(false);
    }
  };

  const filteredOrders = orders.filter((o) => {
    if (filterStatus === 'all') return true;
    return o.status === filterStatus;
  });

  return (
    <div className="flex-1 bg-slate-50 dark:bg-slate-950 p-6 overflow-y-auto flex flex-col transition-colors">
      <div className="max-w-6xl w-full mx-auto space-y-5">
        {/* Header */}
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <h1 className="text-lg font-semibold text-slate-900 dark:text-slate-100 tracking-tight">
              Supplier Purchase Orders
            </h1>
            <p className="text-xs text-slate-500 dark:text-slate-400 mt-0.5">
              Automated procurement drafts generated from customer order shortfalls.
            </p>
          </div>

          <div className="flex items-center gap-2">
            {successToast && (
              <span className="text-xs font-medium text-emerald-700 bg-emerald-50 border border-emerald-200 px-2.5 py-1 rounded dark:bg-emerald-950/40 dark:text-emerald-300 dark:border-emerald-800 flex items-center gap-1">
                <Check className="w-3.5 h-3.5" /> {successToast}
              </span>
            )}

            <button
              onClick={loadOrders}
              className="text-xs text-slate-600 dark:text-slate-300 hover:text-slate-900 dark:hover:text-white px-2.5 py-1.5 rounded border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 flex items-center gap-1.5 transition cursor-pointer"
            >
              <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
              <span>Refresh</span>
            </button>
          </div>
        </div>

        {/* Filter Pills */}
        <div className="flex items-center gap-1.5 text-xs">
          {[
            { id: 'all', label: 'All Orders' },
            { id: 'draft', label: 'Pending Approval' },
            { id: 'sent', label: 'Dispatched to Supplier' },
          ].map((tab) => (
            <button
              key={tab.id}
              onClick={() => setFilterStatus(tab.id)}
              className={`px-3 py-1.5 rounded-md font-medium transition cursor-pointer ${
                filterStatus === tab.id
                  ? 'bg-slate-900 text-white dark:bg-white dark:text-slate-900'
                  : 'bg-white dark:bg-slate-900 text-slate-600 dark:text-slate-400 border border-slate-200 dark:border-slate-800 hover:bg-slate-50'
              }`}
            >
              {tab.label}
            </button>
          ))}
        </div>

        {/* Real Data Table */}
        <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-lg overflow-hidden shadow-xs">
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-50 dark:bg-slate-800/60 border-b border-slate-200 dark:border-slate-800 text-slate-500 dark:text-slate-400 uppercase text-[11px] font-medium sticky top-0">
                <tr>
                  <th className="py-3 px-4">PO Number</th>
                  <th className="py-3 px-4">Supplier</th>
                  <th className="py-3 px-4">Items / Shortfall</th>
                  <th className="py-3 px-4 text-right">Wholesale Cost</th>
                  <th className="py-3 px-4">Status</th>
                  <th className="py-3 px-4 text-right">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 dark:divide-slate-800 text-slate-700 dark:text-slate-300">
                {loading && orders.length === 0 ? (
                  <tr>
                    <td colSpan={6} className="py-12 text-center text-slate-400">
                      Loading supplier purchase orders...
                    </td>
                  </tr>
                ) : filteredOrders.length === 0 ? (
                  <tr>
                    <td colSpan={6} className="py-12 text-center text-slate-400">
                      No purchase orders matching this filter.
                    </td>
                  </tr>
                ) : (
                  filteredOrders.map((o) => (
                    <tr key={o.id} className="hover:bg-slate-50/80 dark:hover:bg-slate-800/40 transition">
                      <td className="py-3.5 px-4 font-mono font-medium text-slate-900 dark:text-slate-100">
                        {o.order_number}
                      </td>
                      <td className="py-3.5 px-4">
                        <div className="font-medium text-slate-900 dark:text-slate-100">{o.supplier_name}</div>
                        <div className="text-[11px] text-slate-400">{o.supplier_email}</div>
                      </td>
                      <td className="py-3.5 px-4">
                        {o.items.map((it) => (
                          <div key={it.id} className="text-xs">
                            <span className="font-medium text-slate-900 dark:text-slate-100">{it.shortfall_quantity} units</span>
                            <span className="text-slate-500 font-mono ml-1">({it.product_sku})</span>
                          </div>
                        ))}
                      </td>
                      <td className="py-3.5 px-4 text-right font-medium text-slate-900 dark:text-slate-100 tabular-nums">
                        ₹{o.total_estimated_cost.toLocaleString()}
                      </td>
                      <td className="py-3.5 px-4">
                        {o.status === 'draft' ? (
                          <span className="inline-flex items-center gap-1 text-[11px] font-medium text-amber-700 bg-amber-50 border border-amber-200 px-2 py-0.5 rounded dark:bg-amber-950/40 dark:text-amber-300 dark:border-amber-800">
                            Pending approval
                          </span>
                        ) : (
                          <span className="inline-flex items-center gap-1 text-[11px] font-medium text-emerald-700 bg-emerald-50 border border-emerald-200 px-2 py-0.5 rounded dark:bg-emerald-950/40 dark:text-emerald-300 dark:border-emerald-800">
                            <CheckCircle2 className="w-3 h-3" /> Dispatched
                          </span>
                        )}
                      </td>
                      <td className="py-3.5 px-4 text-right">
                        {o.status === 'draft' ? (
                          <button
                            onClick={() => setSelectedOrder(o)}
                            className="inline-flex items-center gap-1 px-3 py-1.5 rounded bg-blue-700 hover:bg-blue-800 text-white font-medium text-xs transition cursor-pointer shadow-xs"
                          >
                            <Send className="w-3 h-3" /> Approve & send
                          </button>
                        ) : (
                          <span className="text-[11px] text-slate-400">Completed</span>
                        )}
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>

        {/* PO Approval Modal */}
        {selectedOrder && (
          <div className="fixed inset-0 bg-slate-900/40 backdrop-blur-xs flex items-center justify-center z-50 p-4">
            <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-lg p-6 max-w-lg w-full shadow-xl space-y-4">
              <div className="flex items-center justify-between border-b border-slate-200 dark:border-slate-800 pb-3">
                <div>
                  <h3 className="text-base font-semibold text-slate-900 dark:text-white">
                    Approve Supplier Purchase Order
                  </h3>
                  <p className="text-xs text-slate-500 font-mono mt-0.5">{selectedOrder.order_number}</p>
                </div>
                <button
                  onClick={() => setSelectedOrder(null)}
                  className="text-slate-400 hover:text-slate-700 dark:hover:text-slate-200 cursor-pointer"
                >
                  ✕
                </button>
              </div>

              <div className="space-y-3 text-xs text-slate-600 dark:text-slate-300">
                <div className="bg-slate-50 dark:bg-slate-800/60 p-3 rounded space-y-1.5 border border-slate-200/60 dark:border-slate-700/60">
                  <div className="flex justify-between">
                    <span className="text-slate-400">Supplier:</span>
                    <strong className="text-slate-900 dark:text-slate-100">{selectedOrder.supplier_name}</strong>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-slate-400">Dispatch Email:</span>
                    <span className="font-mono text-slate-700 dark:text-slate-300">{selectedOrder.supplier_email}</span>
                  </div>
                  <div className="flex justify-between border-t border-slate-200 dark:border-slate-700 pt-1.5">
                    <span className="text-slate-400">Total Purchase Value:</span>
                    <strong className="text-slate-900 dark:text-slate-100 font-mono text-sm">
                      ₹{selectedOrder.total_estimated_cost.toLocaleString()}
                    </strong>
                  </div>
                </div>

                <div>
                  <label className="block text-[11px] font-medium text-slate-500 uppercase tracking-wider mb-1">
                    Approval Remarks / Priority Instructions
                  </label>
                  <input
                    type="text"
                    value={managerNotes}
                    onChange={(e) => setManagerNotes(e.target.value)}
                    placeholder="e.g. Authorized for express road delivery."
                    className="w-full text-xs p-2.5 border border-slate-300 dark:border-slate-700 rounded bg-white dark:bg-slate-950 text-slate-900 dark:text-slate-100 focus:outline-none focus:ring-1 focus:ring-blue-600"
                  />
                </div>
              </div>

              <div className="flex justify-end gap-2 pt-2 border-t border-slate-200 dark:border-slate-800">
                <button
                  onClick={() => setSelectedOrder(null)}
                  className="px-3.5 py-1.5 text-xs text-slate-600 dark:text-slate-400 hover:text-slate-900 cursor-pointer"
                >
                  Cancel
                </button>
                <button
                  onClick={handleApprove}
                  disabled={submitting}
                  className="px-4 py-2 bg-blue-700 hover:bg-blue-800 text-white font-medium text-xs rounded transition shadow-sm cursor-pointer disabled:opacity-50"
                >
                  {submitting ? 'Transmitting...' : 'Confirm & Transmit PO'}
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
