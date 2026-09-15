import { Activity, Clock, Search, AlertCircle, Cpu, CheckCircle2 } from 'lucide-react';
import type { ResearchMetadata } from '../types/research';

interface MetadataPanelProps {
  metadata: ResearchMetadata;
  uncertainties: string[];
  conflicts: string[];
}

export const MetadataPanel: React.FC<MetadataPanelProps> = ({ metadata, uncertainties, conflicts }) => {
  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
      {/* Metrics Card */}
      <div className="bg-zinc-900/60 border border-zinc-800 rounded-2xl p-5 shadow-xl backdrop-blur-sm md:col-span-2 space-y-4">
        <div className="flex items-center space-x-2.5 border-b border-zinc-800 pb-3">
          <div className="p-1.5 rounded-lg bg-orange-500/10 text-orange-500 border border-orange-500/20">
            <Activity className="w-4 h-4" />
          </div>
          <h3 className="text-sm font-semibold text-zinc-200">Execution Telemetry</h3>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
          <div className="p-3 rounded-xl bg-zinc-950/80 border border-zinc-800/80">
            <div className="flex items-center space-x-1.5 text-xs text-zinc-500 mb-1">
              <Clock className="w-3.5 h-3.5 text-orange-400" />
              <span>Execution</span>
            </div>
            <p className="text-lg font-mono font-bold text-orange-400">
              {metadata.execution_time_ms ? `${(metadata.execution_time_ms / 1000).toFixed(2)}s` : 'N/A'}
            </p>
          </div>

          <div className="p-3 rounded-xl bg-zinc-950/80 border border-zinc-800/80">
            <div className="flex items-center space-x-1.5 text-xs text-zinc-500 mb-1">
              <Search className="w-3.5 h-3.5 text-orange-400" />
              <span>Found</span>
            </div>
            <p className="text-lg font-mono font-bold text-zinc-100">
              {metadata.sources_found ?? 0}
            </p>
          </div>

          <div className="p-3 rounded-xl bg-zinc-950/80 border border-zinc-800/80">
            <div className="flex items-center space-x-1.5 text-xs text-zinc-500 mb-1">
              <Cpu className="w-3.5 h-3.5 text-orange-400" />
              <span>Fetched</span>
            </div>
            <p className="text-lg font-mono font-bold text-zinc-100">
              {metadata.sources_fetched ?? 0}
            </p>
          </div>

          <div className="p-3 rounded-xl bg-zinc-950/80 border border-zinc-800/80">
            <div className="flex items-center space-x-1.5 text-xs text-zinc-500 mb-1">
              <CheckCircle2 className="w-3.5 h-3.5 text-orange-400" />
              <span>Synthesized</span>
            </div>
            <p className="text-lg font-mono font-bold text-zinc-100">
              {metadata.sources_used ?? 0}
            </p>
          </div>
        </div>

        {/* Providers list */}
        <div className="flex items-center justify-between text-xs pt-1">
          <span className="text-zinc-400 font-medium">Search Providers Used:</span>
          <div className="flex items-center space-x-2">
            {metadata.providers_used?.map((p) => (
              <span
                key={p}
                className="px-2.5 py-1 rounded-md bg-zinc-950 border border-zinc-800 text-orange-300 font-mono text-[11px]"
              >
                {p}
              </span>
            ))}
          </div>
        </div>
      </div>

      {/* Uncertainties & Limitations Card */}
      <div className="bg-zinc-900/60 border border-zinc-800 rounded-2xl p-5 shadow-xl backdrop-blur-sm space-y-3 flex flex-col justify-between">
        <div>
          <div className="flex items-center space-x-2 border-b border-zinc-800 pb-3 mb-3">
            <AlertCircle className="w-4 h-4 text-amber-500" />
            <h3 className="text-sm font-semibold text-zinc-200">Uncertainties & Scope</h3>
          </div>

          {uncertainties && uncertainties.length > 0 ? (
            <ul className="space-y-2 text-xs text-zinc-400">
              {uncertainties.map((item, idx) => (
                <li key={idx} className="flex items-start space-x-2">
                  <span className="text-amber-500 font-bold">•</span>
                  <span className="leading-relaxed">{item}</span>
                </li>
              ))}
            </ul>
          ) : (
            <p className="text-xs text-zinc-500 italic">No evidence conflicts or uncertainties detected.</p>
          )}
        </div>

        {conflicts && conflicts.length > 0 && (
          <div className="pt-2 border-t border-zinc-800/80">
            <span className="text-xs font-semibold text-rose-400">Conflicts Found:</span>
            <p className="text-xs text-rose-300/80 mt-1">{conflicts.join(', ')}</p>
          </div>
        )}
      </div>
    </div>
  );
};
