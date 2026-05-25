# Project Roadmap - Self-Corrective RAG System

This roadmap details the sequential execution phases to build, refine, and deploy the Self-Corrective RAG system. It is designed to allow step-by-step progress, verifying correctness at each stage before moving forward.

---

## Development Phases

### Phase 1: Environment & Project Scaffolding
*   **Goal**: Initialize project directories, virtual environment, dependency management, and foundational system architecture documentation.
*   **Tasks**:
    *   [x] Create Python virtual environment using `uv`.
    *   [x] Install required packages (`langgraph`, `langchain-google-genai`, `chromadb`, etc.).
    *   [x] Author documentation blueprints (`project_overview.md`, `architecture.md`, `roadmap.md`, `tasks.md`).
    *   [ ] Configure `.env` files and Git ignores.
*   **Outcome**: A functional Python environment with verified installations and approved blueprints.

---

### Phase 2: Ingestion Pipeline & Local Retrieval (Epic 1)
*   **Goal**: Load, split, embed, and store source documents locally.
*   **Tasks**:
    *   [ ] Implement a directory data loader (`app/retrieval/loader.py`).
    *   [ ] Build embedding logic using Google's `text-embedding-004` (`app/retrieval/embedder.py`).
    *   [ ] Setup ChromaDB connection and setup schema to store document text and metadata (`app/retrieval/vectorstore.py`).
    *   [ ] Write a CLI ingestion script (`ingest.py`) to feed sample datasets into the system.
*   **Outcome**: A local vector database containing embedded files, capable of running fast semantic searches.

---

### Phase 3: LLM Synthesis & Critique Graders (Epic 2)
*   **Goal**: Connect to Gemini 1.5 Flash and implement LLM grading components using Pydantic structured outputs.
*   **Tasks**:
    *   [ ] Configure `langchain_google_genai` API bindings.
    *   [ ] Define prompt templates for: Document Relevance, Hallucination Check, and Answer Utility.
    *   [ ] Write critique modules returning structured boolean grades (`app/critique/graders.py`).
    *   [ ] Implement the baseline generation engine (`app/generation/synthesizer.py`).
*   **Outcome**: Independent, unit-tested grader functions that can reliably assess document relevance, hallucinations, and query satisfaction.

---

### Phase 4: Web Search Fallback Mechanism (Epic 3)
*   **Goal**: Build a system that reformulates user queries and runs Web Search when local retrieval is lacking.
*   **Tasks**:
    *   [ ] Implement query reformulation prompts (translating a conversational query into an optimized web-search query).
    *   [ ] Integrate DuckDuckGo programmatic search (`app/utils/search.py`).
    *   [ ] Build logic to parse search results into standardized document objects.
*   **Outcome**: A standalone tool that can convert a complex question into optimized search terms and return relevant web context for free.

---

### Phase 5: LangGraph Stateful Orchestration (Epic 3 Continued)
*   **Goal**: Wire all individual components into a cyclical, stateful execution graph using LangGraph.
*   **Tasks**:
    *   [ ] Define the `GraphState` dictionary and type models.
    *   [ ] Code the workflow nodes (`app/workflows/nodes.py`).
    *   [ ] Code the conditional routing edges (`app/workflows/edges.py`).
    *   [ ] Compile the graph using `StateGraph` and implement visual graph rendering.
*   **Outcome**: A compiled, robust, state-driven workflow capable of self-critiquing, searching, and repeating nodes dynamically.

---

### Phase 6: Interface, Verification & Refinement
*   **Goal**: Put the system to the test, run evaluations, and polish the user experience.
*   **Tasks**:
    *   [ ] Build an interactive terminal console (`app/main.py`) with colored, descriptive logging.
    *   [ ] Write automated tests in the `tests/` directory to simulate edge cases (e.g., questions with perfect database answers vs. questions requiring web fallback).
    *   [ ] Review LLM usage metrics to ensure maximum efficiency.
*   **Outcome**: A polished, ready-to-run Self-Corrective RAG application with verified reliability.
