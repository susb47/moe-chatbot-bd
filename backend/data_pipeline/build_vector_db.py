import os
import json
import faiss
import numpy as np
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer

# Paths
DOCS_DIR = os.path.join(os.path.dirname(__file__), "..", "documents")
DB_DIR = os.path.join(os.path.dirname(__file__), "..", "app", "rag")
FAISS_INDEX_PATH = os.path.join(DB_DIR, "moe_index.faiss")
METADATA_PATH = os.path.join(DB_DIR, "moe_metadata.json")

# Load a fast, multilingual local embedding model (Supports Bengali & English)
print("Loading Embedding Model (This may take a moment the first time)...")
embedder = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

def extract_text_from_pdfs(directory):
    """Reads all PDFs in a folder and chunks the text."""
    chunks = []
    metadata = []
    
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Created {directory}. Please add some PDFs and run again.")
        return chunks, metadata

    for filename in os.listdir(directory):
        if filename.endswith(".pdf"):
            filepath = os.path.join(directory, filename)
            print(f"Processing: {filename}")
            reader = PdfReader(filepath)
            
            for page_num, page in enumerate(reader.pages):
                text = page.extract_text()
                if text:
                    # Simple chunking: split by paragraphs (newlines)
                    paragraphs = [p.strip() for p in text.split('\n\n') if len(p.strip()) > 50]
                    for p in paragraphs:
                        chunks.append(p)
                        metadata.append({
                            "source": filename,
                            "page": page_num + 1
                        })
    return chunks, metadata

def build_faiss_index():
    print("Extracting text from documents...")
    chunks, metadata = extract_text_from_pdfs(DOCS_DIR)
    
    if not chunks:
        print("No text found. Exiting.")
        return

    print(f"Generating embeddings for {len(chunks)} chunks...")
    # Convert text chunks to vector embeddings
    embeddings = embedder.encode(chunks, convert_to_numpy=True)
    
    # Initialize FAISS index
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)
    
    # Save the index and metadata to disk
    os.makedirs(DB_DIR, exist_ok=True)
    faiss.write_index(index, FAISS_INDEX_PATH)
    
    with open(METADATA_PATH, "w", encoding="utf-8") as f:
        json.dump({"chunks": chunks, "metadata": metadata}, f, ensure_ascii=False, indent=2)
        
    print(f"Successfully built FAISS index with {index.ntotal} vectors!")
    print(f"Saved to: {FAISS_INDEX_PATH}")

if __name__ == "__main__":
    build_faiss_index()