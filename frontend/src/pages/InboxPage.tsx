import React, { useState, useEffect } from 'react';
import type { InboundMessage, MessageDetailResponse } from '../types';
import { MessageCard } from '../components/inbox/MessageCard';
import { DraftReviewCard } from '../components/inbox/DraftReviewCard';
import { ContextPanel } from '../components/inbox/ContextPanel';
import { api } from '../services/api';
import { Search, RefreshCw, Inbox } from 'lucide-react';

interface InboxPageProps {
  onNavigateToStock?: () => void;
  refreshTrigger?: number;
}

export const InboxPage: React.FC<InboxPageProps> = ({ onNavigateToStock, refreshTrigger }) => {
  const [messages, setMessages] = useState<InboundMessage[]>([]);
  const [selectedMessageId, setSelectedMessageId] = useState<number | null>(null);
  const [selectedDetail, setSelectedDetail] = useState<MessageDetailResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [loadingDetail, setLoadingDetail] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [filterIntent, setFilterIntent] = useState<string>('all');

  const loadMessages = async () => {
    setLoading(true);
    try {
      const data = await api.getMessages();
      setMessages(data);
      if (data.length > 0 && selectedMessageId === null) {
        setSelectedMessageId(data[0].id);
      }
    } catch (err) {
      console.error('Failed to load messages:', err);
    } finally {
      setLoading(false);
    }
  };

  const loadDetail = async (id: number) => {
    setLoadingDetail(true);
    try {
      const detail = await api.getMessageDetail(id);
      setSelectedDetail(detail);
    } catch (err) {
      console.error(`Failed to load detail for msg ${id}:`, err);
    } finally {
      setLoadingDetail(false);
    }
  };

  useEffect(() => {
    loadMessages();
  }, [refreshTrigger]);

  useEffect(() => {
    if (selectedMessageId !== null) {
      loadDetail(selectedMessageId);
    }
  }, [selectedMessageId]);

  const filteredMessages = messages.filter((m) => {
    const matchesSearch =
      m.sender_address.toLowerCase().includes(searchQuery.toLowerCase()) ||
      (m.subject && m.subject.toLowerCase().includes(searchQuery.toLowerCase())) ||
      m.raw_text.toLowerCase().includes(searchQuery.toLowerCase());

    if (!matchesSearch) return false;

    if (filterIntent === 'all') return true;
    if (filterIntent === 'bulk_order') return m.detected_intent === 'bulk_order';
    if (filterIntent === 'complaint') return m.detected_intent === 'complaint' || m.detected_intent === 'refund';
    if (filterIntent === 'price_quote') return m.detected_intent === 'price_quote';
    return true;
  });

  return (
    <div className="flex-1 flex overflow-hidden bg-slate-50 dark:bg-slate-950 transition-colors">
      {/* Pane 1: Message List (340px) */}
      <div className="w-80 bg-white dark:bg-slate-900 border-r border-slate-200 dark:border-slate-800 flex flex-col shrink-0">
        <div className="p-3 border-b border-slate-200 dark:border-slate-800 space-y-2">
          <div className="flex items-center justify-between">
            <h2 className="text-xs font-semibold text-slate-900 dark:text-slate-100 uppercase tracking-wider">
              Inbox
            </h2>
            <button
              onClick={loadMessages}
              className="text-slate-400 hover:text-slate-700 dark:hover:text-slate-200 p-1 rounded hover:bg-slate-100 dark:hover:bg-slate-800 cursor-pointer"
              title="Refresh messages"
            >
              <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
            </button>
          </div>

          {/* Search */}
          <div className="relative">
            <Search className="w-3.5 h-3.5 absolute left-2.5 top-2 text-slate-400" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search sender or SKU..."
              className="w-full bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded pl-8 pr-2.5 py-1 text-xs text-slate-800 dark:text-slate-200 placeholder-slate-400 focus:outline-none focus:ring-1 focus:ring-blue-600"
            />
          </div>

          {/* Filter Pills */}
          <div className="flex items-center gap-1 text-[11px] overflow-x-auto pb-0.5">
            {[
              { id: 'all', label: 'All' },
              { id: 'price_quote', label: 'Quotes' },
              { id: 'bulk_order', label: 'Bulk' },
              { id: 'complaint', label: 'Complaints' },
            ].map((tab) => (
              <button
                key={tab.id}
                onClick={() => setFilterIntent(tab.id)}
                className={`px-2 py-0.5 rounded font-medium transition cursor-pointer shrink-0 ${
                  filterIntent === tab.id
                    ? 'bg-slate-900 text-white dark:bg-white dark:text-slate-900 font-semibold'
                    : 'text-slate-500 hover:bg-slate-100 dark:hover:bg-slate-800'
                }`}
              >
                {tab.label}
              </button>
            ))}
          </div>
        </div>

        {/* Message Item Scroll */}
        <div className="flex-1 overflow-y-auto divide-y divide-slate-100 dark:divide-slate-800/50 p-1.5 space-y-0.5">
          {loading && messages.length === 0 ? (
            <div className="space-y-2 p-3">
              {[1, 2, 3, 4].map((i) => (
                <div key={i} className="h-16 bg-slate-100 dark:bg-slate-800/40 rounded animate-pulse" />
              ))}
            </div>
          ) : filteredMessages.length === 0 ? (
            <div className="p-8 text-center text-xs text-slate-400">
              No matching messages found.
            </div>
          ) : (
            filteredMessages.map((msg) => (
              <MessageCard
                key={msg.id}
                message={msg}
                isSelected={selectedMessageId === msg.id}
                onSelect={() => setSelectedMessageId(msg.id)}
              />
            ))
          )}
        </div>
      </div>

      {/* Pane 2: Conversation & Hero Draft Review Composer (Flex-1) */}
      <div className="flex-1 flex overflow-hidden">
        {loadingDetail ? (
          <div className="flex-1 flex items-center justify-center bg-white dark:bg-slate-900">
            <RefreshCw className="w-5 h-5 text-slate-400 animate-spin" />
          </div>
        ) : selectedDetail ? (
          <DraftReviewCard
            detail={selectedDetail}
            onActionComplete={() => {
              loadMessages();
              if (selectedMessageId) loadDetail(selectedMessageId);
            }}
          />
        ) : (
          <div className="flex-1 flex flex-col items-center justify-center text-slate-400 bg-white dark:bg-slate-900 text-xs">
            <Inbox className="w-10 h-10 mb-2 opacity-30" />
            <p>Select a message from the queue</p>
          </div>
        )}
      </div>

      {/* Pane 3: Context Inspector (300px) */}
      {selectedDetail && (
        <ContextPanel
          detail={selectedDetail}
          onNavigateToStock={onNavigateToStock}
        />
      )}
    </div>
  );
};
