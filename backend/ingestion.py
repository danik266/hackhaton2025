# ingestion.py
from pathlib import Path
from langchain.text_splitter import RecursiveCharacterTextSplitter
import fitz  # PyMuPDF
import docx

def load_pdf(path):
    doc = fitz.open(path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def load_txt(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def load_docx(path):
    doc = docx.Document(path)
    text = "\n".join([p.text for p in doc.paragraphs])
    return text

def load_documents(folder="data"):
    docs = []
    for file in Path(folder).iterdir():
        if file.suffix.lower() == ".pdf":
            docs.append({"content": load_pdf(file), "source": file.name})
        elif file.suffix.lower() == ".txt":
            docs.append({"content": load_txt(file), "source": file.name})
        elif file.suffix.lower() == ".docx":
            docs.append({"content": load_docx(file), "source": file.name})
    return docs

def chunk_documents(documents, chunk_size=500, overlap=50):
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=overlap)
    chunks = []
    for doc in documents:
        split = splitter.split_text(doc["content"])
        for s in split:
            chunks.append({"content": s, "source": doc["source"]})
    return chunks
