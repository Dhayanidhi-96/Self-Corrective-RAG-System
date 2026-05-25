import os
from langchain_community.document_loaders import DirectoryLoader, TextLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

def load_and_chunk_documents(directory_path: str):
    """
    Loads text and PDF documents from a directory and splits them into smaller chunks.
    """
    print(f"Loading documents from {directory_path}...")
    
    # 1a. Load all .txt files
    txt_loader = DirectoryLoader(
        directory_path, 
        glob="**/*.txt", 
        loader_cls=TextLoader
    )
    txt_docs = txt_loader.load()
    print(f"Loaded {len(txt_docs)} Text document(s).")

    # 1b. Load all .pdf files
    pdf_loader = DirectoryLoader(
        directory_path, 
        glob="**/*.pdf", 
        loader_cls=PyPDFLoader
    )
    pdf_docs = pdf_loader.load()
    print(f"Loaded {len(pdf_docs)} PDF document(s).")
    
    # Combine the documents together!
    documents = txt_docs + pdf_docs
    print(f"Total documents loaded: {len(documents)}")
    
    # 2. Setup the text splitter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,     
        chunk_overlap=200,   
        separators=["\n\n", "\n", " ", ""] 
    )
    
    # Actually split the combined documents
    chunks = text_splitter.split_documents(documents)
    print(f"Successfully split into {len(chunks)} chunk(s).")
    
    return chunks