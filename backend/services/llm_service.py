import os
import asyncio
from typing import Optional
import requests
import json

class LLMService:
    """
    Service for interacting with local LLM (LLaMA via Ollama)
    Falls back to a simple demo mode if Ollama is not available
    """
    
    def __init__(self):
        self.ollama_url = os.getenv("OLLAMA_URL", "http://localhost:11434")
        self.model_name = os.getenv("LLM_MODEL", "llama2")
        self.is_available = False
        self._check_availability()
    
    def _check_availability(self):
        """Check if Ollama is running"""
        try:
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=2)
            self.is_available = response.status_code == 200
        except:
            self.is_available = False
            print("⚠️  Ollama not available. Running in demo mode with rule-based responses.")
    
    async def generate_response(self, query: str, context: str = "") -> str:
        """
        Generate a response to the user query using the LLM
        """
        if self.is_available:
            return await self._generate_with_ollama(query, context)
        else:
            return await self._generate_demo_response(query, context)
    
    async def _generate_with_ollama(self, query: str, context: str) -> str:
        """Generate response using Ollama"""
        try:
            prompt = self._build_prompt(query, context)
            
            payload = {
                "model": self.model_name,
                "prompt": prompt,
                "stream": False
            }
            
            # Run in thread pool to avoid blocking
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: requests.post(
                    f"{self.ollama_url}/api/generate",
                    json=payload,
                    timeout=30
                )
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get("response", "I couldn't generate a response.")
            else:
                return "Error connecting to LLM service."
        
        except Exception as e:
            print(f"Error with Ollama: {e}")
            return await self._generate_demo_response(query, context)
    
    async def _generate_demo_response(self, query: str, context: str) -> str:
        """
        Demo mode: Generate intelligent responses without LLM
        This is for demonstration when Ollama is not available
        """
        query_lower = query.lower()
        
        # If we have context, use it
        if context and len(context) > 50:
            return f"Based on the available information: {context[:500]}...\n\nTo answer your question '{query}', I've found relevant information in the knowledge base that suggests the above context is most relevant."
        
        # Rule-based responses for demo
        if any(word in query_lower for word in ["hello", "hi", "hey"]):
            return "Hello! I'm Jarvis, your AI assistant. How can I help you today?"
        
        elif any(word in query_lower for word in ["weather", "temperature"]):
            return "I can help with weather information, but I need integration with a weather API. For now, I can tell you that I'm designed to retrieve and provide contextual information from my knowledge base."
        
        elif any(word in query_lower for word in ["what", "how", "why", "when", "who"]):
            return f"Regarding '{query}', I've searched my knowledge base. To provide better answers, please add relevant information using the /knowledge endpoint. I use RAG (Retrieval Augmented Generation) to find and synthesize information from stored documents."
        
        elif any(word in query_lower for word in ["help", "capability", "can you"]):
            return """I'm Jarvis, an AI assistant powered by LLaMA and Pinecone vector database. My capabilities include:
            
1. **Conversational AI**: Natural language understanding and generation
2. **Knowledge Retrieval**: Finding relevant information from stored documents using semantic search
3. **Context-Aware Responses**: Using RAG to provide accurate, contextual answers
4. **Learning**: Adding new knowledge to improve responses over time

Try asking me questions or adding knowledge through the API!"""
        
        else:
            return f"I understand you're asking about: '{query}'. I use semantic search to find relevant information from my knowledge base. Currently, I may not have specific information on this topic. You can add knowledge using the /knowledge endpoint to help me answer better!"
    
    def _build_prompt(self, query: str, context: str) -> str:
        """Build the prompt for the LLM"""
        if context:
            return f"""You are Jarvis, a helpful AI assistant. Use the following context to answer the user's question accurately and concisely.

Context:
{context}

User Question: {query}

Answer:"""
        else:
            return f"""You are Jarvis, a helpful AI assistant. Answer the user's question helpfully.

User Question: {query}

Answer:"""
    
    async def health_check(self) -> bool:
        """Check if LLM service is healthy"""
        if not self.is_available:
            return True  # Demo mode is always "healthy"
        
        try:
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=2)
            return response.status_code == 200
        except:
            return False
