import { ExternalLink, Globe, Layers, Award } from 'lucide-react';
import type { Source } from '../types/research';

interface SourcesGridProps {
  sources: Source[];
  selectedSourceId: string | null;
  onSelectSource: (sourceId: string) => void;
}

export const SourcesGrid: React.FC<SourcesGridProps> = ({ sources, selectedSourceId, onSelectSource }) => {
  if (!sources || sources.length === 0) return null;

  return (
    <div className="bg-zinc-900/60 border border-zinc-800 rounded-2xl p-6 shadow-xl backdrop-blur-sm">
      <div className="flex items-center justify-between border-b border-zinc-800 pb-4 mb-4">
        <div className="flex items-center space-x-2.5">
          <div className="p-2 rounded-lg bg-orange-500/10 text-orange-500 border border-orange-500/20">
            <Layers className="w-5 h-5" />
          </div>
          <div>
            <h2 className="text-base font-semibold text-zinc-100">Retrieved & Ranked Sources</h2>
            <p className="text-xs text-zinc-400">Deduplicated sources evaluated for relevance and accuracy</p>
          </div>
        </div>

        <div className="text-xs text-zinc-500 font-mono">
          {sources.length} Items
        </div>
      </div>

      {/* Grid of sources */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {sources.map((src) => {
          const isSelected = selectedSourceId === src.id;
          const hostname = new URL(src.url).hostname.replace('www.', '');

          return (
            <div
              key={src.id}
              id={`source-card-${src.id}`}
              onClick={() => onSelectSource(src.id)}
              className={`p-4 rounded-xl border transition-all duration-200 cursor-pointer flex flex-col justify-between ${
                isSelected
                  ? 'bg-orange-950/20 border-orange-500 ring-2 ring-orange-500/20 shadow-lg shadow-orange-500/10'
                  : 'bg-zinc-950/80 border-zinc-800 hover:border-zinc-700 hover:bg-zinc-900/80'
              }`}
            >
              <div>
                {/* Source header info */}
                <div className="flex items-center justify-between gap-2 mb-2">
                  <div className="flex items-center space-x-2">
                    <span className="font-mono text-xs font-bold text-orange-400 px-2 py-0.5 rounded bg-orange-500/10 border border-orange-500/20">
                      {src.id}
                    </span>

                    {/* Providers badges */}
                    {src.providers.map((p) => (
                      <span
                        key={p}
                        className="text-[10px] font-semibold uppercase px-2 py-0.5 rounded bg-zinc-900 text-zinc-400 border border-zinc-800"
                      >
                        {p}
                      </span>
                    ))}
                  </div>

                  {/* Score badge */}
                  <div className="flex items-center space-x-1 text-xs text-zinc-400 font-mono" title="Relevance Score">
                    <Award className="w-3.5 h-3.5 text-amber-500" />
                    <span>{src.score.toFixed(2)}</span>
                  </div>
                </div>

                {/* Title */}
                <h4 className="text-sm font-semibold text-zinc-200 line-clamp-2 hover:text-orange-300 transition-colors mb-2">
                  {src.title}
                </h4>
              </div>

              {/* Footer link */}
              <div className="pt-3 mt-2 border-t border-zinc-800/60 flex items-center justify-between text-xs">
                <div className="flex items-center space-x-1.5 text-zinc-400 truncate max-w-[80%]">
                  <Globe className="w-3.5 h-3.5 shrink-0 text-zinc-500" />
                  <span className="truncate">{hostname}</span>
                </div>

                <a
                  href={src.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  onClick={(e) => e.stopPropagation()}
                  className="text-orange-400 hover:text-orange-300 font-medium flex items-center space-x-1 text-[11px] px-2 py-1 rounded hover:bg-orange-500/10 transition-colors"
                >
                  <span>Open</span>
                  <ExternalLink className="w-3 h-3" />
                </a>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
