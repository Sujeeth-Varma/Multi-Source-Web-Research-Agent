import { useState } from 'react';
import { Header } from './components/Header';
import { ResearchForm } from './components/ResearchForm';
import { AnswerCard } from './components/AnswerCard';
import { KeyClaimsCard } from './components/KeyClaimsCard';
import { SourcesGrid } from './components/SourcesGrid';
import { MetadataPanel } from './components/MetadataPanel';
import { JsonViewer } from './components/JsonViewer';
import type { ResearchRequest, ResearchResponse } from './types/research';
import { SAMPLE_RESEARCH_RESPONSE } from './mock/sampleData';
import { executeResearch } from './services/api';
import { Sparkles, AlertTriangle } from 'lucide-react';

export function App() {
  const [data, setData] = useState<ResearchResponse | null>(SAMPLE_RESEARCH_RESPONSE);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [selectedSourceId, setSelectedSourceId] = useState<string | null>(null);

  const handleResearchSubmit = async (request: ResearchRequest) => {
    setLoading(true);
    setError(null);
    setSelectedSourceId(null);

    try {
      const res = await executeResearch(request);
      setData(res);
    } catch (err: any) {
      console.error('Research error:', err);
      const errMsg = err.response?.data?.detail?.message || err.message || 'Failed to execute research query.';
      setError(errMsg);
    } finally {
      setLoading(false);
    }
  };

  const handleLoadSample = () => {
    setError(null);
    setSelectedSourceId(null);
    setData(SAMPLE_RESEARCH_RESPONSE);
  };

  const handleSelectSource = (sourceId: string) => {
    setSelectedSourceId(sourceId);
    const element = document.getElementById(`source-card-${sourceId}`);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
  };

  return (
    <div className="min-h-screen bg-[#09090b] text-zinc-100 font-sans selection:bg-orange-500/30 selection:text-orange-200">
      {/* Navbar */}
      <Header apiStatus={loading ? 'loading' : error ? 'error' : 'idle'} />

      {/* Main Container */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
        {/* Intro / Title Banner */}
        <div className="text-center max-w-2xl mx-auto space-y-2">
          <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-orange-500/10 border border-orange-500/20 text-orange-400 text-xs font-semibold mb-1">
            <Sparkles className="w-3.5 h-3.5" />
            <span>AI Web Research & Grounding API</span>
          </div>
          <h1 className="text-3xl sm:text-4xl font-extrabold tracking-tight text-zinc-100">
            Intelligent Research Engine
          </h1>
          <p className="text-sm text-zinc-400">
            Retrieves web sources across providers, deduplicates URLs, verifies key claims, and synthesizes cited answers.
          </p>
        </div>

        {/* Query Input Form */}
        <ResearchForm
          onSubmit={handleResearchSubmit}
          onLoadSample={handleLoadSample}
          isLoading={loading}
        />

        {/* Error Alert */}
        {error && (
          <div className="bg-rose-950/30 border border-rose-500/30 rounded-2xl p-4 flex items-center space-x-3 text-rose-300 text-sm">
            <AlertTriangle className="w-5 h-5 shrink-0 text-rose-400" />
            <div className="flex-1">
              <p className="font-semibold">Research Error</p>
              <p className="text-xs text-rose-400/80">{error}</p>
            </div>
            <button
              onClick={handleLoadSample}
              className="text-xs px-3 py-1.5 rounded-lg bg-rose-500/20 hover:bg-rose-500/30 border border-rose-500/30 text-rose-200 font-medium transition-colors"
            >
              Load Sample Response
            </button>
          </div>
        )}

        {/* Results Sections */}
        {data && (
          <div className="space-y-8 animate-fade-in">
            {/* Top Answer Block */}
            <AnswerCard
              answer={data.answer}
              sources={data.sources}
              onSelectSource={handleSelectSource}
            />

            {/* Key Claims Verification */}
            <KeyClaimsCard
              claims={data.key_claims}
              onSelectSource={handleSelectSource}
            />

            {/* Metadata Telemetry & Scope */}
            <MetadataPanel
              metadata={data.metadata}
              uncertainties={data.uncertainties}
              conflicts={data.conflicts}
            />

            {/* Sources Grid */}
            <SourcesGrid
              sources={data.sources}
              selectedSourceId={selectedSourceId}
              onSelectSource={handleSelectSource}
            />

            {/* Raw JSON Payload Accordion */}
            <JsonViewer data={data} />
          </div>
        )}
      </main>

      {/* Minimal Footer */}
      <footer className="border-t border-zinc-900 py-6 text-center text-xs text-zinc-600 mt-12">
        <p>ZEPHRA AI Assignment • Minimalist Dark & Orange Interface</p>
      </footer>
    </div>
  );
}

export default App;