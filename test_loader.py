from app.retrieval.loader import load_and_chunk_documents

def main():
    # Tell the script where our sample text file is located
    directory_path = "data/source_docs"
    
    # Call the function we just wrote!
    chunks = load_and_chunk_documents(directory_path)
    
    # Loop through the chunks and print them to the terminal so we can see them
    print("\n--- TEXT CHUNKS ---")
    for i, chunk in enumerate(chunks):
        print(f"\n[CHUNK {i + 1}]")
        print(chunk.page_content)
        print("-" * 50)

if __name__ == "__main__":
    main()