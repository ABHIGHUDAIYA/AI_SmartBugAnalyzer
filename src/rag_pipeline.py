import os
from data_processing import load_and_clean_data
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document

def build_knowledge_base(csv_filename):
    print("Step 1: Loading and cleaning data...")
    df = load_and_clean_data(csv_filename)
    if df is None or df.empty:
        print("Data loading failed. Exiting.")
        return

    print("Step 2: Converting to LangChain Documents...")
    documents = []
    # Using 'long_description' as the main text to embed
    for index, row in df.iterrows():
        text = str(row.get('long_description', ''))
        if not text.strip():
            continue
            
        metadata = {
            "bug_id": str(row.get('bug_id', 'unknown')),
            "short_description": str(row.get('short_description', '')),
            "resolution": str(row.get('resolution_category', ''))
        }
        documents.append(Document(page_content=text, metadata=metadata))

    print(f"Created {len(documents)} document records.")
    
    # We only take the first 500 for prototype/speed purposes
    documents = documents[:500]
    print(f"Using {len(documents)} documents for quick prototype indexing...")

    print("Step 3: Chunking documents...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Generated {len(chunks)} chunks.")

    print("Step 4: Generating Embeddings & Storing in ChromaDB...")
    # Using a free, local huggingface model
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    # Save to a local folder named 'chroma_db'
    persist_directory = "../chroma_db"
    
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=persist_directory
    )
    print(f"Successfully indexed {len(chunks)} chunks into ChromaDB at '{persist_directory}'!")
    print("RAG Pipeline Knowledge Base is fully built and ready!")

if __name__ == "__main__":
    # Find dataset in parent dir (since this script is inside src/)
    dataset_files = [f for f in os.listdir('..') if f.upper().startswith('DATASET') and f.endswith('.csv')]
    if dataset_files:
        # Pass the relative path from inside src/
        build_knowledge_base(f"../{dataset_files[0]}")
    else:
        print("Could not find DATASET.csv. Please place it in the project root.")
