import { Sparkles, Terminal } from 'lucide-react';

interface HeaderProps {
  apiStatus: 'idle' | 'loading' | 'success' | 'error';
}

export const Header: React.FC<HeaderProps> = ({ apiStatus }) => {
  return (
    <header className="border-b border-zinc-800/80 bg-zinc-950/80 backdrop-blur-md sticky top-0 z-40">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        {/* Logo and branding */}
        <div className="flex items-center space-x-3">
          <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-orange-600 via-orange-500 to-amber-400 p-0.5 shadow-lg shadow-orange-500/20">
            <div className="w-full h-full bg-zinc-950 rounded-[10px] flex items-center justify-center">
              <Sparkles className="w-5 h-5 text-orange-500" />
            </div>
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <span className="font-bold text-lg text-zinc-100 tracking-tight">ZEPHRA</span>
              <span className="text-xs font-semibold px-2 py-0.5 rounded-full bg-orange-500/10 text-orange-400 border border-orange-500/20 uppercase tracking-widest">
                AI Research
              </span>
            </div>
            <p className="text-xs text-zinc-500 hidden sm:block">Multi-Source Research & Claim Verification Engine</p>
          </div>
        </div>

        {/* Right status badges */}
        <div className="flex items-center space-x-4">
          <div className="flex items-center space-x-2 px-3 py-1.5 rounded-lg bg-zinc-900/90 border border-zinc-800 text-xs">
            <span className="relative flex h-2 w-2">
              <span className={`animate-ping absolute inline-flex h-full w-full rounded-full opacity-75 ${
                apiStatus === 'loading' ? 'bg-amber-400' : 'bg-orange-400'
              }`}></span>
              <span className={`relative inline-flex rounded-full h-2 w-2 ${
                apiStatus === 'loading' ? 'bg-amber-500' : 'bg-orange-500'
              }`}></span>
            </span>
            <span className="text-zinc-400 font-medium">
              {apiStatus === 'loading' ? 'Researching...' : 'API Active'}
            </span>
          </div>

          <a
            href="http://localhost:8000/docs"
            target="_blank"
            rel="noopener noreferrer"
            className="hidden md:flex items-center space-x-1.5 text-xs text-zinc-400 hover:text-orange-400 transition-colors px-2.5 py-1.5 rounded-lg hover:bg-zinc-900 border border-transparent hover:border-zinc-800"
          >
            <Terminal className="w-3.5 h-3.5" />
            <span>FastAPI Docs</span>
          </a>
        </div>
      </div>
    </header>
  );
};
