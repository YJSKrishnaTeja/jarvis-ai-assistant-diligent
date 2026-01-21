from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
from dotenv import load_dotenv
import uvicorn

# Load environment variables
load_dotenv()

app = FastAPI(title="Jarvis AI Assistant", version="1.0.0")

# CORS middleware for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response models
class QueryRequest(BaseModel):
    query: str
    user_id: Optional[str] = "default_user"

class QueryResponse(BaseModel):
    response: str
    sources: Optional[List[str]] = []

class KnowledgeRequest(BaseModel):
    content: str
    metadata: Optional[dict] = {}
    user_id: Optional[str] = "default_user"

# Initialize services
from services.llm_service import LLMService
from services.vector_service import VectorService

llm_service = LLMService()
vector_service = VectorService()

@app.get("/")
async def root():
    return {
        "message": "Jarvis AI Assistant API",
        "version": "1.0.0",
        "endpoints": {
            "/chat": "POST - Send a query to Jarvis",
            "/knowledge": "POST - Add knowledge to the vector database",
            "/health": "GET - Check system health"
        }
    }

@app.post("/chat", response_model=QueryResponse)
async def chat(request: QueryRequest):
    """
    Main chat endpoint - processes user queries using RAG (Retrieval Augmented Generation)
    """
    try:
        # 1. Retrieve relevant context from vector database
        relevant_docs = await vector_service.search(request.query, top_k=3)
        
        # 2. Build context from retrieved documents
        context = "\n\n".join([doc['text'] for doc in relevant_docs])
        
        # 3. Generate response using LLM with context
        response = await llm_service.generate_response(
            query=request.query,
            context=context
        )
        
        # 4. Extract sources
        sources = [doc.get('metadata', {}).get('source', 'Unknown') for doc in relevant_docs]
        
        return QueryResponse(
            response=response,
            sources=sources
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")

@app.post("/knowledge")
async def add_knowledge(request: KnowledgeRequest):
    """
    Add new knowledge to the vector database
    """
    try:
        # Store in vector database
        doc_id = await vector_service.add_document(
            text=request.content,
            metadata=request.metadata,
            user_id=request.user_id
        )
        
        return {
            "status": "success",
            "message": "Knowledge added successfully",
            "document_id": doc_id
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding knowledge: {str(e)}")

@app.get("/health")
async def health_check():
    """
    Health check endpoint
    """
    llm_status = await llm_service.health_check()
    vector_status = await vector_service.health_check()
    
    return {
        "status": "healthy" if llm_status and vector_status else "degraded",
        "services": {
            "llm": "operational" if llm_status else "unavailable",
            "vector_db": "operational" if vector_status else "unavailable"
        }
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
