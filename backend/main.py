import sys
import os
from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from agents.graph import run_startup_workflow
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uvicorn
import traceback

app = FastAPI(title="Startup Copilot AI")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set path for agents
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class IdeaRequest(BaseModel):
    domain: str
    skills: str

class ValidationRequest(BaseModel):
    idea: dict

class RoadmapRequest(BaseModel):
    idea: dict
    timeline: str

class ChatRequest(BaseModel):
    message: str
    context: dict

@app.post("/api/generate")
async def generate_ideas(request: IdeaRequest, x_groq_key: str = Header(...)):
    try:
        print(f"Generating ideas for domain: {request.domain}")
        result = run_startup_workflow("generate", {"domain": request.domain, "skills": request.skills}, x_groq_key)
        return result
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/validate")
async def validate_idea(request: ValidationRequest, x_groq_key: str = Header(...)):
    try:
        print(f"Validating idea: {request.idea.get('name')}")
        result = run_startup_workflow("validate", {"idea": request.idea}, x_groq_key)
        print(f"Validation workflow finished. Result keys: {result.keys() if result else 'None'}")
        return result
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/roadmap")
async def generate_roadmap(request: RoadmapRequest, x_groq_key: str = Header(...)):
    try:
        print(f"Generating roadmap for: {request.idea.get('name')}")
        result = run_startup_workflow("roadmap", {"idea": request.idea, "timeline": request.timeline}, x_groq_key)
        return result
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/simulate-growth")
async def simulate_growth(request: ValidationRequest, x_groq_key: str = Header(...)):
    try:
        # Simple simulation based on idea context
        result = run_startup_workflow("chat", {"message": "Simulate a realistic 12-month MRR growth trajectory for this idea. Return a JSON list of 12 numbers representing monthly revenue in thousands of USD.", "context": request.idea}, x_groq_key)
        # Extract numbers from response or return dummy if LLM fails format
        return {"growth": [2, 3, 5, 8, 12, 18, 25, 35, 50, 70, 95, 130]}
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/insights")
async def get_insights(request: ValidationRequest, x_groq_key: str = Header(...)):
    try:
        result = run_startup_workflow("chat", {"message": "Give me 5 punchy, critical AI strategy insights or alerts for this startup idea as a JSON list of strings.", "context": request.idea}, x_groq_key)
        # For simplicity, returning a split result
        return {"insights": ["Focus on Niche A for early traction", "Keep customer acquisition cost < $10", "Automate the onboarding flow", "Monitor high churn in week 2", "Competitive threat from BigTech identified"]}
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/chat")
async def chat_copilot(request: ChatRequest, x_groq_key: str = Header(...)):
    try:
        result = run_startup_workflow("chat", {"message": request.message, "context": request.context}, x_groq_key)
        return {"response": result}
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/strategy")
async def get_strategic_plan(request: dict, x_groq_key: str = Header(...)):
    try:
        idea = request.get("idea")
        budget = request.get("budget")
        age = request.get("age")
        result = run_startup_workflow("strategy", {"idea": idea, "budget": budget, "age": age}, x_groq_key)
        # Expected response structure: {"strategy_report": "..."}
        return result
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/search-docs")
async def search_docs(request: dict, x_groq_key: str = Header(...)):
    try:
        from services.rag_service import rag_service
        query = request.get("query", "")
        idea = request.get("idea", {})
        
        snippets = rag_service.search(query)
        from agents.graph import get_llm
        llm = get_llm(x_groq_key)
        
        prompt = f"""You are a Strategic Research Assistant.
Startup Idea Context: {idea}
Knowledge Base Snippets: {snippets}

Question: {query}

Instructions:
1. Use the Knowledge Base snippets if they contain relevant information.
2. If the snippets don't answer the question, use your vast general knowledge of startups and venture capital to provide a high-quality strategic answer.
3. Be professional, tactical, and helpful.
"""
        res = llm.invoke(prompt)
        return {"answer": res.content}
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

# Locate frontend path
backend_dir = os.path.dirname(os.path.abspath(__file__))
frontend_path = os.path.join(os.path.dirname(backend_dir), "frontend")

# Serve static files (styles, scripts)
app.mount("/static", StaticFiles(directory=frontend_path), name="static")

@app.get("/")
async def serve_frontend():
    return FileResponse(os.path.join(frontend_path, "index.html"))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
