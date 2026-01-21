# 🤖 Jarvis – Personal AI Assistant for Enterprise SaaS

A powerful personal AI assistant powered by self-hosted LLM (LLaMA) and Pinecone vector database, featuring conversational interface and contextual knowledge retrieval using RAG (Retrieval Augmented Generation).

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 📸 Demo Screenshot

![Jarvis Demo](docs/images/image.png)

## 🎯 Overview

Jarvis is an enterprise-grade AI assistant that combines:
- **Self-hosted LLM** (LLaMA via Ollama) for natural language understanding
- **Vector Database** (Pinecone) for semantic search and knowledge retrieval
- **RAG Architecture** for contextually relevant responses
- **Modern Web UI** for seamless user interaction
- **RESTful API** for easy integration

## ✨ Features
“Jarvis uses a fully self-hosted LLM (LLaMA via Ollama) ensuring data privacy and enterprise compliance.”

### Core Capabilities
- 💬 **Conversational AI**: Natural language processing with LLaMA
- 🔍 **Semantic Search**: Vector-based knowledge retrieval using Pinecone
- 🧠 **RAG Pipeline**: Combines retrieval and generation for accurate responses
- 📚 **Knowledge Management**: Add and query custom knowledge base
- 🎨 **Modern UI**: Beautiful, responsive chat interface
- 🔌 **REST API**: Full API access for integrations
- 🐳 **Docker Support**: Easy deployment with Docker Compose
- 🎭 **Demo Mode**: Works without external dependencies for testing

### Technical Features
- Asynchronous processing for high performance
- In-memory fallback when Pinecone is unavailable
- Sentence transformer embeddings (all-MiniLM-L6-v2)
- Automatic health checks and monitoring
- CORS enabled for cross-origin requests
- Interactive API documentation (Swagger)

## 🏗️ Architecture

```
┌─────────────┐
│   Frontend  │  (HTML/CSS/JS)
│   Chat UI   │
└──────┬──────┘
       │ HTTP/REST
       ▼
┌─────────────────────────────────────┐
│         FastAPI Backend             │
│  ┌──────────────┐  ┌─────────────┐ │
│  │ LLM Service  │  │   Vector    │ │
│  │   (LLaMA)    │  │   Service   │ │
│  └──────┬───────┘  └──────┬──────┘ │
│         │                  │        │
└─────────┼──────────────────┼────────┘
          ▼                  ▼
    ┌──────────┐      ┌───────────┐
    │  Ollama  │      │ Pinecone  │
    │  Server  │      │  Vector   │
    └──────────┘      │    DB     │
                      └───────────┘
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- (Optional) Docker and Docker Compose
- (Optional) Ollama for local LLaMA



### Installation

#### Option 1: Automated Setup (Recommended)
```bash
# Clone the repository
git clone <repository-url>
cd jarvis-ai-assistant

# Run setup script
./setup.sh

# Edit .env file with your Pinecone API key
nano backend/.env

# Start the application
./run.sh
```

#### Option 2: Manual Setup
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r backend/requirements.txt

# Create .env file
cp backend/.env.example backend/.env
# Edit backend/.env and add your Pinecone API key

# Start backend
cd backend
python app.py

# Open frontend/index.html in your browser
```

#### Option 3: Docker Compose
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the `backend` directory:

```env
# Pinecone Configuration
PINECONE_API_KEY=your_pinecone_api_key_here
PINECONE_INDEX_NAME=jarvis-knowledge
PINECONE_REGION=us-east-1

# LLM Configuration (Ollama)
OLLAMA_URL=http://localhost:11434
LLM_MODEL=llama2

# Application Settings
APP_ENV=development
DEBUG=True
```


### Setting Up Ollama (Optional)
```bash
# Install Ollama
curl https://ollama.ai/install.sh | sh

# Pull LLaMA model
ollama pull llama2

# Start Ollama server
ollama serve
```

**Note**: The application works in demo mode without Ollama, using intelligent rule-based responses.

## 📖 Usage

### Web Interface

1. Open `frontend/index.html` in your browser
2. Type your question in the input field
3. Press Enter or click Send
4. View Jarvis's response with sources
