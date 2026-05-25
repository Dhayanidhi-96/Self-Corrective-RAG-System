# Master Tasks List - Self-Corrective RAG System

This task list serves as the tracking log for the features and code modules of this project.

---

## Phase 1: Environment & Project Scaffolding
- [x] Create Python virtual environment using `uv`
- [x] Install initial package dependencies (`langgraph`, `langchain-google-genai`, `chromadb`, `duckduckgo-search`, `python-dotenv`)
- [x] Author system design documents:
  - [x] `docs/project_overview.md` (Workflow & Goals)
  - [x] `docs/architecture.md` (Components & Schemas)
  - [x] `docs/roadmap.md` (Development Phases)
  - [x] `docs/tasks.md` (Master Task List)
- [ ] Configure local environment values (Create `.env.example` and `.env`)

---

## Phase 2: Knowledge Ingestion & Vector Storage (Epic 1)
- [ ] Implement data loaders in `app/retrieval/loader.py`
  - [ ] Implement text file loader
  - [ ] Implement markdown file loader
- [ ] Implement text splitting configurations (recursive splitting by character)
- [ ] Create `app/retrieval/vectorstore.py`
  - [ ] Initialize local ChromaDB client (in-memory or local persistent directory)
  - [ ] Create/retrieve collections
  - [ ] Implement semantic document retrieval function
- [ ] Write CLI dataset ingestion script `ingest.py`
- [ ] Verify ingestion pipeline by uploading a few markdown test documents

---

## Phase 3: LLM Generation & Grader Critique Agents (Epic 2)
- [ ] Verify Google AI Studio API connections
- [ ] Implement Grader agents in `app/critique/graders.py` using Pydantic structured output:
  - [ ] Document Relevance Grader (Assess retrieved chunk relevance)
  - [ ] Hallucination Grader (Verify answer is grounded in chunks)
  - [ ] Answer Utility Grader (Check if answer matches original query)
- [ ] Implement generative model in `app/generation/synthesizer.py`
  - [ ] Write context-aware system prompts
  - [ ] Generate responses using `gemini-1.5-flash`

---

## Phase 4: Fallback Search Mechanics (Epic 3)
- [ ] Implement query reformulation in `app/utils/search.py`
  - [ ] Prompt LLM to optimize user conversational query for web search
- [ ] Implement programmatic DuckDuckGo search function in `app/utils/search.py`
- [ ] Build search results parser (convert HTML snippets into standard `Document` chunks with metadata)

---

## Phase 5: Stateful LangGraph Orchestration (Epic 3 Continued)
- [ ] Define `GraphState` schema in `app/workflows/state.py`
- [ ] Implement workflow nodes in `app/workflows/nodes.py`
  - [ ] `retrieve` node
  - [ ] `grade_documents` node
  - [ ] `generate` node
  - [ ] `web_search` node
- [ ] Implement routing logic in `app/workflows/edges.py`
  - [ ] `decide_to_generate` (Route to search vs. synthesis)
  - [ ] `grade_generation` (Verify hallucination/utility and route to endpoint or retry)
- [ ] Construct, compile, and visualize graph in `app/workflows/graph.py`

---

## Phase 6: Interface, Console & Verification Tests
- [ ] Build command-line client `app/main.py`
  - [ ] Add interactive input loop
  - [ ] Print detailed, color-coded execution steps to visually track graph transitions
- [ ] Write automated verification tests in the `tests/` directory
- [ ] Create test fixtures for:
  - [ ] Question answering strictly using local files
  - [ ] Question answering triggering web search fallback
  - [ ] Question answering triggering graceful refusal
