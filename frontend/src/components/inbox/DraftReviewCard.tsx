import React, { useState, useEffect } from 'react';
import type { MessageDetailResponse } from '../../types';
import { CountdownTimer } from '../common/CountdownTimer';
import { api } from '../../services/api';
import {
  Edit2,
  AlertTriangle,
  Send,
  Save,
  Sparkles
} from 'lucide-react';

interface DraftReviewCardProps {
  detail: MessageDetailResponse;
  onActionComplete: () => void;
}

export const DraftReviewCard: React.FC<DraftReviewCardProps> = ({
  detail,
  onActionComplete,
}) => {
  const { message, draft, customer } = detail;

  const [isEditing, setIsEditing] = useState(false);
  const [editedText, setEditedText] = useState(draft?.edited_text || draft?.draft_text || '');
  const [loading, setLoading] = useState(false);
  const [showRejectModal, setShowRejectModal] = useState(false);
  const [rejectReason, setRejectReason] = useState('');

  useEffect(() => {
    setEditedText(draft?.edited_text || draft?.draft_text || '');
    setIsEditing(false);
  }, [detail]);

  // Keyboard shortcut: Alt + A to Approve
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.altKey && (e.key === 'a' || e.key === 'A')) {
        e.preventDefault();
        if (draft && draft.status === 'pending' && !loading) {
          handleApprove();
        }
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [draft, loading, isEditing, editedText]);

  const handleApprove = async () => {
    if (!draft) return;
    setLoading(true);
    try {
      if (isEditing && editedText !== draft.draft_text) {
        await api.editDraft(draft.id, editedText);
      }
      await api.approveDraft(draft.id);
      onActionComplete();
    } catch (err) {
      console.error('Failed to approve draft:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleSaveEdit = async () => {
    if (!draft) return;
    setLoading(true);
    try {
      await api.editDraft(draft.id, editedText);
      setIsEditing(false);
      onActionComplete();
    } catch (err) {
      console.error('Failed to save edit:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleReject = async () => {
    if (!draft) return;
    setLoading(true);
    try {
      await api.rejectDraft(draft.id, rejectReason || 'Manager rejection');
      setShowRejectModal(false);
      onActionComplete();
    } catch (err) {
      console.error('Failed to reject draft:', err);
    } finally {
      setLoading(false);
    }
  };

  const recipientDisplay = customer
    ? `${customer.name} <${message.sender_address}>`
    : message.sender_address;

  const isPending = draft?.status === 'pending';
  const isEscalated = draft?.status === 'escalated';

  return (
    <div className="flex-1 flex flex-col h-full bg-white dark:bg-slate-900 overflow-hidden transition-colors">
      {/* 1. Top Compact Header & Summary Bar */}
      <div className="px-6 py-3.5 border-b border-slate-200 dark:border-slate-800 flex items-center justify-between gap-4 shrink-0">
        <div className="min-w-0">
          <div className="flex items-center gap-2 mb-0.5">
            <h1 className="text-sm font-semibold text-slate-900 dark:text-slate-100 truncate">
              {message.subject || 'Customer Inquiry'}
            </h1>
            <span className="text-[11px] text-slate-400 dark:text-slate-500 font-mono">
              #{message.id}
            </span>
          </div>
          <div className="flex items-center gap-2 text-xs text-slate-500 dark:text-slate-400">
            <span>From: {recipientDisplay}</span>
          </div>
        </div>

        {/* Calm countdown timer or status badge */}
        {draft && (
          <CountdownTimer
            initialSeconds={draft.seconds_remaining}
            deadlineString={draft.auto_approve_deadline}
            status={draft.status}
            onExpire={onActionComplete}
          />
        )}
      </div>

      {/* 2. Main Scroll Area: Customer Message (Secondary) + Draft Composer (Hero) */}
      <div className="flex-1 overflow-y-auto px-6 py-5 space-y-6">
        {/* Customer Incoming Message (Secondary Quote Block) */}
        <div>
          <div className="text-[11px] font-medium text-slate-400 uppercase tracking-wider mb-2">
            Inbound message
          </div>
          <div className="p-3.5 rounded-lg bg-slate-50 dark:bg-slate-800/40 border-l-2 border-slate-300 dark:border-slate-700 text-xs text-slate-700 dark:text-slate-300 leading-relaxed font-sans whitespace-pre-wrap">
            {message.raw_text}
          </div>
        </div>

        {/* Security Alert if Injected */}
        {message.prompt_injection_detected && (
          <div className="p-3 rounded-md bg-red-50 dark:bg-red-950/40 border border-red-200 dark:border-red-900 text-xs text-red-700 dark:text-red-300 flex items-start gap-2">
            <AlertTriangle className="w-4 h-4 shrink-0 mt-0.5" />
            <div>
              <strong className="font-semibold">Security policy violation:</strong> Prompt injection attempt detected and neutralized. Automatic drafting was blocked.
            </div>
          </div>
        )}

        {/* Draft Reply — The Visual Hero */}
        {draft && (
          <div className="border border-slate-200 dark:border-slate-800 rounded-lg bg-white dark:bg-slate-900 shadow-sm overflow-hidden">
            {/* Composer Header */}
            <div className="px-4 py-3 bg-slate-50/70 dark:bg-slate-800/50 border-b border-slate-200 dark:border-slate-800 flex items-center justify-between text-xs">
              <div className="flex items-center gap-2">
                <Sparkles className="w-3.5 h-3.5 text-blue-600 dark:text-blue-400" />
                <span className="font-medium text-slate-700 dark:text-slate-200">
                  AI drafted reply
                </span>
                <span className="text-slate-400">·</span>
                <span className="text-slate-500 dark:text-slate-400">
                  To: {customer?.name || message.sender_address}
                </span>
              </div>

              {isPending && !isEditing && (
                <button
                  onClick={() => setIsEditing(true)}
                  className="inline-flex items-center gap-1 text-xs text-slate-600 dark:text-slate-300 hover:text-slate-900 dark:hover:text-white transition cursor-pointer"
                >
                  <Edit2 className="w-3 h-3" /> Edit text
                </button>
              )}
            </div>

            {/* Composer Body */}
            <div className="p-5">
              {isEditing ? (
                <div className="space-y-3">
                  <textarea
                    value={editedText}
                    onChange={(e) => setEditedText(e.target.value)}
                    rows={10}
                    className="w-full text-sm leading-relaxed p-3 bg-white dark:bg-slate-950 border border-blue-500 rounded-md focus:outline-none focus:ring-1 focus:ring-blue-500 dark:text-slate-100 font-sans"
                  />
                  <div className="flex justify-end gap-2 text-xs">
                    <button
                      onClick={() => setIsEditing(false)}
                      className="px-3 py-1.5 text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-200 cursor-pointer"
                    >
                      Cancel
                    </button>
                    <button
                      onClick={handleSaveEdit}
                      disabled={loading}
                      className="inline-flex items-center gap-1 px-3 py-1.5 bg-blue-700 hover:bg-blue-800 text-white font-medium rounded cursor-pointer"
                    >
                      <Save className="w-3 h-3" /> Save changes
                    </button>
                  </div>
                </div>
              ) : (
                <div className="text-sm text-slate-800 dark:text-slate-200 leading-relaxed whitespace-pre-wrap font-sans">
                  {draft.edited_text || draft.draft_text}
                </div>
              )}
            </div>

            {/* Quiet Footer Note */}
            <div className="px-5 py-2.5 bg-slate-50/50 dark:bg-slate-800/30 border-t border-slate-100 dark:border-slate-800/80 text-[11px] text-slate-500 dark:text-slate-400 flex items-center justify-between">
              <span>AI-drafted from verified catalog pricing and warehouse inventory.</span>
              {isEscalated && (
                <span className="text-amber-600 dark:text-amber-400 font-medium flex items-center gap-1">
                  <AlertTriangle className="w-3 h-3" /> Customer sentiment requires manager review
                </span>
              )}
            </div>
          </div>
        )}
      </div>

      {/* 3. Hero Bottom Action Bar */}
      {draft && isPending && (
        <div className="px-6 py-3.5 bg-white dark:bg-slate-900 border-t border-slate-200 dark:border-slate-800 flex items-center justify-between shrink-0">
          <span className="text-xs text-slate-500 dark:text-slate-400">
            Press <kbd className="px-1.5 py-0.5 rounded bg-slate-100 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-[11px] font-mono text-slate-700 dark:text-slate-300">Alt</kbd> + <kbd className="px-1.5 py-0.5 rounded bg-slate-100 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-[11px] font-mono text-slate-700 dark:text-slate-300">A</kbd> to approve immediately
          </span>

          <div className="flex items-center gap-2.5">
            <button
              onClick={() => setShowRejectModal(true)}
              disabled={loading}
              className="px-3.5 py-1.5 text-xs text-slate-600 dark:text-slate-400 hover:text-red-600 dark:hover:text-red-400 font-medium rounded hover:bg-slate-100 dark:hover:bg-slate-800 transition cursor-pointer"
            >
              Reject
            </button>

            <button
              onClick={handleApprove}
              disabled={loading}
              className="inline-flex items-center gap-1.5 px-5 py-2 rounded-md bg-blue-700 hover:bg-blue-800 text-white text-xs font-semibold shadow-sm transition cursor-pointer disabled:opacity-50"
            >
              <Send className="w-3.5 h-3.5" />
              <span>{loading ? 'Sending...' : 'Approve & send'}</span>
            </button>
          </div>
        </div>
      )}

      {/* Rejection Modal */}
      {showRejectModal && (
        <div className="fixed inset-0 bg-slate-900/40 backdrop-blur-xs flex items-center justify-center z-50 p-4">
          <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-lg p-5 max-w-sm w-full shadow-xl space-y-3">
            <h3 className="text-sm font-semibold text-slate-900 dark:text-white">Reject draft response</h3>
            <p className="text-xs text-slate-500 dark:text-slate-400">
              Provide an internal note explaining why this response was rejected.
            </p>
            <textarea
              value={rejectReason}
              onChange={(e) => setRejectReason(e.target.value)}
              placeholder="e.g. Quoted pricing does not reflect customized agreement."
              rows={3}
              className="w-full text-xs p-2.5 border border-slate-300 dark:border-slate-700 rounded bg-white dark:bg-slate-950 text-slate-800 dark:text-slate-200 focus:outline-none focus:ring-1 focus:ring-blue-500"
            />
            <div className="flex justify-end gap-2 pt-1 text-xs">
              <button
                onClick={() => setShowRejectModal(false)}
                className="px-3 py-1.5 text-slate-600 dark:text-slate-400 hover:text-slate-800 cursor-pointer"
              >
                Cancel
              </button>
              <button
                onClick={handleReject}
                className="px-3 py-1.5 bg-red-600 hover:bg-red-700 text-white font-medium rounded cursor-pointer"
              >
                Confirm rejection
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
