import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

def get_synthesizer_llm() -> ChatGoogleGenerativeAI:
    """
    Initializes and returns the Chat LLM for generation.
    Uses 'gemini-2.5-flash' with temperature=0.3 for a balance of creativity and grounding.
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable is not set. Please add it to your .env file.")
        
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=api_key,
        temperature=0.3
    )

def create_synthesizer():
    """
    Creates and returns a runnable Generative Synthesizer chain.
    """
    llm = get_synthesizer_llm()
    
    system = """You are an assistant for question-answering tasks. 
Use the following pieces of retrieved context to answer the question. 
If you don't know the answer, just say that you don't know. 
Keep the answer concise, accurate, and completely grounded in the provided context."""
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system),
        ("human", "Context:\n\n{context}\n\nQuestion: {question}\n\nAnswer:")
    ])
    return prompt | llm | StrOutputParser()
