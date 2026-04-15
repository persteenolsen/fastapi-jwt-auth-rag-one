# Python + FastAPI + JWT Auth + RAG + (Mock Embeddings Version)  
 
A lightweight **Retrieval-Augmented Generation (RAG)** API built with **FastAPI**, designed for **learning, testing, and prototyping**.

This version uses **deterministic fake embeddings** instead of real embedding models—allowing you to test the full RAG pipeline **without external embedding APIs or costs**.

---

## 📌 Project Info

- **Version:** 0.0.1  
- **Python:** 3.12  
- **Last Updated:** 15-04-2026  

---

## ✨ Features

### 🔐 Authentication
- JWT-based authentication (HS256)  
- Protected endpoints with Bearer tokens  
- Simple environment-based credentials  

---

### 🧠 RAG Pipeline (Fully Functional)
- Ingest `.txt` files from URLs  
- Chunk text with overlap  
- Generate embeddings (**mocked**)  
- Store vectors in PostgreSQL (`pgvector`)  
- Retrieve relevant context for queries  
- Generate answers with Groq LLM  

---

### 🧪 Fake Embeddings (Key Feature)
- Deterministic embeddings based on text hashing  
- 384-dimensional normalized vectors  
- No external API calls required  
- Perfect for:
  - Local development  
  - Testing pipelines  
  - Learning RAG architecture  

> ⚠️ Note: These embeddings do **not understand semantics**—they only simulate the pipeline.

---

### 🤖 LLM Integration (Groq)
- Model: `llama-3.1-8b-instant`  
- Generates responses from retrieved context  
- Temperature-controlled outputs  

---

### 🔎 Semantic Retrieval (Simulated)
- Query → fake embedding  
- Vector similarity search via `pgvector`  
- Top-K document retrieval  

---

### 🗄️ Database (PostgreSQL + pgvector)

Stores:
- Document content  
- Embeddings (`VECTOR(384)`)  
- Source URL  
- Embedding metadata  
- Timestamp  

Optimizations:
- `ivfflat` index  
- Cosine similarity (`<->`)  

---

### ⚙️ Background Processing
- Uses FastAPI `BackgroundTasks`  
- Async ingestion pipeline  
- Non-blocking embedding + database insert  

---

### 🧪 Debugging Tools
- `/debug/retrieve` → test retrieval without auth or LLM  
- Console logs for retrieval inspection  

---

## 📡 API Endpoints

| Method | Endpoint            | Description                          |
|--------|--------------------|--------------------------------------|
| GET    | `/`                | Health check                         |
| POST   | `/login`           | Get JWT token                        |
| POST   | `/ask`             | RAG question answering 🔐            |
| POST   | `/ingest`          | Ingest `.txt` from URL 🔐            |
| POST   | `/debug/retrieve`  | Test retrieval only                  |

🔐 = Requires authentication

---

## ⚙️ Getting Started

### 1. Clone Repository

```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo
```

---

### 2. Create Virtual Environment

```bash
python -m venv venv
```

Activate:

**Windows:**
```bash
venv\Scripts\activate
```

**Mac/Linux:**
```bash
source venv/bin/activate
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file:

```env
DATABASE_URL=your_postgres_connection
GROQ_API_KEY=your_groq_api_key
SECRET_KEY=your_secret_key

FAKE_USERNAME=admin
FAKE_PASSWORD=password
```

---

## ▶️ Run the Application

```bash
uvicorn app:app --reload
```

Available at:

- 🌐 API: http://127.0.0.1:8000

- 📄 Swagger UI: http://127.0.0.1:8000/docs  

---

## 🔐 Authentication Flow

1. Call `/login` with credentials  
2. Receive JWT token  
3. Use in headers:

```http
Authorization: Bearer <your_token>
```

---

## 🧠 How It Works

```text
User Query
   ↓
Fake Embedding (Deterministic)
   ↓
pgvector Similarity Search
   ↓
Top-K Chunks
   ↓
Groq LLM (LLaMA 3.1)
   ↓
Final Answer + Sources
```

---

## 📥 Document Ingestion

### `/ingest`
- Accepts `.txt` file URLs  
- Fetches and cleans text  
- Splits into chunks (with overlap)  
- Generates fake embeddings  
- Stores in PostgreSQL  

---

## 🛠️ Core Components

### 🔹 Chunking
- Fixed-size chunks (default: 500 chars)  
- Overlap: 50 chars  

---

### 🔹 Fake Embedding Logic
- Seed based on text hash  
- Generates reproducible vectors  
- Normalized for cosine similarity  

---

### 🔹 Retrieval
- Uses `embedding <-> query_vector`  
- Returns top-K most similar chunks  

---

## 🗄️ Database Initialization

On startup:
- Enables `pgvector` extension  
- Creates `documents` table  
- Builds similarity index (`ivfflat`)  

---

## 📌 Use Cases

This version is ideal for:

- 🧪 Learning RAG systems  
- ⚙️ Backend prototyping  
- 💻 Local development without API costs  
- 🔍 Debugging retrieval pipelines  

---

## 🚧 Limitations

- ❌ No real semantic understanding (fake embeddings)  
- ❌ Retrieval quality is not meaningful  
- ✅ Pipeline behavior is realistic  

---

## 📌 Future Improvements

- 🔄 Replace fake embeddings with real models (Hugging Face / OpenAI)  
- 📊 Add monitoring/logging  
- 🔍 Hybrid search (BM25 + vectors)  
- 🧩 Add document formats (PDF, HTML)
- Splitting up the app.py into seperate files and folders for improved structure  

---

## 📄 License

MIT License  

---

## 🙌 Final Notes

This project demonstrates a **complete RAG architecture** without external dependencies for embeddings—making it perfect for understanding how everything fits together before scaling to production systems.