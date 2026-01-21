# API Usage Examples

## Python Examples

### Basic Chat Example
```python
import requests

# Configuration
API_URL = "http://localhost:8000"

# Send a chat message
response = requests.post(
    f"{API_URL}/chat",
    json={
        "query": "What is machine learning?",
        "user_id": "demo_user"
    }
)

result = response.json()
print(f"Response: {result['response']}")
print(f"Sources: {result['sources']}")
```

### Adding Knowledge
```python
import requests

API_URL = "http://localhost:8000"

# Add a document to the knowledge base
documents = [
    {
        "content": "Python is a high-level, interpreted programming language known for its simplicity and readability.",
        "metadata": {"source": "python_intro.txt", "category": "programming"}
    },
    {
        "content": "Machine learning is a subset of AI that enables systems to learn from data without explicit programming.",
        "metadata": {"source": "ml_basics.pdf", "category": "ai"}
    }
]

for doc in documents:
    response = requests.post(
        f"{API_URL}/knowledge",
        json=doc
    )
    result = response.json()
    print(f"Added document: {result['document_id']}")
```

### Health Check
```python
import requests

API_URL = "http://localhost:8000"

response = requests.get(f"{API_URL}/health")
health = response.json()

print(f"System Status: {health['status']}")
print(f"LLM: {health['services']['llm']}")
print(f"Vector DB: {health['services']['vector_db']}")
```

## JavaScript Examples

### Fetch API - Chat
```javascript
async function chat(query) {
    const response = await fetch('http://localhost:8000/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            query: query,
            user_id: 'demo_user'
        })
    });
    
    const data = await response.json();
    console.log('Response:', data.response);
    console.log('Sources:', data.sources);
    return data;
}

// Usage
chat('Tell me about artificial intelligence');
```

### Axios - Add Knowledge
```javascript
const axios = require('axios');

async function addKnowledge(content, metadata) {
    try {
        const response = await axios.post('http://localhost:8000/knowledge', {
            content: content,
            metadata: metadata,
            user_id: 'demo_user'
        });
        
        console.log('Document added:', response.data.document_id);
        return response.data;
    } catch (error) {
        console.error('Error:', error.message);
    }
}

// Usage
addKnowledge(
    'FastAPI is a modern, fast web framework for building APIs with Python.',
    { source: 'fastapi_docs', category: 'web_framework' }
);
```

## cURL Examples

### Chat Request
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What are the benefits of cloud computing?",
    "user_id": "user123"
  }'
```

### Add Knowledge
```bash
curl -X POST http://localhost:8000/knowledge \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Docker is a platform for developing, shipping, and running applications in containers.",
    "metadata": {
      "source": "docker_guide.pdf",
      "category": "devops",
      "author": "Docker Team"
    },
    "user_id": "user123"
  }'
```

### Health Check
```bash
curl http://localhost:8000/health
```

## Advanced Examples

### Conversational Context
```python
import requests

API_URL = "http://localhost:8000"
conversation_history = []

def chat_with_context(query):
    conversation_history.append(query)
    
    # Include conversation history in the query
    full_query = " ".join(conversation_history[-3:])  # Last 3 messages
    
    response = requests.post(
        f"{API_URL}/chat",
        json={"query": full_query}
    )
    
    result = response.json()
    return result['response']

# Usage
print(chat_with_context("What is Python?"))
print(chat_with_context("What are its main features?"))
print(chat_with_context("Give me an example"))
```

### Batch Knowledge Addition
```python
import requests
import json

API_URL = "http://localhost:8000"

def add_knowledge_from_file(filepath):
    """Add multiple documents from a JSON file"""
    with open(filepath, 'r') as f:
        documents = json.load(f)
    
    results = []
    for doc in documents:
        response = requests.post(
            f"{API_URL}/knowledge",
            json=doc
        )
        results.append(response.json())
    
    return results

# JSON file format:
# [
#   {
#     "content": "Document text here...",
#     "metadata": {"source": "file1.txt"}
#   },
#   ...
# ]

results = add_knowledge_from_file('knowledge_base.json')
print(f"Added {len(results)} documents")
```

### Error Handling
```python
import requests
from requests.exceptions import RequestException

API_URL = "http://localhost:8000"

def safe_chat(query, retries=3):
    for attempt in range(retries):
        try:
            response = requests.post(
                f"{API_URL}/chat",
                json={"query": query},
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error: {response.status_code}")
                
        except RequestException as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt == retries - 1:
                raise
    
    return None

# Usage
result = safe_chat("What is Docker?")
if result:
    print(result['response'])
```

## Integration Examples

### Flask Integration
```python
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)
JARVIS_API = "http://localhost:8000"

@app.route('/ask', methods=['POST'])
def ask_jarvis():
    user_query = request.json.get('question')
    
    response = requests.post(
        f"{JARVIS_API}/chat",
        json={"query": user_query}
    )
    
    return jsonify(response.json())

if __name__ == '__main__':
    app.run(port=5000)
```

### Express.js Integration
```javascript
const express = require('express');
const axios = require('axios');

const app = express();
app.use(express.json());

const JARVIS_API = 'http://localhost:8000';

app.post('/ask', async (req, res) => {
    try {
        const response = await axios.post(`${JARVIS_API}/chat`, {
            query: req.body.question
        });
        
        res.json(response.data);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

app.listen(3000, () => {
    console.log('Server running on port 3000');
});
```

## Testing Examples

### Unit Test (pytest)
```python
import pytest
import requests

API_URL = "http://localhost:8000"

def test_health_check():
    response = requests.get(f"{API_URL}/health")
    assert response.status_code == 200
    data = response.json()
    assert data['status'] in ['healthy', 'degraded']

def test_chat_endpoint():
    response = requests.post(
        f"{API_URL}/chat",
        json={"query": "Hello"}
    )
    assert response.status_code == 200
    data = response.json()
    assert 'response' in data
    assert 'sources' in data

def test_add_knowledge():
    response = requests.post(
        f"{API_URL}/knowledge",
        json={
            "content": "Test document",
            "metadata": {"source": "test"}
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data['status'] == 'success'
```

## Performance Testing

### Load Testing with locust
```python
from locust import HttpUser, task, between

class JarvisUser(HttpUser):
    wait_time = between(1, 3)
    
    @task(3)
    def chat(self):
        self.client.post("/chat", json={
            "query": "What is AI?",
            "user_id": "load_test_user"
        })
    
    @task(1)
    def health_check(self):
        self.client.get("/health")
```

## Response Formats

### Successful Chat Response
```json
{
  "response": "Machine learning is a subset of artificial intelligence...",
  "sources": [
    "ml_introduction.pdf",
    "ai_concepts.html"
  ]
}
```

### Knowledge Addition Response
```json
{
  "status": "success",
  "message": "Knowledge added successfully",
  "document_id": "a1b2c3d4e5f6..."
}
```

### Error Response
```json
{
  "detail": "Error processing query: Connection timeout"
}
```

### Health Check Response
```json
{
  "status": "healthy",
  "services": {
    "llm": "operational",
    "vector_db": "operational"
  }
}
```

---

For more examples and detailed API documentation, visit `http://localhost:8000/docs` after starting the server.
