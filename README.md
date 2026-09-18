# Multi-Source Web Research Agent

A full-stack, enterprise-grade web research platform designed to automate natural language web research, cross-source fact verification, and grounded answer synthesis. The system orchestrates multi-provider web retrieval, canonical URL deduplication, asynchronous page scraping, domain-relevance ranking, claim verification, and citation-backed synthesis with full tracing and observability.

---

## Architecture Overview

The system consists of a Python FastAPI backend implementing an asynchronous research orchestration pipeline and a modern React + TypeScript frontend built with Vite and Tailwind CSS.

```
                    +--------------------------------+
                    |        React Frontend          |
                    | (Vite, TypeScript, Tailwind)   |
                    +---------------+----------------+
                                    |
                                    | HTTP POST /api/v1/research
                                    v
                    +---------------+----------------+
                    |       FastAPI Backend          |
                    |    Research Orchestrator       |
                    +---------------+----------------+
                                    |
        +---------------------------+---------------------------+
        |                           |                           |
        v                           v                           v
+---------------+           +---------------+           +---------------+
|    Serper     |           |   Wikipedia   |           |  DuckDuckGo   |
| Search API    |           | Search API    |           | Search Engine |
+-------+-------+           +-------+-------+           +-------+-------+
        |                           |                           |
        +---------------------------+---------------------------+
                                    |
                                    v
                    +---------------+----------------+
                    |      Source Deduplication      |
                    |  & URL Canonical Normalization  |
                    +---------------+----------------+
                                    |
                                    v
                    +---------------+----------------+
                    |  Async Web Fetching & Parsing  |
                    |   (HTTPX + Trafilatura/BS4)    |
                    +---------------+----------------+
                                    |
                                    v
                    +---------------+----------------+
                    |    Source Relevance Ranking    |
                    |    & Quality Filtering         |
                    +---------------+----------------+
                                    |
                                    v
                    +---------------+----------------+
                    |   Gemini Claim Verification    |
                    |  (Status, Contradictions,      |
                    |   Uncertainties Detection)     |
                    +---------------+----------------+
                                    |
                                    v
                    +---------------+----------------+
                    |   Grounded Synthesis Engine    |
                    |    (In-text Citation Mapping)  |
                    +---------------+----------------+
                                    |
                                    v
                    +---------------+----------------+
                    |  Langfuse Observability Trace  |
                    +--------------------------------+
```

---

## Key Features

- **Multi-Provider Web Search**: Queries Serper API, DuckDuckGo, and Wikipedia concurrently to maximize research breadth. Supports fallback mechanisms if primary search providers fail.
- **Canonical URL Deduplication**: Standardizes incoming search result URLs by normalizing schemes, lowercasing hostnames, stripping tracking parameters (`utm_*`, `fbclid`, `gclid`), and resolving canonical paths.
- **Asynchronous Content Fetching**: Concurrently fetches web page contents with strict timeout protection (10 seconds) and response payload byte limits (500 KB limit per source).
- **Source Relevance Ranking**: Evaluates fetched content using TF-IDF term coverage, domain authority metrics, and freshness indicators to score and rank top sources.
- **Gemini Claim Verification**: Extracts core claims from retrieved documents, tags verification statuses (`VERIFIED`, `CONTRADICTED`, `UNCERTAIN`), and flags conflicting statements across sources.
- **Citation-Backed Synthesis**: Generates grounded synthesis reports referencing specific source IDs, ensuring transparent provenance and preventing hallucinations.
- **Observability & Tracing**: Integrates with Langfuse to provide complete visibility into planning, search queries, execution latency, token usage, and pipeline failure modes.

---

## Technology Stack

### Backend
- **Language**: Python 3.12+
- **Framework**: FastAPI, Uvicorn
- **Package Management**: UV
- **Data Validation & Settings**: Pydantic v2, Pydantic-Settings
- **LLM Integration**: Google Gemini via `langchain-google-genai`
- **Search & Scraping**: `httpx`, `beautifulsoup4`, `trafilatura`, `duckduckgo-search`, `ddgs`
- **Observability**: Langfuse Python SDK (`langfuse`)
- **Testing**: Pytest, Pytest-Asyncio, Pytest-Mock

### Frontend
- **Framework**: React 19, Vite 8
- **Language**: TypeScript 6
- **Styling**: Tailwind CSS v4, Lucide React icons
- **HTTP Client**: Axios
- **Linting & Code Quality**: Oxlint

---

## Project Structure

