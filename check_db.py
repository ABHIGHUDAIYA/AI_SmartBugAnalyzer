import os
import sys
import warnings
warnings.filterwarnings('ignore')

from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

print("Connecting to local ChromaDB...")
try:
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = Chroma(persist_directory="chroma_db", embedding_function=embeddings)
    
    collection = vectorstore._collection
    count = collection.count()
    print(f"\nTotal records in Knowledge Base: {count}")
    
    if count > 0:
        print("\nFetching recent additions...")
        results = collection.get()
        
        # We only want to look at bugs we manually added (which start with 'KB-ADDED-')
        kb_added = [meta for meta in results['metadatas'] if meta and meta.get('bug_id', '').startswith('KB-ADDED-')]
        
        if len(kb_added) > 0:
            print(f"\nFound {len(kb_added)} manually added resolution(s)!")
            for idx, meta in enumerate(kb_added[-5:]): # Show last 5
                print(f"\n--- Entry {idx+1} ---")
                print(f"Bug ID: {meta.get('bug_id')}")
                print(f"Short Description: {meta.get('short_description')}")
                print(f"Stored Resolution: {meta.get('resolution_metadata')[:100]}...")
        else:
            print("\nNo manually added bugs (starting with 'KB-ADDED-') found yet.")
except Exception as e:
    print(f"Error connecting to ChromaDB: {e}")
