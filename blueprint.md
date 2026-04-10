# Startup Copilot AI: Product Blueprint & Specification

## 1. System Overview
**Startup Copilot AI** is a production-ready GenAI application designed to guide entrepreneurs from initial "niche" sparks to validated execution roadmaps. It leverages multi-agent workflows and RAG to provide deep technical and business insights.

## 2. Technical Stack
| Layer | Tech | Rationale |
| :--- | :--- | :--- |
| **Frontend** | React (Vite) + CSS Modules | Fast, modern UI with rich animations. |
| **Backend** | FastAPI (Python) | High-performance, async, native support for LangChain. |
| **AI Orchestration** | LangGraph + LangChain | State-aware multi-agent workflows. |
| **Vector Database** | ChromaDB (Local/Persistent) | Lightweight RAG for industry validation. |
| **Observability** | LangSmith | Traceability, cost tracking, and prompt debugging. |
| **Deployment** | Vercel (Frontend/Serverless) | Seamless CI/CD and scalability. |

---

## 3. Product Modules

### A. Idea Generator
- **Inputs:** User's domain of interest, skills, or a problem statement.
- **Logic:** Uses GPT-4o with specialized prompts to generate 3-5 unique startup concepts with UVP (Unique Value Proposition).
- **Output:** JSON list of concepts with names, descriptions, and target audiences.

### B. Validation Engine (RAG)
- **Inputs:** Selected idea.
- **Logic:** 
  1. Queries ChromaDB for similar existing startups or market trends.
  2. Performs a SWOT analysis.
  3. Uses a "Critic Agent" to highlight risks.
- **Output:** Validation report (Score 1-100, Market Gaps, Risk Assessment).

### C. Execution Roadmap
- **Inputs:** Validated Idea + User's timeline (e.g., 3 months).
- **Logic:** Breaks down the project into weekly phases (MVP, Marketing, Growth).
- **Output:** Interactive timeline view.

### D. Interactive Copilot (Chat)
- **Inputs:** Natural language queries.
- **Logic:** Context-aware chat using the current project state (Idea + Roadmap).
- **Output:** Dynamic advice and documentation generation.

---

## 4. Agent Workflows (LangGraph)

The system uses a stateful graph to manage transitions:
1. **Node: `generate_ideas`** -> Returns list of candidates.
2. **Node: `validate_selection`** -> Performs RAG lookup and Swot Analysis.
3. **Node: `refine_concept`** -> Reasoning loop to improve the idea based on validation.
4. **Node: `generate_roadmap`** -> Structured output of execution steps.
5. **Conditional Logic:** If validation score < 50, route back to `refine_concept`.

---

## 5. RAG Architecture
- **Data Source:** Curated local JSON files of startup trends and tech news.
- **Flow:**
  1. **Ingest:** Periodically update `ChromaDB` with market data.
  2. **Retrieve:** When validating, embed the user's idea and fetch top 5 related market snippets.
  3. **Augment:** Inject snippets into the `Critic Agent` prompt context.

---

## 6. API Structure (FastAPI)

- `POST /api/generate`: Generate startup ideas.
- `POST /api/validate`: Validate a specific idea.
- `POST /api/roadmap`: Generate a roadmap for a validated idea.
- `POST /api/chat`: Talk to the Copilot (streaming supported).
- `GET /api/history`: Retrieve past generated projects.

---

## 7. Data Flow
1. **User Input** -> Frontend -> API Request.
2. **Backend** -> LangGraph Execution.
3. **LangGraph** -> (State Update) -> ChromaDB Query -> LLM Processing.
4. **Final State** -> Database (Local JSON/SQLite) -> Frontend Dashboard.

---

## 8. Evaluation & Metrics
- **Accuracy:** Human-in-the-loop scoring for validity.
- **Latency:** Target < 3s for generation, < 8s for full validation.
- **Cost:** GPT-3.5-Turbo for chat, GPT-4o for complex reasoning/validation.
- **Observability:** LangSmith integration for tracing graph nodes.

---

## 9. Design Aesthetic (The "Premium" Feel)
- **Theme:** Midnight Navy & Electric Cyan (Dark Mode by default).
- **Typography:** Inter or Outfit (Google Fonts).
- **Interactions:** Subtle glassmorphism, pulse animations during generation, and smooth fade-ins for content cards.
