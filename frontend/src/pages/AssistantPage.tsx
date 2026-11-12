import React, { useState } from 'react';
import { api } from '../services/api';
import type { SQLQueryResponse } from '../types';
import {
  Mic,
  MicOff,
  Send,
  Volume2,
  Code2,
  ChevronDown,
  ChevronUp,
  RefreshCw,
  Sparkles,
  ShieldCheck
} from 'lucide-react';

export const AssistantPage: React.FC = () => {
  const [prompt, setPrompt] = useState('');
  const [language, setLanguage] = useState<'en' | 'ta' | 'hi'>('en');
  const [loading, setLoading] = useState(false);
  const [response, setResponse] = useState<SQLQueryResponse | null>(null);
  const [sqlExpanded, setSqlExpanded] = useState(false);
  const [isListening, setIsListening] = useState(false);

  // Suggested queries for presentation walkthroughs
  const sampleQueries = [
    {
      label: 'Suppliers & Lead Times',
      prompt: 'Show our suppliers and procurement lead times.',
      lang: 'en' as const,
    },
    {
      label: 'Total Revenue & Sales',
      prompt: 'What is our total revenue and sales volume?',
      lang: 'en' as const,
    },
    {
      label: 'Lowest stock parts',
      prompt: 'Show products with low stock count below reorder level.',
      lang: 'en' as const,
    },
    {
      label: 'Top selling item (Tamil)',
      prompt: 'கடந்த காலத்தில் அதிக விற்பனையான பொருள் எது?',
      lang: 'ta' as const,
    },
    {
      label: 'Critical low stock (Hindi)',
      prompt: 'वेयरहाउस में कौन से उत्पाद का स्टॉक कम है?',
      lang: 'hi' as const,
    },
  ];

  const handleQuery = async (queryText?: string, langCode?: 'en' | 'ta' | 'hi') => {
    const textToRun = queryText || prompt;
    const langToRun = langCode || language;
    if (!textToRun.trim()) return;

    setLoading(true);
    try {
      const res = await api.queryAssistant(textToRun, langToRun);
      setResponse(res);
      setPrompt(textToRun);
      setLanguage(langToRun);
    } catch (err) {
      console.error('Failed to query assistant:', err);
    } finally {
      setLoading(false);
    }
  };

  // Browser Web Speech STT
  const handleToggleVoice = () => {
    const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
    if (!SpeechRecognition) {
      alert('Speech Recognition is not supported by this browser. Please use Chrome or Edge.');
      return;
    }

    if (isListening) {
      setIsListening(false);
      return;
    }

    const recognition = new SpeechRecognition();
    recognition.lang = language === 'ta' ? 'ta-IN' : language === 'hi' ? 'hi-IN' : 'en-IN';
    recognition.interimResults = false;

    recognition.onstart = () => setIsListening(true);
    recognition.onend = () => setIsListening(false);
    recognition.onerror = () => setIsListening(false);

    recognition.onresult = (event: any) => {
      const transcript = event.results[0][0].transcript;
      setPrompt(transcript);
      handleQuery(transcript, language);
    };

    recognition.start();
  };

  // Browser Web Speech TTS
  const handleSpeak = (textToSpeak: string) => {
    if (!('speechSynthesis' in window)) return;
    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(textToSpeak);
    utterance.lang = language === 'ta' ? 'ta-IN' : language === 'hi' ? 'hi-IN' : 'en-IN';
    window.speechSynthesis.speak(utterance);
  };

  return (
    <div className="flex-1 bg-slate-50 dark:bg-slate-950 p-6 overflow-y-auto flex flex-col transition-colors">
      <div className="max-w-4xl w-full mx-auto space-y-5">
        {/* Header */}
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div>
            <h1 className="text-lg font-semibold text-slate-900 dark:text-slate-100 tracking-tight">
              Ask AI — Operational Assistant
            </h1>
            <p className="text-xs text-slate-500 dark:text-slate-400 mt-0.5">
              Natural-language database queries for frontline staff. Strictly read-only, AST-verified SQL.
            </p>
          </div>

          <div className="flex items-center gap-2">
            <span className="inline-flex items-center gap-1 text-[11px] font-medium text-emerald-700 bg-emerald-50 border border-emerald-200 px-2 py-0.5 rounded dark:bg-emerald-950/40 dark:text-emerald-300 dark:border-emerald-800">
              <ShieldCheck className="w-3.5 h-3.5" /> Read-only SQLite Sandbox
            </span>
          </div>
        </div>

        {/* Input Box & Language Select */}
        <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-lg p-4 space-y-3 shadow-xs">
          <div className="flex items-center justify-between">
            <span className="text-[11px] font-medium text-slate-500 uppercase tracking-wider">
              Ask about inventory, sales, or suppliers
            </span>

            {/* Language Pills */}
            <div className="flex items-center gap-1 text-xs">
              {[
                { id: 'en', label: 'English' },
                { id: 'ta', label: 'தமிழ்' },
                { id: 'hi', label: 'हिंदी' },
              ].map((l) => (
                <button
                  key={l.id}
                  onClick={() => setLanguage(l.id as any)}
                  className={`px-2.5 py-0.5 rounded text-xs transition cursor-pointer ${
                    language === l.id
                      ? 'bg-slate-900 text-white dark:bg-white dark:text-slate-900 font-medium'
                      : 'text-slate-500 hover:bg-slate-100 dark:hover:bg-slate-800'
                  }`}
                >
                  {l.label}
                </button>
              ))}
            </div>
          </div>

          <div className="flex gap-2">
            <input
              type="text"
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleQuery()}
              placeholder={
                language === 'ta'
                  ? 'உதாரணம்: கடந்த 3 மாதங்களில் அதிக விற்பனையான பொருள் எது?'
                  : language === 'hi'
                  ? 'उदाहरण: वेयरहाउस में 10 से कम स्टॉक वाले उत्पाद दिखाएं'
                  : 'e.g. Which components have stock under 10 units?'
              }
              className="flex-1 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-md px-3.5 py-2 text-xs text-slate-900 dark:text-slate-100 placeholder-slate-400 focus:outline-none focus:ring-1 focus:ring-blue-600"
            />

            {/* Microphone Button */}
            <button
              onClick={handleToggleVoice}
              className={`p-2 rounded-md border transition cursor-pointer ${
                isListening
                  ? 'bg-red-50 text-red-600 border-red-300 dark:bg-red-950 dark:border-red-800'
                  : 'bg-slate-100 text-slate-600 border-slate-200 hover:bg-slate-200 dark:bg-slate-800 dark:border-slate-700 dark:text-slate-300'
              }`}
              title={isListening ? 'Stop listening' : 'Speak query'}
            >
              {isListening ? <MicOff className="w-4 h-4 animate-pulse" /> : <Mic className="w-4 h-4" />}
            </button>

            {/* Submit Button */}
            <button
              onClick={() => handleQuery()}
              disabled={loading || !prompt.trim()}
              className="px-4 py-2 bg-blue-700 hover:bg-blue-800 text-white font-medium text-xs rounded-md transition cursor-pointer disabled:opacity-50 flex items-center gap-1.5 shadow-xs"
            >
              {loading ? <RefreshCw className="w-3.5 h-3.5 animate-spin" /> : <Send className="w-3.5 h-3.5" />}
              <span>Query</span>
            </button>
          </div>

          {/* Preset Sample Pills */}
          <div className="flex flex-wrap items-center gap-2 pt-1 text-[11px] text-slate-500">
            <span className="text-slate-400">Try:</span>
            {sampleQueries.map((sq, i) => (
              <button
                key={i}
                onClick={() => handleQuery(sq.prompt, sq.lang)}
                className="text-xs text-slate-600 dark:text-slate-400 bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 px-2.5 py-0.5 rounded transition cursor-pointer"
              >
                {sq.label}
              </button>
            ))}
          </div>
        </div>

        {/* Results View */}
        {response && (
          <div className="space-y-4">
            {/* Natural Language Answer Card */}
            <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-lg p-5 space-y-3 shadow-xs">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2 text-xs font-semibold text-slate-900 dark:text-slate-100">
                  <Sparkles className="w-4 h-4 text-blue-600" />
                  <span>Answer</span>
                </div>

                <button
                  onClick={() => handleSpeak(response.natural_response)}
                  className="inline-flex items-center gap-1 text-xs text-blue-700 dark:text-blue-400 hover:underline cursor-pointer"
                >
                  <Volume2 className="w-3.5 h-3.5" />
                  <span>Play audio</span>
                </button>
              </div>

              <p className="text-sm text-slate-800 dark:text-slate-200 leading-relaxed font-sans">
                {response.natural_response}
              </p>

              {/* Collapsible SQL Query Inspector */}
              <div className="pt-2 border-t border-slate-100 dark:border-slate-800">
                <button
                  onClick={() => setSqlExpanded(!sqlExpanded)}
                  className="flex items-center gap-1.5 text-[11px] text-slate-500 hover:text-slate-800 dark:hover:text-slate-300 font-medium cursor-pointer"
                >
                  <Code2 className="w-3 h-3" />
                  <span>{sqlExpanded ? 'Hide executed SQL' : 'View executed SQL'}</span>
                  {sqlExpanded ? <ChevronUp className="w-3 h-3" /> : <ChevronDown className="w-3 h-3" />}
                </button>

                {sqlExpanded && (
                  <div className="mt-2 p-3 bg-slate-950 text-slate-200 rounded font-mono text-xs overflow-x-auto leading-relaxed border border-slate-800">
                    <div className="text-[10px] text-slate-500 uppercase tracking-wider mb-1 font-sans">
                      Verified Read-Only SQL (Latency: {response.execution_time_ms}ms)
                    </div>
                    {response.sql_query}
                  </div>
                )}
              </div>
            </div>

            {/* Structured Table Data Result */}
            {response.results && response.results.length > 0 && (
              <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-lg overflow-hidden shadow-xs">
                <div className="px-4 py-2.5 bg-slate-50 dark:bg-slate-800/60 border-b border-slate-200 dark:border-slate-800 text-xs font-medium text-slate-600 dark:text-slate-400 flex items-center justify-between">
                  <span>Query Results ({response.row_count} rows)</span>
                  <span className="text-[11px] text-slate-400 font-mono">SQLite mode=ro</span>
                </div>

                <div className="overflow-x-auto max-h-72">
                  <table className="w-full text-left text-xs">
                    <thead className="bg-slate-50 dark:bg-slate-800/40 text-slate-500 text-[11px] font-medium border-b border-slate-200 dark:border-slate-800 sticky top-0">
                      <tr>
                        {Object.keys(response.results[0]).map((col) => (
                          <th key={col} className="py-2 px-3 uppercase tracking-wider font-mono text-[10px]">
                            {col}
                          </th>
                        ))}
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-100 dark:divide-slate-800 text-slate-700 dark:text-slate-300">
                      {response.results.map((row, idx) => (
                        <tr key={idx} className="hover:bg-slate-50/60 dark:hover:bg-slate-800/30">
                          {Object.values(row).map((val: any, cidx) => (
                            <td key={cidx} className="py-2 px-3 font-mono text-xs">
                              {typeof val === 'number' ? val.toLocaleString() : String(val)}
                            </td>
                          ))}
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};
