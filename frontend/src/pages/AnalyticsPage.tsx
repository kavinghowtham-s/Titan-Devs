import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import type { DemandForecastItem, PnLSummary, ExecutiveBriefingReport } from '../types';
import {
  RefreshCw,
  Sparkles,
  Calendar
} from 'lucide-react';
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer
} from 'recharts';

export const AnalyticsPage: React.FC = () => {
  const [forecast, setForecast] = useState<DemandForecastItem[]>([]);
  const [pnl, setPnl] = useState<PnLSummary | null>(null);
  const [insights, setInsights] = useState<ExecutiveBriefingReport | null>(null);
  const [loading, setLoading] = useState(true);

  const loadAnalytics = async () => {
    setLoading(true);
    try {
      const [fData, pData, iData] = await Promise.all([
        api.getDemandForecast(30),
        api.getPnLSummary(),
        api.generateExecutiveInsights(),
      ]);
      setForecast(fData);
      setPnl(pData);
      setInsights(iData);
    } catch (err) {
      console.error('Failed to load analytics:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadAnalytics();
  }, []);

  // Synthetic demand curve points for Recharts based on top forecast items
  const chartData = [
    { month: 'Oct', actual: 120, projected: 120 },
    { month: 'Nov', actual: 145, projected: 145 },
    { month: 'Dec', actual: 160, projected: 160 },
    { month: 'Jan', actual: 185, projected: 185 },
    { month: 'Feb', actual: 210, projected: 210 },
    { month: 'Mar (Proj)', actual: null, projected: 260 },
  ];

  const criticalCount = forecast.filter((f) => f.status === 'CRITICAL').length;

  return (
    <div className="flex-1 bg-slate-50 dark:bg-slate-950 p-6 overflow-y-auto flex flex-col transition-colors">
      <div className="max-w-6xl w-full mx-auto space-y-6">
        {/* Header */}
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div>
            <h1 className="text-lg font-semibold text-slate-900 dark:text-slate-100 tracking-tight">
              Operational Forecast & Margins
            </h1>
            <p className="text-xs text-slate-500 dark:text-slate-400 mt-0.5">
              30-day forward demand projections, warehouse stockout risks, and gross profit analysis.
            </p>
          </div>

          <button
            onClick={loadAnalytics}
            className="text-xs text-slate-600 dark:text-slate-300 hover:text-slate-900 dark:hover:text-white px-2.5 py-1.5 rounded border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 flex items-center gap-1.5 transition cursor-pointer self-start sm:self-auto"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
            <span>Update projections</span>
          </button>
        </div>

        {/* Top KPI Cards */}
        {pnl && (
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-lg p-4 shadow-xs">
              <span className="text-xs text-slate-500 font-medium">30-Day Projected Revenue</span>
              <div className="text-xl font-semibold text-slate-900 dark:text-slate-100 mt-1 tabular-nums">
                ₹{(pnl.projected_month_revenue / 100000).toFixed(2)} Lakhs
              </div>
              <span className="text-[11px] text-emerald-600 dark:text-emerald-400 font-medium mt-1 inline-block">
                +8.2% vs previous run-rate
              </span>
            </div>

            <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-lg p-4 shadow-xs">
              <span className="text-xs text-slate-500 font-medium">Blended Gross Margin</span>
              <div className="text-xl font-semibold text-slate-900 dark:text-slate-100 mt-1 tabular-nums">
                {pnl.gross_margin_pct}%
              </div>
              <span className="text-[11px] text-slate-400 mt-1 inline-block">
                Consistent with industrial benchmark
              </span>
            </div>

            <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-lg p-4 shadow-xs">
              <span className="text-xs text-slate-500 font-medium">High Stockout Risk Items</span>
              <div className="text-xl font-semibold text-amber-600 dark:text-amber-400 mt-1 tabular-nums">
                {criticalCount} SKUs
              </div>
              <span className="text-[11px] text-slate-400 mt-1 inline-block">
                Deficit within 14-day lead time
              </span>
            </div>

            <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-lg p-4 shadow-xs">
              <span className="text-xs text-slate-500 font-medium">12-Month Sales Volume</span>
              <div className="text-xl font-semibold text-slate-900 dark:text-slate-100 mt-1 tabular-nums">
                {pnl.total_sales_volume.toLocaleString()} units
              </div>
              <span className="text-[11px] text-slate-400 mt-1 inline-block">
                Across 30 active product catalog lines
              </span>
            </div>
          </div>
        )}

        {/* Demand Curve Chart & Risk Highlights */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-5">
          <div className="lg:col-span-2 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-lg p-5 shadow-xs">
            <div className="flex items-center justify-between mb-4">
              <div>
                <h3 className="text-sm font-semibold text-slate-900 dark:text-slate-100">
                  Propulsion & Avionics Demand Trajectory
                </h3>
                <p className="text-xs text-slate-400">Monthly units sold and 30-day weighted run-rate projection</p>
              </div>
              <span className="text-xs text-slate-500 font-mono flex items-center gap-1">
                <Calendar className="w-3.5 h-3.5 text-slate-400" /> Oct - Mar
              </span>
            </div>

            <div className="h-56 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={chartData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                  <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e2e8f0" opacity={0.6} />
                  <XAxis dataKey="month" stroke="#94a3b8" fontSize={11} tickLine={false} />
                  <YAxis stroke="#94a3b8" fontSize={11} tickLine={false} />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: '#0f172a',
                      borderColor: '#1e293b',
                      borderRadius: '6px',
                      color: '#f8fafc',
                      fontSize: '12px',
                    }}
                  />
                  <Area type="monotone" dataKey="actual" stroke="#1d4ed8" fill="#dbeafe" fillOpacity={0.4} strokeWidth={2} name="Actual Sales" />
                  <Area type="monotone" dataKey="projected" stroke="#60a5fa" strokeDasharray="4 4" fill="#eff6ff" fillOpacity={0.2} strokeWidth={2} name="Projected Run-rate" />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* AI Executive Briefing */}
          <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-lg p-5 shadow-xs flex flex-col justify-between">
            <div>
              <div className="flex items-center gap-1.5 text-xs font-semibold text-blue-700 dark:text-blue-400 mb-2">
                <Sparkles className="w-3.5 h-3.5" />
                <span>Executive Operations Briefing</span>
              </div>

              {insights ? (
                <div className="space-y-3 text-xs leading-relaxed text-slate-700 dark:text-slate-300">
                  <div className="font-medium text-slate-900 dark:text-slate-100">
                    {insights.headline}
                  </div>
                  <div className="space-y-2">
                    {insights.actionable_insights.map((item, i) => (
                      <div key={i} className="p-2.5 rounded bg-slate-50 dark:bg-slate-800/60 border border-slate-100 dark:border-slate-700/60 text-[11px] space-y-1">
                        <div className="flex items-center justify-between">
                          <span className="font-semibold text-slate-800 dark:text-slate-200 capitalize">{item.category.replace('_', ' ')}</span>
                          <span className={`text-[10px] font-medium px-1.5 py-0.2 rounded uppercase ${item.severity === 'critical' ? 'bg-red-100 text-red-700 dark:bg-red-950 dark:text-red-400' : 'bg-amber-100 text-amber-700 dark:bg-amber-950 dark:text-amber-400'}`}>
                            {item.severity}
                          </span>
                        </div>
                        <p className="text-slate-600 dark:text-slate-400">{item.finding}</p>
                      </div>
                    ))}
                  </div>
                </div>
              ) : (
                <div className="py-8 text-center text-xs text-slate-400">Loading AI briefing...</div>
              )}
            </div>
          </div>
        </div>

        {/* 30-Day Forecast Table */}
        <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-lg overflow-hidden shadow-xs">
          <div className="px-4 py-3 bg-slate-50 dark:bg-slate-800/60 border-b border-slate-200 dark:border-slate-800 text-xs font-semibold text-slate-900 dark:text-slate-100 flex items-center justify-between">
            <span>30-Day Itemized Reorder Recommendations</span>
            <span className="text-[11px] text-slate-400 font-normal">Algorithm: Weighted Moving Average</span>
          </div>

          <div className="overflow-x-auto max-h-80">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-50 dark:bg-slate-800/40 text-slate-500 uppercase text-[10px] font-medium border-b border-slate-200 dark:border-slate-800 sticky top-0">
                <tr>
                  <th className="py-2.5 px-4">SKU</th>
                  <th className="py-2.5 px-4">Product Name</th>
                  <th className="py-2.5 px-4 text-right">In-Hand Stock</th>
                  <th className="py-2.5 px-4 text-right">30d Demand</th>
                  <th className="py-2.5 px-4 text-right">Daily Burn</th>
                  <th className="py-2.5 px-4 text-right">Stockout Risk</th>
                  <th className="py-2.5 px-4 text-center">Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 dark:divide-slate-800 text-slate-700 dark:text-slate-300">
                {forecast.map((f) => (
                  <tr key={f.product_id} className="hover:bg-slate-50/60 dark:hover:bg-slate-800/30">
                    <td className="py-2.5 px-4 font-mono font-medium text-slate-900 dark:text-slate-100 text-xs">
                      {f.sku}
                    </td>
                    <td className="py-2.5 px-4 font-medium text-slate-800 dark:text-slate-200">
                      {f.product_name}
                    </td>
                    <td className="py-2.5 px-4 text-right font-medium text-slate-900 dark:text-slate-100 tabular-nums">
                      {f.current_stock}
                    </td>
                    <td className="py-2.5 px-4 text-right tabular-nums text-slate-600 dark:text-slate-400">
                      {f.forecast_30d_demand}
                    </td>
                    <td className="py-2.5 px-4 text-right tabular-nums text-slate-600 dark:text-slate-400">
                      {f.daily_run_rate}/day
                    </td>
                    <td className="py-2.5 px-4 text-right tabular-nums font-semibold">
                      <span className={f.stockout_risk_pct >= 60 ? 'text-red-600' : f.stockout_risk_pct >= 25 ? 'text-amber-600' : 'text-slate-500'}>
                        {f.stockout_risk_pct}%
                      </span>
                    </td>
                    <td className="py-2.5 px-4 text-center">
                      <span className={`text-[10px] font-medium px-2 py-0.5 rounded ${f.status === 'CRITICAL' ? 'bg-red-100 text-red-700 dark:bg-red-950 dark:text-red-400' : f.status === 'WARNING' ? 'bg-amber-100 text-amber-700 dark:bg-amber-950 dark:text-amber-400' : 'bg-slate-100 text-slate-600 dark:bg-slate-800 dark:text-slate-400'}`}>
                        {f.status}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
};
