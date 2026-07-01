<div align="center">
  <h1>🔬 Enterprise Medical Research Assistant (RAG)</h1>
  <p>An intelligent Retrieval-Augmented Generation (RAG) platform for querying clinical research papers and medical literature.</p>

  <h3><a href="https://huggingface.co/spaces/ruchira1212/medical-rag-bot">🔴 Live Demo on Hugging Face Spaces</a></h3>

  [![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](#)
  [![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
  [![LlamaIndex](https://img.shields.io/badge/LlamaIndex-000000?style=for-the-badge)](#)
  [![ChromaDB](https://img.shields.io/badge/ChromaDB-FC5200?style=for-the-badge)](#)
  [![HuggingFace](https://img.shields.io/badge/HuggingFace-FFD21E?style=for-the-badge&logo=huggingface&logoColor=black)](https://huggingface.co/spaces/ruchira1212/medical-rag-bot)
</div>

---

## 🌟 Overview

**Enterprise Medical Research Assistant** is a production-ready RAG application designed to assist healthcare professionals and researchers in extracting rapid, accurate, and evidence-based answers from complex clinical literature. 

By utilizing advanced Natural Language Processing and Vector Search, this tool dynamically parses uploaded medical PDFs, embeds the content using specialized medical models, and generates synthesized answers alongside exact source citations to ensure total transparency. 

## 🚀 Key Modules & Features

The platform is designed to handle document processing, semantic search, and generation seamlessly in real-time.

| Module | Core Functionalities |
| ------ | -------------------- |
| 📁 **Dynamic Ingestion** | Drag-and-drop interface to instantly upload, parse, and embed new medical PDF documents into the knowledge base. |
| 🧠 **Medical Embeddings** | Utilizes **PubMedBERT** (`NeuML/pubmedbert-base-embeddings`) for highly accurate vector representations of clinical text. |
| 🗄️ **Vector Storage** | Persistent local storage via **ChromaDB**, ensuring rapid semantic retrieval without external database dependencies. |
| 🤖 **LLM Inference** | Powered by **Qwen 2.5 7B Instruct** via the HuggingFace Serverless Inference API for highly contextual medical answers. |
| 📑 **Source Citations** | Mitigates AI hallucinations by strictly citing the exact PDF file name, page number, and text snippet used to generate the answer. |
| 🔒 **Secure Auth** | Integrated Hugging Face Secret management for secure API token handling with a user-friendly UI fallback. |

## 🛠️ Technology Stack

Our platform is constructed using modern, scalable, and robust AI and web technologies:
* **Frontend:** Streamlit.
* **Orchestration:** LlamaIndex.
* **Vector Database:** ChromaDB.
* **Embeddings:** HuggingFace `pubmedbert-base-embeddings`.
* **LLM:** HuggingFace Inference API (`Qwen/Qwen2.5-7B-Instruct`).
* **Deployment:** Docker, optimized for Hugging Face Spaces.

## 🗂️ Project Structure

The repository is modularized for straightforward local development and easy deployment:
```text
medical-rag-assistant/
├── 📁 data/                 # Directory to store initial or sample medical PDFs
├── 📁 chromadb_storage/     # Persistent local vector database files
├── 📄 app.py                # Main Streamlit application and RAG pipeline logic
├── 📄 ingestion.py          # Scripts for bulk document ingestion (Optional)
├── 📄 requirements.txt      # Python dependencies
├── 📄 Dockerfile            # Container configuration for HF Spaces
└── 📄 README.md             # Project documentation
```

## ⚙️ Getting Started

Follow these steps to run the Medical RAG Assistant locally.

### 1️⃣ Dependencies Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/Ruchira-Rukshan/medical-rag-assistant.git
   cd medical-rag-assistant
   ```
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### 2️⃣ API Token Configuration
You will need a HuggingFace Access Token to communicate with the LLM Inference API.
1. Create a free account at [HuggingFace](https://huggingface.co/).
2. Generate an Access Token via your profile settings.
3. You can either set it as an environment variable (`HF_TOKEN`) or enter it directly through the application's sidebar when it launches.

### 3️⃣ Run the Application
Open a terminal and start the Streamlit frontend.
```bash
streamlit run app.py
```
The application will be accessible via your browser at `http://localhost:8501/`.

### 4️⃣ Deploy to Hugging Face Spaces
This project is fully Dockerized. To deploy:
1. Create a new Space on Hugging Face (choose Docker as the environment).
2. Set your `HF_TOKEN` in the Space's **Secrets** configuration.
3. Push this repository's contents to the Space.

---

<div align="center">
  <i>Developed and Maintained by Ruchira Rukshan.</i>
</div>
