from typing import Annotated, TypedDict, List, Dict, Any
from langgraph.graph import StateGraph, END
from langchain_groq import ChatGroq
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
import json

class AgentState(TypedDict):
    task: str
    input_data: Dict
    result: Any
    groq_key: str

def get_llm(groq_key: str):
    # Ensure key is valid
    if not groq_key or len(groq_key) < 10:
        raise ValueError("Invalid Groq API Key provided")
        
    return ChatGroq(
        temperature=0.1,
        api_key=groq_key,
        model_name="llama-3.1-8b-instant"
    )

class Idea(BaseModel):
    name: str = Field(description="Name of the startup")
    description: str = Field(description="Brief summary of the idea")
    target_audience: str = Field(description="Who is this for")
    uvp: str = Field(description="Unique Value Proposition")

class IdeaList(BaseModel):
    ideas: List[Idea]

class Pioneer(BaseModel):
    name: str = Field(description="Name of the person")
    company: str = Field(description="Company they founded or lead")
    story: str = Field(description="One sentence about their success")
    link: str = Field(description="URL to their LinkedIn, Twitter or website")

class PioneerList(BaseModel):
    pioneers: List[Pioneer]

class Event(BaseModel):
    name: str = Field(description="Name of the event")
    date: str = Field(description="Date or month of the event")
    location: str = Field(description="City or 'Online'")
    link: str = Field(description="Registration URL")

class Resource(BaseModel):
    title: str = Field(description="Title of the resource/video")
    type: str = Field(description="e.g. YouTube, Podcast, Article")
    summary: str = Field(description="Why this is relevant")
    url: str = Field(description="Link to the resource")

class EcosystemList(BaseModel):
    events: List[Event]
    resources: List[Resource]

def generate_ideas_node(state: AgentState):
    llm = get_llm(state["groq_key"])
    
    # Use a direct prompt first if structured output fails
    # But let's try to keep structured output and add a fallback or more context
    structured_llm = llm.with_structured_output(IdeaList)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a senior startup architect. Generate 3 unique startup ideas. You MUST return valid JSON matching the schema provided."),
        ("human", "Generate ideas for domain: '{domain}' with these skills: '{skills}'")
    ])
    
    chain = prompt | structured_llm
    try:
        res = chain.invoke(state["input_data"])
        return {"result": res.model_dump()}
    except Exception as e:
        print(f"Structured output failed: {e}")
        # Fallback to plain text if needed
        raise e

def validate_idea_node(state: AgentState):
    llm = get_llm(state["groq_key"])
    idea = state["input_data"]["idea"]
    
    # Handle missing fields from simple validation mode
    name = idea.get("name", "Unnamed Idea")
    desc = idea.get("description", "No description provided")
    target = idea.get("target_audience", "General Public")
    uvp = idea.get("uvp", "Standard Market Value")

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a critical startup validator. Analyze the following idea for Market Fit, Risks, and SWOT. Use a technical and business-focused tone."),
        ("human", "Idea: {name}\nDescription: {description}\nTarget: {target}\nUVP: {uvp}")
    ])
    
    chain = prompt | llm
    res = chain.invoke({"name": name, "description": desc, "target": target, "uvp": uvp})
    return {"result": {"validation_report": res.content}}

def generate_roadmap_node(state: AgentState):
    llm = get_llm(state["groq_key"])
    idea = state["input_data"]["idea"]
    timeline = state["input_data"]["timeline"]
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert project manager. Create a detailed weekly execution roadmap for the following startup idea over a {timeline} period."),
        ("human", "Idea: {name}\nDescription: {description}")
    ])
    
    chain = prompt | llm
    res = chain.invoke({**idea, "timeline": timeline})
    return {"result": {"roadmap": res.content}}

def chat_node(state: AgentState):
    llm = get_llm(state["groq_key"])
    message = state["input_data"]["message"]
    context = state["input_data"]["context"]
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a Startup Copilot assistant. Answer ANY question asked. If it's related to startups, use this context: {context}. IMPORTANT: Always end your response with 1 specific follow-up question."),
        ("human", "{message}")
    ])
    
    chain = prompt | llm
    res = chain.invoke({"message": message, "context": json.dumps(context)})
    return {"result": res.content}

def strategy_node(state: AgentState):
    llm = get_llm(state["groq_key"])
    idea = state["input_data"]["idea"]
    budget = state["input_data"]["budget"]
    age = state["input_data"]["age"]
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a master venture strategist. Create a custom startup strategy. Weigh Founder Age (Younger=Aggressive/Digital, Older=Strategic/Network) and Budget (Runway limits). Current context: {idea}"),
        ("human", "My Budget is {budget} and I am {age} years old. Give me a tactical execution strategy.")
    ])
    
    chain = prompt | llm
    res = chain.invoke({"idea": json.dumps(idea), "budget": budget, "age": age})
    return {"result": {"strategy_report": res.content}}

def pioneers_node(state: AgentState):
    llm = get_llm(state["groq_key"])
    domain = state["input_data"].get("domain", "Tech")
    
    structured_llm = llm.with_structured_output(PioneerList)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a startup historian. Identify 4 iconic founders or leaders who have succeeded in the specific domain provided. Provide their name, company, a punchy one-sentence story, and a real URL to their profile or company site. If domain is generic, provide global tech icons."),
        ("human", "Find pioneers for the domain: '{domain}'")
    ])
    
    chain = prompt | structured_llm
    res = chain.invoke({"domain": domain})
    return {"result": res.model_dump()}

def ecosystem_node(state: AgentState):
    llm = get_llm(state["groq_key"])
    domain = state["input_data"].get("domain", "Tech")
    
    structured_llm = llm.with_structured_output(EcosystemList)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a startup networker. Identify 3 major global startup events or summits happening in 2026 (e.g. Web Summit, SaaStr, TechCrunch Disrupt, Slush). Also, provide 3 high-quality learning resources or specific YouTube video suggestions (name and search link) related to the given domain."),
        ("human", "Build an ecosystem hub for the domain: '{domain}'")
    ])
    
    chain = prompt | structured_llm
    res = chain.invoke({"domain": domain})
    return {"result": res.model_dump()}

def run_startup_workflow(task: str, input_data: Dict, groq_key: str):
    workflow = StateGraph(AgentState)
    
    workflow.add_node("generate", generate_ideas_node)
    workflow.add_node("validate", validate_idea_node)
    workflow.add_node("roadmap", generate_roadmap_node)
    workflow.add_node("chat", chat_node)
    workflow.add_node("strategy", strategy_node)
    workflow.add_node("pioneers", pioneers_node)
    workflow.add_node("ecosystem", ecosystem_node)
    
    workflow.set_entry_point(task)
    workflow.add_edge(task, END)
    
    app = workflow.compile()
    
    state = {
        "task": task,
        "input_data": input_data,
        "groq_key": groq_key,
        "result": {}
    }
    
    final_state = app.invoke(state)
    return final_state["result"]
