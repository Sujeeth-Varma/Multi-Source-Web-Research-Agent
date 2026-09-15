import type { ResearchResponse } from '../types/research';

export const SAMPLE_RESEARCH_RESPONSE: ResearchResponse = {
  question: "what is langchain",
  answer: "LangChain is an open-source framework designed to simplify the process of building applications powered by large language models (LLMs) [source_1, source_4]. It provides developers with tools and abstractions that connect LLMs with external data sources, tools, and workflows, thereby improving customization, accuracy, and relevancy [source_1, source_4]. Available in both Python and JavaScript, LangChain helps streamline AI development for various use cases such as chatbots, question-answering systems, content generation, and summarizers [source_1, source_4].\n\n### Key Components\nLangChain supports several core components that facilitate complex workflows [source_4]:\n- **Chains:** Define sequences of steps where each step can utilize an LLM, process data, or invoke tools [source_4].\n- **Prompt Management:** Offers templates and tools to design, control, and manage inputs, outputs, and model behaviors [source_4].\n- **Agents:** LLM-driven components that dynamically decide which actions or APIs to call based on user input [source_4].\n- **Vector Databases:** Stores data as vector embeddings to enable similarity search for tasks like document search and Retrieval-Augmented Generation (RAG) [source_4].\n- **Models:** Supports integration with multiple LLMs (such as OpenAI and Hugging Face) for flexibility [source_4].\n- **Memory Management:** Maintains context from previous interactions to support ongoing conversations and multi-step tasks [source_4].\n\n### How It Works (RAG Workflow)\nLangChain enables context-aware workflows like Retrieval-Augmented Generation (RAG) to help LLMs reason over domain-specific data without requiring model retraining [source_1, source_4]. The workflow typically involves document processing (splitting documents into smaller chunks), creating embeddings, storing those embeddings in a vector database, performing a similarity search based on a user query, fetching relevant contextual information, and passing it to the LLM to generate an accurate response [source_4].\n\n### Uncertainties and Limitations\nWhile LangChain supports broad integrations and components, the exact details of how LangChain integrates with every proprietary database system are not fully specified in the available evidence.",
  key_claims: [
    {
      claim: "LangChain is an open source framework for building applications based on large language models (LLMs).",
      sources: ["source_1", "source_4"],
      status: "SUPPORTED"
    },
    {
      claim: "LangChain provides tools and abstractions to improve customization, accuracy, and relevancy, and connects LLMs with external data, tools, and workflows.",
      sources: ["source_1", "source_4"],
      status: "SUPPORTED"
    },
    {
      claim: "LangChain is available in both Python and JavaScript.",
      sources: ["source_4"],
      status: "SUPPORTED"
    },
    {
      claim: "LangChain supports key components such as chains, prompt management, agents, vector databases, models, and memory management.",
      sources: ["source_4"],
      status: "SUPPORTED"
    }
  ],
  sources: [
    {
      id: "source_1",
      title: "What is LangChain?",
      url: "https://aws.amazon.com/what-is/langchain",
      providers: ["serper"],
      score: 1.283
    },
    {
      id: "source_3",
      title: "LangChain: the open agent platform to own your intelligence",
      url: "https://www.langchain.com/",
      providers: ["serper"],
      score: 1.15
    },
    {
      id: "source_5",
      title: "What is LangChain?",
      url: "https://www.youtube.com/watch?v=1bUy-1hGZpI",
      providers: ["serper"],
      score: 0.983
    },
    {
      id: "source_2",
      title: "can someone explain Langchain in a simple manner",
      url: "https://www.reddit.com/r/LangChain/comments/1n0qam7/can_someone_explain_langchain_in_a_simple_manner",
      providers: ["serper"],
      score: 0.917
    },
    {
      id: "source_4",
      title: "Introduction to LangChain",
      url: "https://www.geeksforgeeks.org/artificial-intelligence/introduction-to-langchain",
      providers: ["serper"],
      score: 0.917
    },
    {
      id: "source_6",
      title: "Vector database (Wikipedia)",
      url: "https://en.wikipedia.org/wiki/Vector_database",
      providers: ["wikipedia"],
      score: 0.8
    },
    {
      id: "source_7",
      title: "List of artificial intelligence companies (Wikipedia)",
      url: "https://en.wikipedia.org/wiki/List_of_artificial_intelligence_companies",
      providers: ["wikipedia"],
      score: 0.8
    },
    {
      id: "source_8",
      title: "Agent harness (Wikipedia)",
      url: "https://en.wikipedia.org/wiki/Agent_harness",
      providers: ["wikipedia"],
      score: 0.8
    }
  ],
  conflicts: [],
  uncertainties: [
    "The exact details of how LangChain integrates with every proprietary database system are not fully specified."
  ],
  metadata: {
    providers_used: ["duckduckgo", "serper", "wikipedia"],
    failed_providers: [],
    total_queries: 1,
    sources_found: 15,
    sources_fetched: 5,
    sources_used: 8,
    execution_time_ms: 8545.17,
    partial_results: false,
    warning_notes: []
  }
};
