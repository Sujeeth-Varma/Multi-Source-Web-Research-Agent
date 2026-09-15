import { CheckCircle2, AlertTriangle, XCircle, ShieldCheck, Link2 } from 'lucide-react';
import type { KeyClaim } from '../types/research';

interface KeyClaimsCardProps {
  claims: KeyClaim[];
  onSelectSource?: (sourceId: string) => void;
}

export const KeyClaimsCard: React.FC<KeyClaimsCardProps> = ({ claims, onSelectSource }) => {
  if (!claims || claims.length === 0) return null;

  const getStatusBadge = (status: string) => {
    switch (status.toUpperCase()) {
      case 'SUPPORTED':
        return (
          <span className="inline-flex items-center space-x-1 text-xs font-semibold px-2.5 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
            <CheckCircle2 className="w-3.5 h-3.5" />
            <span>SUPPORTED</span>
          </span>
        );
      case 'CONTRADICTED':
        return (
          <span className="inline-flex items-center space-x-1 text-xs font-semibold px-2.5 py-0.5 rounded-full bg-rose-500/10 text-rose-400 border border-rose-500/20">
            <XCircle className="w-3.5 h-3.5" />
            <span>CONTRADICTED</span>
          </span>
        );
      default:
        return (
          <span className="inline-flex items-center space-x-1 text-xs font-semibold px-2.5 py-0.5 rounded-full bg-amber-500/10 text-amber-400 border border-amber-500/20">
            <AlertTriangle className="w-3.5 h-3.5" />
            <span>{status}</span>
          </span>
        );
    }
  };

  return (
    <div className="bg-zinc-900/60 border border-zinc-800 rounded-2xl p-6 shadow-xl backdrop-blur-sm">
      <div className="flex items-center space-x-2.5 border-b border-zinc-800 pb-4 mb-4">
        <div className="p-2 rounded-lg bg-orange-500/10 text-orange-500 border border-orange-500/20">
          <ShieldCheck className="w-5 h-5" />
        </div>
        <div>
          <h2 className="text-base font-semibold text-zinc-100">Key Claims Verification</h2>
          <p className="text-xs text-zinc-400">Claims extracted and verified against fetched web evidence</p>
        </div>
      </div>

      <div className="space-y-3">
        {claims.map((claimItem, idx) => (
          <div
            key={idx}
            className="p-4 rounded-xl bg-zinc-950/80 border border-zinc-800/80 hover:border-zinc-700 transition-all flex flex-col sm:flex-row sm:items-center justify-between gap-3"
          >
            <div className="space-y-1.5 flex-1">
              <p className="text-sm font-medium text-zinc-200 leading-snug">
                "{claimItem.claim}"
              </p>
              
              <div className="flex flex-wrap items-center gap-1.5 pt-1">
                <span className="text-[11px] text-zinc-500 flex items-center gap-1">
                  <Link2 className="w-3 h-3 text-zinc-500" /> Evidence:
                </span>
                {claimItem.sources.map((sid) => (
                  <button
                    key={sid}
                    onClick={() => onSelectSource?.(sid)}
                    className="text-[10px] font-mono px-2 py-0.5 rounded bg-zinc-900 text-orange-400 border border-zinc-800 hover:border-orange-500/50 hover:bg-orange-500/10 transition-all"
                  >
                    {sid}
                  </button>
                ))}
              </div>
            </div>

            <div className="shrink-0 self-start sm:self-center">
              {getStatusBadge(claimItem.status)}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
