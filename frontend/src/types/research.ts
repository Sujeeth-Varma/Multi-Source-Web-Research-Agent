export interface ResearchRequest {
  question: string;
  max_sources?: number;
  enable_planning?: boolean;
}

export interface Source {
  id: string;
  title: string;
  url: string;
  providers: string[];
  score: number;
  snippet?: string;
}

export interface KeyClaim {
  claim: string;
  sources: string[];
  status: 'SUPPORTED' | 'CONTRADICTED' | 'UNVERIFIED' | string;
}

export interface ResearchMetadata {
  providers_used: string[];
  failed_providers: string[];
  total_queries: number;
  sources_found: number;
  sources_fetched: number;
  sources_used: number;
  execution_time_ms: number;
  partial_results: boolean;
  warning_notes: string[];
}

export interface ResearchResponse {
  question: string;
  answer: string;
  key_claims: KeyClaim[];
  sources: Source[];
  conflicts: string[];
  uncertainties: string[];
  metadata: ResearchMetadata;
}
