# GitHub Issues Templates

This file contains the exact Titles and Bodies for all 9 Epics required to build the Self-Corrective RAG System from scratch to a production-grade Kubernetes deployment. 

Copy the Title and Body for each Epic and paste them into the "New Issue" screen on GitHub to populate your Project Board.

---

## 📋 Epic 1: Repository Scaffolding & Environment Setup
**Title:** `Epic 1: Repository Scaffolding & Environment Setup`

**Body:**
```markdown
### Description
Initialize the foundational structure of the Self-Corrective RAG system. This Epic covers setting up the Python virtual environment, installing necessary dependencies, freezing those dependencies for production stability, and organizing the codebase directories.

### Tasks Checklist
- [x] **Sub-task 1: Virtual Environment**
  - [x] Initialize Python virtual environment (`.venv`) using `uv`.
  - [x] Ensure `.venv` is added to `.gitignore`.
- [x] **Sub-task 2: Dependency Installation**
  - [x] Install core packages: `langgraph`, `langchain-google-genai`, `chromadb`, `duckduckgo-search`, and `python-dotenv`.
  - [x] Verify installation by importing packages successfully in a test script.
- [x] **Sub-task 3: Freeze Dependencies (Production Standard)**
  - [x] Freeze installed packages into a `requirements.txt` file so production deployments have deterministic versions.
- [x] **Sub-task 4: Folder Structure & Configuration**
  - [x] Create core directories: `app/`, `data/`, `docs/`, `notebooks/`, and `tests/`.
  - [x] Create `.env.example` to define required environment variables.
  - [x] Write initial project documentation blueprints in the `docs/` folder.

### Acceptance Criteria
- [x] The virtual environment is active and all dependencies are installed without errors.
- [x] A `requirements.txt` file exists tracking exact dependency versions.
- [x] The directory structure is organized perfectly.
```

---

## 📋 Epic 2: Document Loading & Text Chunking
**Title:** `Epic 2: Document Loading & Text Chunking`

**Body:**
```markdown
### Description
Build the first half of the data ingestion pipeline. The goal is to write a script that can open local `.txt` and `.md` files, extract the raw text, and split that text into perfectly sized, 1,000-character "chunks". 

### Tasks Checklist
- [ ] Create the `data/source_docs/` directory and add a sample `.txt` or `.md` file.
- [ ] Write the document loading logic in `app/retrieval/loader.py` using LangChain's DirectoryLoader.
- [ ] Implement the `RecursiveCharacterTextSplitter` logic in the same file to chunk the text.
- [ ] Create `test_loader.py` to run the functions and print the resulting chunks to the terminal.

### Acceptance Criteria
- [ ] Running `python test_loader.py` successfully prints individual chunks of text to the terminal, proving the documents were read and split correctly.
```

---

## 📋 Epic 3: Embeddings & ChromaDB Storage
**Title:** `Epic 3: Embeddings & ChromaDB Storage`

**Body:**
```markdown
### Description
Complete the ingestion pipeline by translating the text chunks into mathematical vectors using Google's embedding model, and storing them locally in ChromaDB.

### Tasks Checklist
- [ ] Connect to Google's `text-embedding-004` API.
- [ ] Initialize the local ChromaDB client in `app/retrieval/vectorstore.py` (persistent folder: `data/chromadb`).
- [ ] Write a script `ingest.py` to take chunks from Epic 2, embed them, and save them to the database.
- [ ] Write a quick search query function to verify we can search the database for relevant chunks.

### Acceptance Criteria
- [ ] Running `python ingest.py` successfully populates the `data/chromadb` directory.
- [ ] We can perform a test semantic search and retrieve accurate chunks.
```

---

## 📋 Epic 4: LLM Synthesis & Critique Graders
**Title:** `Epic 4: LLM Synthesis & Critique Graders`

**Body:**
```markdown
### Description
Build the critique agents and the answer synthesizer. Grader agents evaluate document relevance, verify that synthesized answers don't hallucinate facts, and check that answers satisfy the user query.

### Tasks Checklist
- [ ] Implement Pydantic structured schemas for graders (`GradeDocument`, `GradeHallucination`, `GradeAnswer`).
- [ ] Implement Grader agents in `app/critique/graders.py` using `gemini-1.5-flash`:
  - [ ] **Document Relevance Grader**
  - [ ] **Hallucination Grader**
  - [ ] **Answer Utility Grader**
- [ ] Implement context-aware generation logic in `app/generation/synthesizer.py`.

### Acceptance Criteria
- [ ] Grader agents reliably return `"yes"` or `"no"` boolean answers.
- [ ] The generation synthesizes clear responses based on matching context.
```

