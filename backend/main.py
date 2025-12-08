from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.rag_pipeline import get_answer

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/ask")
def ask(query: str):
    response = get_answer(query)
    return response
