import os
import hashlib
from typing import List, Dict, Optional
from sentence_transformers import SentenceTransformer
import numpy as np

# Try to import pinecone, fallback to in-memory store
try:
    from pinecone import Pinecone, ServerlessSpec
    PINECONE_AVAILABLE = True
except ImportError:
    PINECONE_AVAILABLE = False
    print("⚠️  Pinecone not installed. Using in-memory vector store for demo.")

class VectorService:
    """
    Service for vector database operations using Pinecone
    Falls back to in-memory storage if Pinecone is not configured
    """
    
    def __init__(self):
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.dimension = 384  # Dimension of all-MiniLM-L6-v2
        self.index_name = os.getenv("PINECONE_INDEX_NAME", "jarvis-knowledge")
        
        # In-memory fallback storage
        self.memory_store = []
        
        # Try to initialize Pinecone
        self.pinecone_client = None
        self.index = None
        self._initialize_pinecone()
    
    def _initialize_pinecone(self):
        """Initialize Pinecone connection"""
        if not PINECONE_AVAILABLE:
            print("Using in-memory vector store (demo mode)")
            return
        
        api_key = os.getenv("PINECONE_API_KEY")
        
        if not api_key:
            print("⚠️  PINECONE_API_KEY not found. Using in-memory vector store.")
            return
        
        try:
            # Initialize Pinecone
            self.pinecone_client = Pinecone(api_key=api_key)
            
            # Check if index exists, create if not
            existing_indexes = [index.name for index in self.pinecone_client.list_indexes()]
            
            if self.index_name not in existing_indexes:
                print(f"Creating Pinecone index: {self.index_name}")
                self.pinecone_client.create_index(
                    name=self.index_name,
                    dimension=self.dimension,
                    metric="cosine",
                    spec=ServerlessSpec(
                        cloud="aws",
                        region=os.getenv("PINECONE_REGION", "us-east-1")
                    )
                )
            
            # Connect to index
            self.index = self.pinecone_client.Index(self.index_name)
            print(f"✅ Connected to Pinecone index: {self.index_name}")
            
        except Exception as e:
            print(f"⚠️  Error initializing Pinecone: {e}")
            print("Falling back to in-memory vector store.")
            self.pinecone_client = None
            self.index = None
    
    def _generate_embedding(self, text: str) -> List[float]:
        """Generate embedding for text using sentence transformer"""
        embedding = self.embedding_model.encode(text)
        return embedding.tolist()
    
    def _generate_id(self, text: str) -> str:
        """Generate unique ID for document"""
        return hashlib.md5(text.encode()).hexdigest()
    
    async def add_document(self, text: str, metadata: Dict = {}, user_id: str = "default") -> str:
        """Add document to vector database"""
        # Generate embedding
        embedding = self._generate_embedding(text)
        doc_id = self._generate_id(text)
        
        # Prepare metadata
        full_metadata = {
            "text": text,
            "user_id": user_id,
            **metadata
        }
        
        if self.index:
            # Store in Pinecone
            try:
                self.index.upsert(
                    vectors=[{
                        "id": doc_id,
                        "values": embedding,
                        "metadata": full_metadata
                    }]
                )
                print(f"✅ Document added to Pinecone: {doc_id}")
            except Exception as e:
                print(f"Error adding to Pinecone: {e}")
                # Fallback to memory
                self._add_to_memory(doc_id, embedding, full_metadata)
        else:
            # Store in memory
            self._add_to_memory(doc_id, embedding, full_metadata)
        
        return doc_id
    
    def _add_to_memory(self, doc_id: str, embedding: List[float], metadata: Dict):
        """Add document to in-memory store"""
        self.memory_store.append({
            "id": doc_id,
            "embedding": embedding,
            "metadata": metadata
        })
        print(f"✅ Document added to memory store: {doc_id}")
    
    async def search(self, query: str, top_k: int = 3, user_id: Optional[str] = None) -> List[Dict]:
        """Search for similar documents"""
        # Generate query embedding
        query_embedding = self._generate_embedding(query)
        
        if self.index:
            # Search in Pinecone
            try:
                results = self.index.query(
                    vector=query_embedding,
                    top_k=top_k,
                    include_metadata=True
                )
                
                documents = []
                for match in results.matches:
                    documents.append({
                        "id": match.id,
                        "score": match.score,
                        "text": match.metadata.get("text", ""),
                        "metadata": match.metadata
                    })
                
                return documents
            
            except Exception as e:
                print(f"Error searching Pinecone: {e}")
                # Fallback to memory search
                return self._search_memory(query_embedding, top_k)
        else:
            # Search in memory
            return self._search_memory(query_embedding, top_k)
    
    def _search_memory(self, query_embedding: List[float], top_k: int) -> List[Dict]:
        """Search in-memory store using cosine similarity"""
        if not self.memory_store:
            return []
        
        query_vec = np.array(query_embedding)
        similarities = []
        
        for doc in self.memory_store:
            doc_vec = np.array(doc["embedding"])
            # Cosine similarity
            similarity = np.dot(query_vec, doc_vec) / (np.linalg.norm(query_vec) * np.linalg.norm(doc_vec))
            similarities.append({
                "id": doc["id"],
                "score": float(similarity),
                "text": doc["metadata"].get("text", ""),
                "metadata": doc["metadata"]
            })
        
        # Sort by similarity and return top_k
        similarities.sort(key=lambda x: x["score"], reverse=True)
        return similarities[:top_k]
    
    async def health_check(self) -> bool:
        """Check if vector service is healthy"""
        if self.index:
            try:
                # Try to get index stats
                stats = self.index.describe_index_stats()
                return True
            except:
                return False
        else:
            # Memory store is always healthy
            return True
    
    def get_stats(self) -> Dict:
        """Get statistics about the vector store"""
        if self.index:
            try:
                stats = self.index.describe_index_stats()
                return {
                    "backend": "pinecone",
                    "total_vectors": stats.total_vector_count,
                    "dimension": self.dimension
                }
            except:
                return {"backend": "pinecone", "status": "error"}
        else:
            return {
                "backend": "memory",
                "total_vectors": len(self.memory_store),
                "dimension": self.dimension
            }
