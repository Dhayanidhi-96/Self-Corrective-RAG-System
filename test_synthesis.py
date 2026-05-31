import os
import sys
from app.retrieval.vectorstore import get_vectorstore
from app.generation.synthesizer import create_synthesizer
from app.critique.graders import create_document_grader, create_hallucination_grader, create_answer_grader

def main():
    print("=" * 60)
    print("[*] Starting LLM Synthesis & Critique Grader Test Script...")
    print("=" * 60)
    
    # 1. Initialize vectorstore and retrieve document
    try:
        vectorstore = get_vectorstore()
        question = "What is the recipe for chocolate chip cookies?"
        print(f"[*] Querying local ChromaDB for: '{question}'...")
        results = vectorstore.similarity_search(question, k=1)
        
        if not results:
            print("[-] No documents found in database. Please run: python ingest.py first.")
            sys.exit(1)
            
        doc_content = results[0].page_content
        source_file = os.path.basename(results[0].metadata.get('source', 'Unknown'))
        print(f"[+] Retrieved document successfully (Source: {source_file}).")
        print(f"    Content Preview: \"{doc_content[:150]}...\"\n")
    except Exception as e:
        print(f"[-] Database query failed: {e}")
        sys.exit(1)
        
    # 2. Test Document Relevance Grader
    try:
        print("[*] 1. Grading retrieved document relevance to query...")
        doc_grader = create_document_grader()
        grade_doc = doc_grader.invoke({"question": question, "document": doc_content})
        print(f"[+] Relevance Grade (yes/no): '{grade_doc.binary_score}'\n")
    except Exception as e:
        print(f"[-] Document grading failed: {e}")
        sys.exit(1)
        
    # 3. Test Generative Synthesizer
    try:
        print("[*] 2. Synthesizing answer using gemini-1.5-flash...")
        synthesizer = create_synthesizer()
        answer = synthesizer.invoke({"question": question, "context": doc_content})
        print(f"[+] Generated Answer:\n    \"{answer}\"\n")
    except Exception as e:
        print(f"[-] Answer synthesis failed: {e}")
        sys.exit(1)
        
    # 4. Test Hallucination Grader (Grounded Answer)
    try:
        print("[*] 3. Checking Synthesized Answer for hallucinations...")
        hallucination_grader = create_hallucination_grader()
        grade_hallucination = hallucination_grader.invoke({"documents": doc_content, "generation": answer})
        print(f"[+] Grounded Grade (yes = grounded, no = hallucinated): '{grade_hallucination.binary_score}'\n")
    except Exception as e:
        print(f"[-] Hallucination grading failed: {e}")
        sys.exit(1)
        
    # 5. Test Answer Utility Grader
    try:
        print("[*] 4. Grading Answer Utility (does it resolve the question?)...")
        answer_grader = create_answer_grader()
        grade_utility = answer_grader.invoke({"question": question, "generation": answer})
        print(f"[+] Answer Utility Grade (yes/no): '{grade_utility.binary_score}'\n")
    except Exception as e:
        print(f"[-] Utility grading failed: {e}")
        sys.exit(1)
        
    # 6. Test Hallucination Grader (Fictional / Fake Answer)
    try:
        fake_answer = "Alan Turing was an American astronaut who became the first man to walk on Mars in 1969."
        print(f"[*] 5. Simulating a hallucination test using fake answer:\n    \"{fake_answer}\"")
        grade_fake_hallucination = hallucination_grader.invoke({"documents": doc_content, "generation": fake_answer})
        print(f"[+] Grounded Grade for Fake Answer (should be 'no'): '{grade_fake_hallucination.binary_score}'\n")
        
        if grade_fake_hallucination.binary_score == "no":
            print("[SUCCESS] Hallucination Grader successfully detected the hallucination!")
        else:
            print("[WARNING] Hallucination Grader failed to detect the fake answer.")
    except Exception as e:
        print(f"[-] Simulated hallucination test failed: {e}")
        sys.exit(1)
        
    print("\n" + "=" * 60)
    print("[+] All Grader and Synthesizer tests completed successfully!")
    print("=" * 60)

if __name__ == "__main__":
    main()
