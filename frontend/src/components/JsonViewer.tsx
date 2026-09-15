import { useState } from 'react';
import { Code2, Copy, Check, ChevronDown, ChevronUp } from 'lucide-react';
import type { ResearchResponse } from '../types/research';

interface JsonViewerProps {
  data: ResearchResponse;
}

export const JsonViewer: React.FC<JsonViewerProps> = ({ data }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [copied, setCopied] = useState(false);

  const jsonString = JSON.stringify(data, null, 2);

  const handleCopy = (e: React.MouseEvent) => {
    e.stopPropagation();
    navigator.clipboard.writeText(jsonString);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="bg-zinc-900/60 border border-zinc-800 rounded-2xl overflow-hidden shadow-xl backdrop-blur-sm">
      <div
        onClick={() => setIsOpen(!isOpen)}
        className="px-6 py-4 flex items-center justify-between cursor-pointer hover:bg-zinc-800/40 transition-colors select-none"
      >
        <div className="flex items-center space-x-2.5">
          <div className="p-1.5 rounded-lg bg-orange-500/10 text-orange-500 border border-orange-500/20">
            <Code2 className="w-4 h-4" />
          </div>
          <div>
            <h3 className="text-sm font-semibold text-zinc-200">Raw JSON API Payload</h3>
            <p className="text-xs text-zinc-500">Inspect exact response structure from /api/v1/research</p>
          </div>
        </div>

        <div className="flex items-center space-x-3">
          <button
            onClick={handleCopy}
            className="flex items-center space-x-1 text-xs px-2.5 py-1.5 rounded-lg bg-zinc-950 border border-zinc-800 hover:border-orange-500/50 text-zinc-300 hover:text-orange-400 transition-all font-mono"
            title="Copy JSON to clipboard"
          >
            {copied ? (
              <>
                <Check className="w-3.5 h-3.5 text-emerald-400" />
                <span className="text-emerald-400">Copied!</span>
              </>
            ) : (
              <>
                <Copy className="w-3.5 h-3.5" />
                <span>Copy JSON</span>
              </>
            )}
          </button>

          {isOpen ? (
            <ChevronUp className="w-4 h-4 text-zinc-400" />
          ) : (
            <ChevronDown className="w-4 h-4 text-zinc-400" />
          )}
        </div>
      </div>

      {isOpen && (
        <div className="border-t border-zinc-800 bg-zinc-950 p-4 overflow-x-auto max-h-[450px]">
          <pre className="text-xs font-mono text-zinc-300 leading-relaxed">
            {jsonString}
          </pre>
        </div>
      )}
    </div>
  );
};
