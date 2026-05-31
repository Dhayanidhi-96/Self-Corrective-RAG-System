import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
# Load environment variables (pulls GOOGLE_API_KEY)
load_dotenv()
PERSIST_DIRECTORY = os.path.join("data", "chromadb")
COLLECTION_NAME = "rag_collection"
def get_embedding_model() -> GoogleGenerativeAIEmbeddings:
    """
    Initializes and returns the Google Generative AI Embeddings model.
    Uses 'models/gemini-embedding-2' by default.
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable is not set. Please add it to your .env file.")
        
    return GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-2",
        google_api_key=api_key
    )
def get_vectorstore(persist_directory: str = PERSIST_DIRECTORY) -> Chroma:
    """
    Initializes and returns a persistent Chroma vector store instance.
    """
    embeddings = get_embedding_model()
    return Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
        persist_directory=persist_directory
    )
def add_documents_to_vectorstore(documents, persist_directory: str = PERSIST_DIRECTORY) -> Chroma:
    """
    Creates/updates a local Chroma vector database and stores chunks with their embeddings.
    """
    embeddings = get_embedding_model()
    return Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=persist_directory,
        collection_name=COLLECTION_NAME
    )