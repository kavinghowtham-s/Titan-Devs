import React from 'react';
import {
  Inbox,
  Package,
  Mic,
  TrendingUp,
  History,
  Settings,
  Building2
} from 'lucide-react';

interface SidebarProps {
  activeTab: string;
  onTabChange: (tab: string) => void;
  pendingCount: number;
  stockAlertCount?: number;
}

export const Sidebar: React.FC<SidebarProps> = ({
  activeTab,
  onTabChange,
  pendingCount,
  stockAlertCount = 2,
}) => {
  const navItems = [
    {
      id: 'inbox',
      label: 'Inbox',
      icon: Inbox,
      badge: pendingCount > 0 ? pendingCount : null,
      badgeColor: 'bg-blue-100 text-blue-700 dark:bg-blue-900/60 dark:text-blue-300 font-semibold',
    },
    {
      id: 'stock',
      label: 'Supplier Orders',
      icon: Package,
      badge: stockAlertCount > 0 ? stockAlertCount : null,
      badgeColor: 'bg-amber-100 text-amber-800 dark:bg-amber-950/60 dark:text-amber-400',
    },
    {
      id: 'assistant',
      label: 'Ask AI',
      icon: Mic,
    },
    {
      id: 'analytics',
      label: 'Forecast',
      icon: TrendingUp,
    },
    {
      id: 'audit',
      label: 'Activity Log',
      icon: History,
    },
    {
      id: 'settings',
      label: 'Settings',
      icon: Settings,
    },
  ];

  return (
    <aside className="w-52 bg-slate-50 dark:bg-slate-950 border-r border-slate-200 dark:border-slate-800 flex flex-col justify-between select-none py-3 px-2 shrink-0 transition-colors">
      <div>
        <nav className="space-y-0.5">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeTab === item.id;
            return (
              <button
                key={item.id}
                onClick={() => onTabChange(item.id)}
                className={`w-full flex items-center justify-between px-3 py-2 rounded-md text-xs font-medium transition cursor-pointer ${
                  isActive
                    ? 'bg-slate-200/70 text-slate-900 dark:bg-slate-800 dark:text-white font-semibold'
                    : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-900'
                }`}
              >
                <div className="flex items-center gap-2.5">
                  <Icon className={`w-4 h-4 ${isActive ? 'text-blue-700 dark:text-blue-400' : 'text-slate-500 dark:text-slate-400'}`} />
                  <span>{item.label}</span>
                </div>
                {item.badge !== null && item.badge !== undefined && (
                  <span className={`text-[11px] px-1.5 py-0.2 rounded-full tabular-nums ${item.badgeColor}`}>
                    {item.badge}
                  </span>
                )}
              </button>
            );
          })}
        </nav>
      </div>

      {/* Quiet Corporate Footer */}
      <div className="px-3 py-2.5 border-t border-slate-200 dark:border-slate-800 text-[11px] text-slate-500 dark:text-slate-500">
        <div className="flex items-center gap-1.5 font-medium text-slate-700 dark:text-slate-400 mb-0.5">
          <Building2 className="w-3.5 h-3.5 text-slate-400" />
          <span>Trentar Pvt Ltd</span>
        </div>
        <p className="text-[10px] text-slate-400 dark:text-slate-500">Plant #2 Operations</p>
      </div>
    </aside>
  );
};
