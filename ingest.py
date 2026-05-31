import os
import sys
from app.retrieval.loader import load_and_chunk_documents
from app.retrieval.vectorstore import add_documents_to_vectorstore

def main():
    source_dir = os.path.join("data", "source_docs")
    
    print("[*] Starting Ingestion Pipeline: Chunks -> Embeddings -> ChromaDB...")
    
    # 1. Load and chunk documents from data/source_docs/
    try:
        chunks = load_and_chunk_documents(source_dir)
        if not chunks:
            print("[!] No documents found to ingest. Please place some text or PDF files in data/source_docs/.")
            sys.exit(1)
    except Exception as e:
        print(f"[-] Loading/chunking failed: {e}")
        sys.exit(1)
        
    # 2. Embed and store in ChromaDB
    try:
        print(f"[*] Embedding {len(chunks)} chunks and saving to local ChromaDB...")
        vectorstore = add_documents_to_vectorstore(chunks)
        print("[+] Ingestion successful! Vector database persisted in data/chromadb/.")
    except Exception as e:
        print(f"[-] Storing/embedding failed: {e}")
        sys.exit(1)
        
    # 3. Quick verification search if a command-line query is provided
    if len(sys.argv) > 1:
        query = sys.argv[1]
        print(f"\n[*] Running verification similarity search for: '{query}'...")
        try:
            results = vectorstore.similarity_search(query, k=1)
            if results:
                print("[+] Match found! Top matching text chunk retrieved:")
                source_file = os.path.basename(results[0].metadata.get('source', 'Unknown'))
                print(f"\n--- MATCHING CHUNK (Source: {source_file}) ---")
                print(results[0].page_content)
                print("--------------------------------------------------")
            else:
                print("[-] No matching chunks retrieved.")
        except Exception as e:
            print(f"[-] Verification search failed: {e}")

if __name__ == "__main__":
    main()
