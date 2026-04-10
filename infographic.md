# 🚀 Startup Copilot AI: Platform Infographic

Our platform has evolved into a high-octane startup command center. Here is how the engine works.

## 🗺️ The User Journey (Three Strategic Paths)

```mermaid
graph TD
    User([Founder]) --> Choice{Execution Path}
    
    Choice --> OP[<b>Find an Opportunity</b>]
    OP --> |Generate| Ideas[3 Strategic Startup Concepts]
    
    Choice --> FD[<b>Test the Foundation</b>]
    FD --> |Simple Idea| Val[Deep Validation & SWOT]
    
    Choice --> VS[<b>Build My Vision</b>]
    VS --> |Domain + Skills| Road[Execution Roadmap & Growth Simulation]

    subgraph "The Intelligence Engine"
    Ideas --> AI[AI Research Assistant]
    Val --> AI
    Road --> AI
    end
```

## 🧠 The Agentic Graph (LangGraph Architecture)

```mermaid
flowchart LR
    Start((Entry)) --> Task{Task?}
    
    Task --> |Generate| G[generate_ideas_node]
    Task --> |Validate| V[validate_idea_node]
    Task --> |Roadmap| R[generate_roadmap_node]
    Task --> |Strategy| S[strategy_node]
    Task --> |Chat| C[chat_node]
    
    G --> End((Dashboard))
    V --> End
    R --> End
    S --> End
    C --> End
    
    subgraph "Context Layer"
    KB[(ChromaDB Knowledge Base)] <--> AI[RAG Research Agent]
    end
```

## 🛠️ The Technology Stack

| Layer | Technology | Purpose |
| :--- | :--- | :--- |
| **Backend** | **FastAPI** | High-performance API orchestration |
| **AI Graph** | **LangGraph** | State-managed agent workflows |
| **Brain** | **Llama 3.1 (Groq)** | 8B parameter high-speed inference |
| **Memory** | **ChromaDB** | Semantic search & RAG Knowledge Base |
| **Frontend** | **Vanilla JS / CSS** | Premium Glassmorphism UI |

---

### 🌟 Key Performance Features
- **Deterministic State**: LangGraph ensures the AI never loses context during the session.
- **RAG-Powered**: Research answers are grounded in a curated knowledge base of startup wisdom.
- **Strategic Intelligence**: Strategy is dynamically calculated based on **Founder Age** (Risk) and **Budget** (Runway).
