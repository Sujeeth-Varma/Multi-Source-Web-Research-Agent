import { useState } from 'react';
import { Search, Sparkles, Database, Zap, RefreshCw } from 'lucide-react';
import type { ResearchRequest } from '../types/research';

interface ResearchFormProps {
  onSubmit: (request: ResearchRequest) => void;
  onLoadSample: () => void;
  isLoading: boolean;
}

const PRESET_QUESTIONS = [
  "what is langchain",
  "RAG architecture vs Fine-tuning",
  "Vector databases comparison 2026",
  "Agent harness framework features"
];

export const ResearchForm: React.FC<ResearchFormProps> = ({ onSubmit, onLoadSample, isLoading }) => {
  const [question, setQuestion] = useState("what is langchain");
  const [maxSources, setMaxSources] = useState(8);
  const [enablePlanning, setEnablePlanning] = useState(true);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!question.trim() || isLoading) return;
    onSubmit({
      question: question.trim(),
      max_sources: maxSources,
      enable_planning: enablePlanning,
    });
  };

  return (
    <div className="bg-zinc-900/60 border border-zinc-800 rounded-2xl p-5 sm:p-6 shadow-xl relative overflow-hidden backdrop-blur-sm">
      {/* Accent glow top right */}
      <div className="absolute -top-16 -right-16 w-32 h-32 bg-orange-500/10 rounded-full blur-3xl pointer-events-none" />

      <form onSubmit={handleSubmit} className="space-y-4">
        {/* Input box */}
        <div>
          <label htmlFor="question-input" className="block text-xs font-semibold uppercase tracking-wider text-zinc-400 mb-2 flex items-center justify-between">
            <span>Research Query</span>
            <span className="text-[10px] text-zinc-500 font-mono">POST /api/v1/research</span>
          </label>
          <div className="relative group">
            <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-zinc-500 group-focus-within:text-orange-500 transition-colors">
              <Search className="w-5 h-5" />
            </div>
            <input
              id="question-input"
              type="text"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              placeholder="Ask any research topic (e.g. what is langchain...)"
              className="w-full bg-zinc-950/90 text-zinc-100 placeholder-zinc-500 pl-11 pr-4 py-3.5 rounded-xl border border-zinc-800 focus:border-orange-500 focus:ring-2 focus:ring-orange-500/20 outline-none transition-all font-medium text-sm sm:text-base"
            />
          </div>
        </div>

        {/* Preset query chips */}
        <div className="flex flex-wrap items-center gap-2 pt-1">
          <span className="text-xs text-zinc-500 flex items-center gap-1">
            <Zap className="w-3 h-3 text-orange-500" /> Suggestions:
          </span>
          {PRESET_QUESTIONS.map((q) => (
            <button
              key={q}
              type="button"
              onClick={() => setQuestion(q)}
              className={`text-xs px-2.5 py-1 rounded-lg border transition-all ${
                question.toLowerCase() === q.toLowerCase()
                  ? 'bg-orange-500/15 border-orange-500/40 text-orange-400 font-medium'
                  : 'bg-zinc-950/60 border-zinc-800 text-zinc-400 hover:border-zinc-700 hover:text-zinc-300'
              }`}
            >
              {q}
            </button>
          ))}
        </div>

        {/* Options Bar */}
        <div className="pt-2 flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-t border-zinc-800/60">
          <div className="flex items-center space-x-6 text-xs text-zinc-400">
            {/* Max Sources Slider */}
            <div className="flex items-center space-x-2">
              <Database className="w-4 h-4 text-orange-500" />
              <span>Max Sources:</span>
              <input
                type="number"
                min={1}
                max={20}
                value={maxSources}
                onChange={(e) => setMaxSources(Number(e.target.value))}
                className="w-14 bg-zinc-950 border border-zinc-800 rounded px-2 py-1 text-center text-orange-400 font-mono font-semibold focus:border-orange-500 outline-none"
              />
            </div>

            {/* Enable Planning Toggle */}
            <label className="flex items-center space-x-2 cursor-pointer select-none">
              <input
                type="checkbox"
                checked={enablePlanning}
                onChange={(e) => setEnablePlanning(e.target.checked)}
                className="sr-only peer"
              />
              <div className="w-8 h-4 bg-zinc-800 rounded-full peer peer-checked:bg-orange-600 peer-checked:after:translate-x-full after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-zinc-200 after:rounded-full after:h-3 after:w-3 after:transition-all relative"></div>
              <span className="text-zinc-300 font-medium">Enable Planning</span>
            </label>
          </div>

          {/* Action Buttons */}
          <div className="flex items-center space-x-3">
            <button
              type="button"
              onClick={onLoadSample}
              className="flex-1 sm:flex-initial px-4 py-2.5 rounded-xl border border-zinc-700 hover:border-orange-500/50 text-zinc-300 hover:text-orange-400 text-xs font-semibold transition-all bg-zinc-950/80 hover:bg-zinc-900 flex items-center justify-center space-x-2"
              title="Load exact API response JSON provided in user request"
            >
              <RefreshCw className="w-3.5 h-3.5" />
              <span>Load Sample Response</span>
            </button>

            <button
              type="submit"
              disabled={isLoading || !question.trim()}
              className="flex-1 sm:flex-initial px-6 py-2.5 rounded-xl bg-orange-600 hover:bg-orange-500 text-zinc-950 text-xs font-bold uppercase tracking-wider transition-all shadow-lg shadow-orange-600/25 flex items-center justify-center space-x-2 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isLoading ? (
                <>
                  <div className="w-4 h-4 border-2 border-zinc-950 border-t-transparent rounded-full animate-spin" />
                  <span>Executing...</span>
                </>
              ) : (
                <>
                  <Sparkles className="w-4 h-4" />
                  <span>Run Agent</span>
                </>
              )}
            </button>
          </div>
        </div>
      </form>
    </div>
  );
};
