import sys
import importlib

packages = [
    "langgraph",
    "langchain_google_genai",
    "chromadb",
    "duckduckgo_search",
    "dotenv",
    "pypdf",
    "pytest"
]

print("Verifying core dependencies for Self-Corrective RAG system:")
success = True
for pkg in packages:
    try:
        importlib.import_module(pkg)
        print(f"  [PASS] Successfully imported {pkg}")
    except ImportError as e:
        print(f"  [FAIL] Failed to import {pkg}: {e}")
        success = False

if success:
    print("\nAll core packages successfully imported. Environment is healthy!")
    sys.exit(0)
else:
    print("\nOne or more core packages failed to import.")
    sys.exit(1)
