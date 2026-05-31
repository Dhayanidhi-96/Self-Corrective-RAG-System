import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

# Define Pydantic Models for Structured Output
class GradeDocument(BaseModel):
    """Binary score for document relevance check."""
    binary_score: str = Field(
        description="Relevance score: 'yes' if document is relevant to the question, else 'no'"
    )

class GradeHallucination(BaseModel):
    """Binary score for hallucination check."""
    binary_score: str = Field(
        description="Hallucination score: 'yes' if the generation is strictly grounded in the documents, else 'no'"
    )

class GradeAnswer(BaseModel):
    """Binary score for checking if the answer actually addresses the user's question."""
    binary_score: str = Field(
        description="Utility score: 'yes' if the answer directly addresses and resolves the user's question, else 'no'"
    )

def get_llm() -> ChatGoogleGenerativeAI:
    """
    Initializes and returns the Gemini Chat LLM.
    Uses 'gemini-2.5-flash' with temperature=0.0 for deterministic grading.
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable is not set. Please add it to your .env file.")
        
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=api_key,
        temperature=0.0
    )

def create_document_grader():
    """
    Creates and returns a runnable Document Relevance Grader chain.
    """
    llm = get_llm()
    structured_llm = llm.with_structured_output(GradeDocument)
    
    system = """You are a grader assessing relevance of a retrieved document to a user question. 
If the document contains keyword(s) or semantic meaning related to the user question, grade it as relevant. 
Give a binary score 'yes' or 'no' to indicate whether the document is relevant to the question."""
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system),
        ("human", "Retrieved Document:\n\n{document}\n\nUser Question: {question}")
    ])
    return prompt | structured_llm

def create_hallucination_grader():
    """
    Creates and returns a runnable Hallucination Grader chain.
    """
    llm = get_llm()
    structured_llm = llm.with_structured_output(GradeHallucination)
    
    system = """You are a grader assessing whether an LLM generation is grounded in / supported by a set of retrieved facts. 
Give a binary score 'yes' or 'no'. 'yes' means the generation is strictly grounded in the facts and does not contain extra ungrounded facts. 'no' means the generation is not grounded in the facts."""
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system),
        ("human", "Set of Facts:\n\n{documents}\n\nLLM Generation:\n\n{generation}")
    ])
    return prompt | structured_llm

def create_answer_grader():
    """
    Creates and returns a runnable Answer Utility Grader chain.
    """
    llm = get_llm()
    structured_llm = llm.with_structured_output(GradeAnswer)
    
    system = """You are a grader assessing whether an answer directly addresses and resolves a user question. 
Give a binary score 'yes' or 'no'. 'yes' means the answer directly addresses and resolves the question. 'no' means the answer does not address the question."""
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system),
        ("human", "User Question: {question}\n\nLLM Answer:\n\n{generation}")
    ])
    return prompt | structured_llm
