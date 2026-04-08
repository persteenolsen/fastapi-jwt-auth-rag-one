# app.py
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import uvicorn
from dotenv import load_dotenv
import os
from pydantic import BaseModel
from groq import Groq
from sqlalchemy import create_engine, text
import numpy as np
import jwt

# -----------------------------
# Load environment
# -----------------------------
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# 08-04-2026: Updated to use environment variable for JWT secret key
# SECRET_KEY = os.getenv("JWT_SECRET_KEY", "mysecret")
SECRET_KEY = os.getenv("SECRET_KEY")

DATABASE_URL = os.getenv("DATABASE_URL")

if not GROQ_API_KEY or not DATABASE_URL:
    raise Exception("GROQ_API_KEY or DATABASE_URL not set")

# 08-04-2026: Updated to use environment variables for credentials
FAKE_USERNAME=os.getenv("FAKE_USERNAME")
FAKE_PASSWORD = os.getenv("FAKE_PASSWORD")

# -----------------------------
# FastAPI Setup & Groq Client
# -----------------------------
# app = FastAPI(title="Groq + RAG + JWT Demo")

# Initialize the FastAPI app
app = FastAPI(

    title="Python + FastApi + JWT Auth + RAG + LLM + Groq",
    description="08-04-2026 - FastAPI with JWT Auth serving an RAG Application powered by one of Groq's LLaMA models",
    version="0.0.1",

    contact={
        "name": "Per Olsen",
        "url": "https://persteenolsen.netlify.app",
         },
)

client = Groq(api_key=GROQ_API_KEY)
engine = create_engine(DATABASE_URL)

# -----------------------------
# Security: HTTP Bearer for Swagger UI
# -----------------------------
bearer_scheme = HTTPBearer()  # This enables the "Authorize" button

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    token = credentials.credentials
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return decoded["username"]
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

# -----------------------------
# Pydantic Models
# -----------------------------
class LoginRequest(BaseModel):
    username: str
    password: str

class PromptRequest(BaseModel):
    prompt: str

class DocumentRequest(BaseModel):
    content: str

# -----------------------------
# Embeddings & RAG
# -----------------------------
def simple_embedding(text: str):
    np.random.seed(abs(hash(text)) % (10**6))
    return np.random.rand(384).tolist()

def init_db():
    with engine.connect() as conn:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS documents (
                id SERIAL PRIMARY KEY,
                content TEXT UNIQUE,
                embedding VECTOR(384)
            );
        """))
        conn.commit()

def seed_data():
    docs = [
        "FastAPI is a modern web framework for building APIs with Python.",
        "JWT stands for JSON Web Token and is used for authentication.",
        "RAG stands for Retrieval-Augmented Generation.",
        "Neon provides serverless PostgreSQL with autoscaling.",
        "pgvector allows storing and querying embeddings in PostgreSQL."
    ]
    with engine.connect() as conn:
        for doc in docs:
            # Check if document already exists
            existing_doc = conn.execute(
                text("SELECT 1 FROM documents WHERE content = :content LIMIT 1"),
                {"content": doc}
            ).fetchone()
            
            if not existing_doc:
                # Insert only if the document does not exist
                emb = simple_embedding(doc)
                emb_str = "ARRAY[" + ",".join(map(str, emb)) + "]::vector"
                conn.execute(
                    text(f"INSERT INTO documents (content, embedding) VALUES (:content, {emb_str})"),
                    {"content": doc}
                )
        conn.commit()

# 07-04-2026 - top_k parameter controls the number of retrieved documents from the PostgreSQL 
# ( Here were are taking the 5 documents with the closest embeddings to the query embedding )
def retrieve_context(query: str, top_k: int = 5):
    query_emb = simple_embedding(query)
    query_emb_str = "ARRAY[" + ",".join(map(str, query_emb)) + "]::vector"
    with engine.connect() as conn:
        result = conn.execute(
            text(f"""
                SELECT content
                FROM documents
                ORDER BY embedding <-> {query_emb_str}
                LIMIT :k
            """),
            {"k": top_k}
        )
        return [row[0] for row in result.fetchall()]

def groq_response(prompt: str):
    response = client.chat.completions.create(
        model="allam-2-7b",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1000,
        temperature=0.7
    )
    return response.choices[0].message.content

# -----------------------------
# API Routes
# -----------------------------
@app.get("/")
def root():
    return {"message": "Welcome to theFastAPI + JWT + RAG + Groq demo!"}

@app.post("/login")
def login(request: LoginRequest):
    
    # Simple demo authentication
    # 08-04-2026: Updated to use environment variables for credentials
    # if request.username == "admin" and request.password == "password123":
    if request.username == FAKE_USERNAME and request.password == FAKE_PASSWORD:
        token = jwt.encode({"username": request.username}, SECRET_KEY, algorithm="HS256")
        return {"token": token}
    raise HTTPException(status_code=401, detail="Invalid credentials")

@app.post("/api/generate-response")
def generate_response(request: PromptRequest, user: str = Depends(verify_token)):
    try:
        context_docs = retrieve_context(request.prompt)
        prompt = f"Context:\n{chr(10).join(context_docs)}\nQuestion:\n{request.prompt}"
        response = groq_response(prompt)
        return {"response": response, "context_used": context_docs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/add-document")
def add_document(request: DocumentRequest, user: str = Depends(verify_token)):
    try:
        emb = simple_embedding(request.content)
        emb_str = "ARRAY[" + ",".join(map(str, emb)) + "]::vector"
        with engine.connect() as conn:
            conn.execute(
                text(f"INSERT INTO documents (content, embedding) VALUES (:content, {emb_str})"),
                {"content": request.content}
            )
            conn.commit()
        return {"message": "Document added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# -----------------------------
# Startup Event
# -----------------------------
@app.on_event("startup")
def startup():
    init_db()
    seed_data()

# -----------------------------
# Run server
# -----------------------------
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)