```
zephraai-assignment/
├── backend/
│   ├── src/
│   │   └── backend/
│   │       ├── api/            # API endpoints and route definitions
│   │       │   └── research.py # Main research endpoint (/api/v1/research)
│   │       ├── core/           # Core configuration and exception definitions
│   │       │   ├── config.py   # Pydantic Settings application configuration
│   │       │   └── exceptions.py
│   │       ├── models/         # Pydantic schemas for requests, responses, and internal models
│   │       ├── observability/  # Langfuse tracing setup
│   │       ├── orchestrator/   # Pipeline execution engine (ResearchOrchestrator)
│   │       ├── providers/      # Search provider abstractions (Serper, DuckDuckGo, Wikipedia)
│   │       └── services/       # Domain services (Planner, Deduplicator, Fetcher, Ranker, Verifier, Synthesizer)
│   ├── tests/                  # Unit and integration test suite
│   ├── .env.example            # Backend environment template
│   └── pyproject.toml          # Python project definitions and dependencies
├── frontend/
│   ├── src/
│   │   ├── components/         # Modular UI components (SearchInput, SourceCard, ClaimMatrix, SynthesisReport)
│   │   ├── services/           # Axios API client setup
│   │   ├── types/              # TypeScript interface definitions matching backend schemas
│   │   ├── App.tsx             # Main dashboard shell
│   │   └── main.tsx            # Application entry point
│   ├── package.json            # Node.js dependencies and build scripts
│   └── vite.config.ts          # Vite configuration
└── README.md                   # Project documentation
```

---

## Prerequisites

- **Python**: Version 3.12 or higher
- **Node.js**: Version 18.0 or higher (with `npm`)
- **Package Manager**: `uv` (recommended for backend management) or `pip`

---

## Getting Started

### 1. Environment Configuration

Navigate to the `backend/` directory and set up your environment variables:

```bash
cd backend
cp .env.example .env
```

Configure the following variables in `backend/.env`:

```env
# Required API Keys
GEMINI_API_KEY=your_google_gemini_api_key

# Optional Search Provider Keys (DuckDuckGo and Wikipedia operate without keys)
SERPER_API_KEY=your_serper_api_key

# Model Selection
GEMINI_MODEL=gemini-3.5-flash-lite

# Optional Observability Configuration
LANGFUSE_PUBLIC_KEY=your_langfuse_public_key
LANGFUSE_SECRET_KEY=your_langfuse_secret_key
LANGFUSE_HOST=https://cloud.langfuse.com

# System Settings
LOG_LEVEL=INFO
MAX_PLANNING_QUERIES=4
MAX_SEARCH_RESULTS_PER_QUERY=5
MAX_SOURCES_TO_FETCH=8
HTTP_TIMEOUT_SECONDS=10.0
MAX_CONTENT_BYTES=500000
```

### 2. Backend Installation and Execution

Using `uv` (recommended):

```bash
cd backend
uv sync
uv run uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

Alternatively using traditional `pip` and virtual environment:

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

The backend server will start at `http://localhost:8000`. You can inspect interactive OpenAPI documentation at `http://localhost:8000/docs`.

### 3. Frontend Installation and Execution

Navigate to the `frontend/` directory, install dependencies, and start the development server:

```bash
cd frontend
npm install
npm run dev
```

The frontend application will run at `http://localhost:5173`.

---

## API Documentation

### Research Endpoint

`POST /api/v1/research`

Executes a complete multi-source research workflow for a user-provided question.

#### Request Payload

```json
{
  "question": "What are the latest developments in quantum computing algorithms?",
  "enable_planning": true,
  "max_sources": 6
}
```

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `question` | String | Yes | N/A | The research query or prompt to analyze. |
| `enable_planning` | Boolean | No | `true` | Whether to expand the input query into targeted sub-queries. |
| `max_sources` | Integer | No | `8` | Maximum number of ranked sources to include in synthesis. |

#### Response Payload

```json
{
  "question": "What are the latest developments in quantum computing algorithms?",
  "answer": "Recent developments in quantum computing algorithms focus on variational quantum algorithms (VQAs), fault-tolerant error mitigation, and quantum chemistry simulations [S1][S3]...",
  "key_claims": [
    {
      "claim": "Variational Quantum Eigensolvers have achieved lower error rates in chemical simulations.",
      "sources": ["S1", "S3"],
      "status": "VERIFIED"
    }
  ],
  "sources": [
    {
      "id": "S1",
      "title": "Advances in Quantum Algorithms - Nature",
      "url": "https://example.com/quantum-advances",
      "providers": ["serper"],
      "score": 0.89
    }
  ],
  "conflicts": [],
  "uncertainties": [],
  "metadata": {
    "providers_used": ["serper", "wikipedia"],
    "failed_providers": [],
    "total_queries": 3,
    "sources_found": 12,
    "sources_fetched": 8,
    "sources_used": 6,
    "execution_time_ms": 3420.5,
    "partial_results": false,
    "warning_notes": []
  }
}
```

### Health Check Endpoint

`GET /health`

Returns system readiness status.

#### Response

```json
{
  "status": "ok"
}
```

---

## Testing & Quality Assurance

### Backend Unit & Integration Tests

To run the backend test suite, execute pytest inside the `backend/` directory:

```bash
cd backend
uv run pytest
```

To run tests with detailed output and coverage:

```bash
cd backend
uv run pytest -v -s
```

### Frontend Code Quality

To lint the frontend codebase:

```bash
cd frontend
npm run lint
```

To run TypeScript verification and production build:

```bash
cd frontend
npm run build
```