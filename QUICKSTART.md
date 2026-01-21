# Quick Start Guide - Jarvis AI Assistant

Get Jarvis up and running in 5 minutes!

## Prerequisites Check

Before starting, ensure you have:
- [ ] Python 3.8 or higher: `python3 --version`
- [ ] pip installed: `pip --version`
- [ ] Git installed: `git --version`

## Step 1: Clone Repository

```bash
git clone <repository-url>
cd jarvis-ai-assistant
```

## Step 2: Setup

### Option A: Automated (Recommended)
```bash
./setup.sh
```

### Option B: Manual
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r backend/requirements.txt

# Setup environment
cp backend/.env.example backend/.env
```

## Step 3: Configure (Optional)

Edit `backend/.env`:
```env
PINECONE_API_KEY=your_api_key_here
```

**Get Pinecone API Key:**
1. Visit https://www.pinecone.io/
2. Sign up for free account
3. Copy API key from dashboard
4. Paste in `.env` file

**Note:** App works without Pinecone in demo mode!

## Step 4: Run

```bash
./run.sh
```

Or manually:
```bash
cd backend
python app.py
```

## Step 5: Access

1. **Backend API**: http://localhost:8000
2. **API Docs**: http://localhost:8000/docs
3. **Frontend**: Open `frontend/index.html` in browser

## Quick Test

### Test in Browser
1. Open `frontend/index.html`
2. Type: "What can you do?"
3. Press Enter

### Test via API
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "Hello Jarvis!"}'
```

## Common Issues

### Port 8000 already in use
```bash
# Kill existing process
lsof -ti:8000 | xargs kill -9

# Or use different port
cd backend
uvicorn app:app --port 8001
```

### ModuleNotFoundError
```bash
# Activate virtual environment
source venv/bin/activate

# Reinstall dependencies
pip install -r backend/requirements.txt
```

### Frontend can't connect
1. Ensure backend is running
2. Check http://localhost:8000/health
3. Open browser console for errors

## Next Steps

### Add Knowledge
```bash
curl -X POST http://localhost:8000/knowledge \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Your knowledge here",
    "metadata": {"source": "my_doc"}
  }'
```

### Install Ollama (Optional)
```bash
# Install
curl https://ollama.ai/install.sh | sh

# Download LLaMA
ollama pull llama2

# Start server
ollama serve
```

### Use Docker
```bash
docker-compose up -d
```

## Architecture Overview

```
Frontend (HTML/JS) → FastAPI → LLM (LLaMA) + Vector DB (Pinecone)
```

## Key Features

✅ Natural language chat interface
✅ Semantic search with vector database
✅ RAG (Retrieval Augmented Generation)
✅ Works in demo mode without dependencies
✅ REST API for integrations
✅ Docker support

## Getting Help

- **Documentation**: Check `README.md`
- **API Docs**: Visit http://localhost:8000/docs
- **Examples**: See `docs/api-examples.md`
- **Architecture**: Read `docs/architecture.md`

## What's Next?

1. **Customize**: Modify frontend UI
2. **Integrate**: Use API in your apps
3. **Scale**: Deploy with Docker
4. **Extend**: Add new features

---

**You're all set! Start chatting with Jarvis! 🚀**

For detailed documentation, see the main README.md file.
