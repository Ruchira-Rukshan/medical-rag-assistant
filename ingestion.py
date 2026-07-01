import os
import chromadb
from llama_index.core import SimpleDirectoryReader, StorageContext, VectorStoreIndex, Settings
from llama_index.core.node_parser import SentenceSplitter
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.chroma import ChromaVectorStore

def build_medical_knowledge_base():
    print("🔄 Step 1: Loading Medical PDFs from ./data...")
    if not os.path.exists("./data") or os.listdir("./data") == []:
        print("❌ Error: Please add some medical PDFs inside the './data' folder first!")
        return

    # Load all documents from the local directory
    reader = SimpleDirectoryReader("./data")
    documents = reader.load_data()
    print(f"✅ Loaded {len(documents)} pages/documents.")

    print("🧬 Step 2: Loading PubMedBERT Medical Embedding Model...")
    # Using a specialized biomedical model to accurately capture complex medical terms
    Settings.embed_model = HuggingFaceEmbedding(
        model_name="NeuML/pubmedbert-base-embeddings"
    )

    # Configure the chunk size and overlap to keep paragraphs and clinical context intact
    Settings.node_parser = SentenceSplitter(chunk_size=512, chunk_overlap=50)

    print("📦 Step 3: Setting up Local ChromaDB Storage...")
    db = chromadb.PersistentClient(path="./chromadb_storage")
    chroma_collection = db.get_or_create_collection("medical_kb")
    
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    print("🧠 Step 4: Indexing and Embedding Documents (Please wait)...")
    index = VectorStoreIndex.from_documents(
        documents, storage_context=storage_context
    )
    
    print("🎉 Success: Vector Database built and saved to './chromadb_storage'!")

if __name__ == "__main__":
    build_medical_knowledge_base()
