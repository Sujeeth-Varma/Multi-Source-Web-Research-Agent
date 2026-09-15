import { Sparkles, ExternalLink } from 'lucide-react';
import type { Source } from '../types/research';

interface AnswerCardProps {
  answer: string;
  sources: Source[];
  onSelectSource?: (sourceId: string) => void;
}

export const AnswerCard: React.FC<AnswerCardProps> = ({ answer, sources, onSelectSource }) => {
  // Helper to render inline citations formatted like [source_1, source_4]
  const renderFormattedText = (text: string) => {
    // Split by sections or markdown blocks
    const lines = text.split('\n');

    return lines.map((line, idx) => {
      // Check if line is a header ###
      if (line.startsWith('### ')) {
        return (
          <h3 key={idx} className="text-lg font-bold text-orange-400 mt-6 mb-3 flex items-center gap-2">
            <span className="w-1.5 h-4 bg-orange-500 rounded-full inline-block"></span>
            {line.replace('### ', '')}
          </h3>
        );
      }

      // Check if bullet point
      const isBullet = line.trim().startsWith('-');
      const cleanLine = isBullet ? line.trim().substring(1).trim() : line;

      // Parse citations like [source_1, source_4] or [source_1]
      const parts = cleanLine.split(/(\[source_\d+(?:,\s*source_\d+)*\])/g);

      const content = parts.map((part, pIdx) => {
        const citationMatch = part.match(/^\[(.*)\]$/);
        if (citationMatch) {
          const sourceIds = citationMatch[1].split(',').map((s) => s.trim());
          return (
            <span key={pIdx} className="inline-flex items-center gap-1 mx-1 my-0.5">
              {sourceIds.map((sid) => {
                const src = sources.find((s) => s.id === sid);
                return (
                  <button
                    key={sid}
                    onClick={() => onSelectSource?.(sid)}
                    className="inline-flex items-center space-x-1 text-[11px] font-mono px-2 py-0.5 rounded-md bg-orange-500/15 text-orange-300 border border-orange-500/30 hover:bg-orange-500/30 hover:border-orange-500 transition-all group"
                    title={src ? `${src.title} (${src.url})` : sid}
                  >
                    <span>{sid}</span>
                    <ExternalLink className="w-2.5 h-2.5 opacity-60 group-hover:opacity-100" />
                  </button>
                );
              })}
            </span>
          );
        }

        // Parse bold **text**
        const boldParts = part.split(/(\*\*.*?\*\*)/g);
        return boldParts.map((bPart, bIdx) => {
          if (bPart.startsWith('**') && bPart.endsWith('**')) {
            return (
              <strong key={bIdx} className="font-semibold text-zinc-100">
                {bPart.slice(2, -2)}
              </strong>
            );
          }
          return bPart;
        });
      });

      if (!line.trim()) {
        return <div key={idx} className="h-3" />;
      }

      if (isBullet) {
        return (
          <li key={idx} className="ml-4 list-disc text-zinc-300 leading-relaxed text-sm my-1 marker:text-orange-500">
            {content}
          </li>
        );
      }

      return (
        <p key={idx} className="text-zinc-300 leading-relaxed text-sm sm:text-base my-2">
          {content}
        </p>
      );
    });
  };

  return (
    <div className="bg-zinc-900/60 border border-zinc-800 rounded-2xl p-6 shadow-xl backdrop-blur-sm relative">
      {/* Card Header */}
      <div className="flex items-center justify-between border-b border-zinc-800 pb-4 mb-4">
        <div className="flex items-center space-x-2.5">
          <div className="p-2 rounded-lg bg-orange-500/10 text-orange-500 border border-orange-500/20">
            <Sparkles className="w-5 h-5" />
          </div>
          <div>
            <h2 className="text-base font-semibold text-zinc-100">Synthesized Answer</h2>
            <p className="text-xs text-zinc-400">Grounded evidence synthesis with inline citations</p>
          </div>
        </div>

        <div className="text-xs px-2.5 py-1 rounded-full bg-zinc-950 border border-zinc-800 text-zinc-400 font-mono">
          {sources.length} Sources Cited
        </div>
      </div>

      {/* Answer Content */}
      <div className="prose prose-invert max-w-none text-zinc-200">
        {renderFormattedText(answer)}
      </div>
    </div>
  );
};
