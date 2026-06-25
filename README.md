# 🚀 Multi-PDF RAG Chatbot with Persistent Vector Memory

A production-ready Retrieval-Augmented Generation (RAG) chatbot that allows users to chat with multiple PDF documents using semantic search and Google Gemini. The application stores document embeddings in a persistent ChromaDB vector database, eliminating the need to re-index previously uploaded documents.

---

# 🌟 Features

## 📚 Multi-PDF Knowledge Base

Upload and index multiple PDF documents into a shared vector database. The chatbot can retrieve information across all indexed documents.

## 💾 Persistent Vector Memory

Uses ChromaDB Persistent Client to store embeddings locally, allowing indexed documents to remain available across application restarts.

## 🔍 Semantic Search

Leverages Sentence Transformers (`all-MiniLM-L6-v2`) to perform meaning-based retrieval rather than simple keyword matching.

## 🧠 Retrieval-Augmented Generation (RAG)

Retrieves relevant document chunks and grounds responses using Google Gemini.

## 🏷️ Source Attribution

Displays the source document(s) used to answer each question.

## 🚫 Duplicate Detection

Prevents the same PDF from being indexed multiple times.

## 🐳 Dockerized Deployment

Fully containerized for consistent deployment across development and production environments.

## 🎨 User-Friendly Interface

Built with Gradio for a simple drag-and-drop document upload experience.

---

# 🏗️ Architecture

```text
                    ┌─────────────┐
                    │ PDF Upload  │
                    └──────┬──────┘
                           │
                           ▼
                  ┌────────────────┐
                  │    PyPDF2      │
                  │ Text Extraction│
                  └───────┬────────┘
                          │
                          ▼
           ┌──────────────────────────────┐
           │ RecursiveCharacterTextSplitter│
           └──────────────┬───────────────┘
                          │
                          ▼
              ┌───────────────────────┐
              │ Sentence Transformers │
              │ all-MiniLM-L6-v2      │
              └───────────┬───────────┘
                          │
                          ▼
                ┌──────────────────┐
                │     ChromaDB     │
                │ Persistent Store │
                └────────┬─────────┘
                         │
                         ▼
                  User Question
                         │
                         ▼
                 Similarity Search
                         │
                         ▼
                 Relevant Chunks
                         │
                         ▼
                  Google Gemini
                         │
                         ▼
                   Final Answer
```

---

# 🛠️ Technology Stack

| Component        | Technology              |
| ---------------- | ----------------------- |
| LLM              | Google Gemini 2.5 Flash |
| Framework        | LangChain               |
| Vector Database  | ChromaDB                |
| Embedding Model  | all-MiniLM-L6-v2        |
| PDF Processing   | PyPDF2                  |
| Frontend         | Gradio                  |
| Containerization | Docker                  |
| Language         | Python 3.10             |

---

# 📂 Project Structure

```plaintext
pdf-rag-chat/
├── .gradio/
├── app.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── my_vector_db/
├── hf_cache/
├── README.md
├── LICENSE
└── .env
```

---

# 🚀 Getting Started

## Prerequisites

* Python 3.10+
* Docker (optional)
* Google Gemini API Key

Obtain an API key from:

https://aistudio.google.com

---

# Installation

## Clone Repository

```bash
git clone https://github.com/HJ1981/pdf-rag-chat.git
cd pdf-rag-chat
```

## Create Environment

```bash
conda create -n rag python=3.10 -y
conda activate rag
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Configuration

Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=your_google_api_key_here
```

---

# Running the Application

## Local Execution

```bash
python app.py
```

---

## Docker Deployment

Build and start the application:

```bash
docker compose up --build
```

Application URL:

```text
http://localhost:7860
```

Stop the application:

```bash
docker compose down
```

---

# 🧠 How It Works

## Step 1: Document Ingestion

The uploaded PDF is processed using PyPDF2 to extract raw text.

## Step 2: Text Chunking

The document is split into chunks of:

* Chunk Size: 1000 characters
* Chunk Overlap: 200 characters

This preserves contextual continuity during retrieval.

## Step 3: Embedding Generation

Each chunk is converted into a dense vector representation using:

```text
all-MiniLM-L6-v2
```

## Step 4: Persistent Storage

Embeddings, chunks, and metadata are stored in ChromaDB.

Metadata includes:

```python
{
    "source": "filename.pdf"
}
```

## Step 5: Similarity Search

When a user submits a question:

1. The question is embedded.
2. ChromaDB performs vector similarity search.
3. Top matching chunks are retrieved.

## Step 6: Response Generation

The retrieved context is passed to Google Gemini, which generates a grounded answer.

---

# 💬 Example Questions

* What services does ABC Bank provide?
* Summarize the key findings of this report.
* What are the eligibility criteria mentioned in the document?
* Extract all important dates from the PDF.
* Which document mentions Zimomo?

---

# 💾 Persistent Storage

The application stores data locally:

```plaintext
./my_vector_db
```

Benefits:

* No re-indexing after restart
* Faster startup
* Persistent knowledge base

---

# 🐳 Docker Persistence

The application persists:

| Folder       | Purpose                  |
| ------------ | ------------------------ |
| my_vector_db | ChromaDB storage         |
| hf_cache     | Hugging Face model cache |

This prevents repeated model downloads and preserves indexed documents.

---

# ⚠️ Current Limitations

* Supports text-based PDFs only
* Scanned PDFs require OCR
* Single-user deployment architecture
* Depends on Gemini API availability and quota limits
* No document management UI yet

---

# 🚀 Future Enhancements

* OCR support using Tesseract
* Hybrid Search (BM25 + Vector Search)
* Conversation Memory
* Document Management Dashboard
* User Authentication
* Cloud Deployment (AWS/GCP/Azure)
* Citation Highlighting
* Streaming Responses

---

# 🔒 Security

Never commit secrets to GitHub.

Add the following to `.gitignore`:

```gitignore
.env
.gradio/
my_vector_db/
hf_cache/
```

---

# 📜 License

This project is licensed under the MIT License.

---

# 👨‍💻 Author

HJJ1981

GitHub:
https://github.com/HJJ1981

LinkedIn:
https://www.linkedin.com/in/jian-jin-hu-69951243/

---

If you found this project useful, consider giving it a ⭐ on GitHub.