---

## 📋 Epic 5: Web Search Fallback & LangGraph Orchestration
**Title:** `Epic 5: Web Search Fallback & LangGraph Orchestration`

**Body:**
```markdown
### Description
Construct the stateful, cyclic workflow graph using LangGraph. Connect the free DuckDuckGo search fallback mechanism and assemble all nodes into a state machine.

### Tasks Checklist
- [ ] Implement query reformulation inside `app/utils/search.py`.
- [ ] Connect DuckDuckGo search API and parser (`app/utils/search.py`).
- [ ] Define the `GraphState` dictionary model (`app/workflows/state.py`).
- [ ] Build workflow nodes (`retrieve`, `grade_documents`, `generate`, `web_search`).
- [ ] Build conditional router edges (`app/workflows/edges.py`).
- [ ] Compile and test the cyclic graph (`app/workflows/graph.py`).

### Acceptance Criteria
- [ ] The CLI successfully answers queries by searching the local vector store.
- [ ] When context is lacking, the system searches DuckDuckGo and outputs a refined answer.
```

---

## 📋 Epic 6: Sleek Frontend Dashboard & Static Web Server
**Title:** `Epic 6: Sleek Frontend Dashboard & Static Web Server`

**Body:**
```markdown
### Description
Create a stunning, modern frontend UI directly served by FastAPI. It must provide a premium chat interface and a live visual representation of our LangGraph agent's decision-making process.

### Tasks Checklist
- [ ] Setup FastAPI static directory hosting (`app/api/static/`).
- [ ] Create `index.html` and `index.css` using modern typography, dark mode glassmorphism, and responsive layouts.
- [ ] Build an interactive Javascript chat client.
- [ ] Create a Live Agent Status Visualizer displaying the active node in real-time.

### Acceptance Criteria
- [ ] Going to `http://localhost:8000` opens a beautiful chat application.
- [ ] Asking a question streams messages and shows live visual tracking.
```

---

## 📋 Epic 7: Production Containerization (Docker)
**Title:** `Epic 7: Production Containerization (Docker)`

**Body:**
```markdown
### Description
Containerize our Self-Corrective RAG system using Docker. Create a production-grade, multi-stage Dockerfile that preserves local ChromaDB storage.

### Tasks Checklist
- [ ] Create a multi-stage `Dockerfile`.
- [ ] Create a `.dockerignore` file.
- [ ] Build a `docker-compose.yml` to configure the FastAPI container and local volume mapping (`./data` -> `/app/data`).

### Acceptance Criteria
- [ ] Running `docker-compose up` launches the entire RAG pipeline successfully.
```

---

## 📋 Epic 8: Production Deployment & Kubernetes
**Title:** `Epic 8: Production Deployment & Kubernetes`

**Body:**
```markdown
### Description
Design the Kubernetes manifests required to deploy and manage our application in a production cluster (e.g., K3s, Minikube).

### Tasks Checklist
- [ ] Create `k8s/deployment.yaml`.
- [ ] Create `k8s/service.yaml`.
- [ ] Create persistent volume claims (`k8s/pvc.yaml`).
- [ ] Define ConfigMaps and Secrets securely.

### Acceptance Criteria
- [ ] Running `kubectl apply -f k8s/` launches the pods and mounts the persistent volume.
```

---

## 📋 Epic 9: CI/CD Pipeline (GitHub Actions)
**Title:** `Epic 9: Continuous Integration & Deployment (CI/CD)`

**Body:**
```markdown
### Description
Configure automation using GitHub Actions to trigger automatically on every push to the `main` branch.

### Tasks Checklist
- [ ] Create the GitHub Actions workflow file `.github/workflows/ci.yml`.
- [ ] Configure code linting and formatting verification.
- [ ] Configure automated Python unit tests (`pytest`).
- [ ] Configure dry-run Docker build.

### Acceptance Criteria
- [ ] Pushing code triggers the CI pipeline.
- [ ] Failed unit tests prevent broken code from merging.
```
