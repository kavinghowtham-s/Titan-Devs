import { useState, useEffect } from 'react';
import { TopNav } from './components/layout/TopNav';
import { Sidebar } from './components/layout/Sidebar';
import { InboxPage } from './pages/InboxPage';
import { StockOrdersPage } from './pages/StockOrdersPage';
import { AssistantPage } from './pages/AssistantPage';
import { AnalyticsPage } from './pages/AnalyticsPage';
import { AuditLogPage } from './pages/AuditLogPage';
import { SettingsPage } from './pages/SettingsPage';
import { api } from './services/api';

export function App() {
  const [activeTab, setActiveTab] = useState('inbox');
  const [pendingCount, setPendingCount] = useState(0);
  const [mockMode, setMockMode] = useState(false);
  const [darkMode, setDarkMode] = useState(false); // Default to calm Light Theme per design direction
  const [refreshTrigger, setRefreshTrigger] = useState(0);

  // Sync dark class on document element
  useEffect(() => {
    if (darkMode) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, [darkMode]);

  const toggleDarkMode = () => {
    setDarkMode((prev) => !prev);
  };

  const fetchGlobalStats = async () => {
    try {
      const drafts = await api.getPendingDrafts();
      setPendingCount(drafts.length);
      const settings = await api.getSettings();
      setMockMode(settings.use_mock_llm);
    } catch (err) {
      console.error('Failed to fetch global stats:', err);
    }
  };

  useEffect(() => {
    fetchGlobalStats();
    const interval = setInterval(fetchGlobalStats, 10000);
    return () => clearInterval(interval);
  }, [refreshTrigger]);

  const handleTriggerRefresh = () => {
    setRefreshTrigger((prev) => prev + 1);
  };

  return (
    <div className="flex flex-col h-screen w-screen overflow-hidden bg-slate-50 dark:bg-slate-950 text-slate-900 dark:text-slate-100 font-sans transition-colors">
      {/* Top Application Bar */}
      <TopNav
        mockMode={mockMode}
        darkMode={darkMode}
        onToggleDarkMode={toggleDarkMode}
        pendingCount={pendingCount}
        onMessageCreated={handleTriggerRefresh}
      />

      {/* Main Container */}
      <div className="flex flex-1 overflow-hidden">
        {/* Left Module Sidebar */}
        <Sidebar
          activeTab={activeTab}
          onTabChange={setActiveTab}
          pendingCount={pendingCount}
        />

        {/* Dynamic Workspace Container */}
        <main className="flex-1 flex overflow-hidden">
          {activeTab === 'inbox' && (
            <InboxPage
              refreshTrigger={refreshTrigger}
              onNavigateToStock={() => setActiveTab('stock')}
            />
          )}
          {activeTab === 'stock' && <StockOrdersPage />}
          {activeTab === 'assistant' && <AssistantPage />}
          {activeTab === 'analytics' && <AnalyticsPage />}
          {activeTab === 'audit' && <AuditLogPage />}
          {activeTab === 'settings' && (
            <SettingsPage
              onSettingsUpdated={handleTriggerRefresh}
            />
          )}
        </main>
      </div>
    </div>
  );
}

export default App;
