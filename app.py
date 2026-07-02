import streamlit as st
import chromadb
import os
import shutil
from llama_index.core import VectorStoreIndex, Settings, SimpleDirectoryReader, PromptTemplate
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.llms.huggingface_api import HuggingFaceInferenceAPI

# Page configuration
st.set_page_config(page_title="Medical Research RAG Assistant", page_icon="🔬", layout="wide")
st.title("🔬 Enterprise Medical Research Assistant (RAG)")
st.write("Ask professional questions based on existing or newly uploaded medical literature.")

# Initialize Models inside LlamaIndex Settings
@st.cache_resource
def load_rag_pipeline(hf_token):
    Settings.embed_model = HuggingFaceEmbedding(model_name="NeuML/pubmedbert-base-embeddings")
    
    # HuggingFace Serverless Inference API setup
    Settings.llm = HuggingFaceInferenceAPI(
        model_name="Qwen/Qwen2.5-7B-Instruct",
        token=hf_token,
        request_timeout=120.0
    )
    
    # Connect to persistent ChromaDB storage
    db = chromadb.PersistentClient(path="./chromadb_storage")
    chroma_collection = db.get_or_create_collection("medical_kb")
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    
    index = VectorStoreIndex.from_vector_store(vector_store)
    return index

try:
    # 🔒 SECURE AUTHENTICATION: Check if token is available in Space Secrets
    hf_token = os.getenv("HF_TOKEN", "")
    
    # If the secret is NOT set on Hugging Face, show the sidebar input box as a backup
    if not hf_token:
        st.sidebar.header("🔑 Authentication")
        hf_token = st.sidebar.text_input(
            "HuggingFace Token", 
            type="password", 
            help="Securely enter your token here, or configure HF_TOKEN in your Space Settings for auto-login."
        )
        
    # Stop execution if no token is provided anywhere
    if not hf_token:
        st.warning("⚠️ Please enter your HuggingFace Token or set the 'HF_TOKEN' Secret in Space Settings to enable the LLM.")
        st.stop()

    # 1. Load the core pipeline and index
    index = load_rag_pipeline(hf_token)
    
    # 🌟 DYNAMIC UPLOADER SIDEBAR 🌟
    st.sidebar.header("📁 Upload New Medical Papers")
    uploaded_file = st.sidebar.file_uploader("Drag and drop your medical PDF here", type=["pdf"])
    
    if 'processed_files' not in st.session_state:
        st.session_state.processed_files = set()
        
    if uploaded_file is not None:
        if uploaded_file.name not in st.session_state.processed_files:
            # temporary folder 
            temp_dir = "./temp_upload"
            os.makedirs(temp_dir, exist_ok=True)
            file_path = os.path.join(temp_dir, uploaded_file.name)
            
            # Save uploaded file to disk temporarily
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
                
            with st.spinner("🧬 Parsing & Embedding new document..."):
                # Read the new PDF from the temp folder
                reader = SimpleDirectoryReader(temp_dir)
                new_documents = reader.load_data()
                
                # Insert new document into the existing index (This auto-updates ChromaDB too!)
                for doc in new_documents:
                    index.insert(doc)
                    
                # Clean up the temp directory after ingestion
                shutil.rmtree(temp_dir)
                
                st.session_state.processed_files.add(uploaded_file.name)
                st.sidebar.success(f"🎉 Successfully indexed: {uploaded_file.name}!")
        else:
            st.sidebar.info(f"📁 Ready for questions based on: {uploaded_file.name}")

    # --- CHAT INTERFACE ---
    qa_prompt_tmpl_str = (
        "Context information is below.\n"
        "---------------------\n"
        "{context_str}\n"
        "---------------------\n"
        "You are an expert medical assistant. Answer the query using ONLY the context information above.\n"
        "If the answer cannot be found in the context, or if the user asks a math problem, greeting, or general trivia, you must strictly answer: 'I cannot find the answer in the provided research documents.'\n"
        "Query: {query_str}\n"
        "Answer: "
    )
    qa_prompt_tmpl = PromptTemplate(qa_prompt_tmpl_str)
    
    query_engine = index.as_query_engine(similarity_top_k=3, text_qa_template=qa_prompt_tmpl)
    user_query = st.text_input("Enter your medical or clinical research question:", placeholder="e.g., What does the text say about the sensitivity of rapid antigen tests?")
    
    if user_query:
        with st.spinner("Analyzing research papers and generating response..."):
            response = query_engine.query(user_query)
            
            st.subheader("💡 Analysis & Answer:")
            st.write(response.response)
            
            # Only show sources if the model actually found an answer
            if "I cannot find the answer" not in response.response:
                st.markdown("---")
                st.subheader("📑 Source Citations & Context Evidence:")
                for i, node in enumerate(response.source_nodes):
                    metadata = node.node.metadata
                    file_name = metadata.get('file_name', 'Unknown File')
                    page_no = metadata.get('page_label', 'Unknown Page')
                    score = round(node.score, 4) if node.score else "N/A"
                    
                    with st.expander(f"Source {i+1}: {file_name} (Page {page_no}) | Confidence Score: {score}"):
                        st.write(f"*{node.node.get_content()}*")

except Exception as e:
    st.error(f"Error loading pipeline: {e}")