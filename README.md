# 🚀 Persistent PDF RAG Chatbot

A production-ready Retrieval-Augmented Generation (RAG) chatbot that allows you to "talk" to your PDF documents. This system leverages ChromaDB for persistent memory and Google Gemini for high-quality response generation.

---

# 🌟 Key Features

## Persistent Vector Memory
Uses ChromaDB to store document embeddings locally, so you don't have to re-index the same PDF across different sessions.

## Semantic Search
Implements all-MiniLM-L6-v2 Sentence Transformers for accurate context retrieval.

## Intelligent Chunking
Utilizes LangChain’s RecursiveCharacterTextSplitter to maintain context window integrity.

## Modern UI
A clean, interactive interface powered by Gradio for seamless document uploading and chatting.

## Containerized
Fully Dockerized for consistent deployment across any environment.

---

# 🛠️ Tech Stack

- LLM: Google Gemini API
- Orchestration: LangChain
- Vector Database: ChromaDB
- Embeddings: Sentence Transformers (`all-MiniLM-L6-v2`)
- Frontend: Gradio
- Parsing: PyPDF2

---

# 📂 Project Structure

```plaintext
pdf-rag-chat/
├── my_vector_db/       # Persistent database storage
├── app.py              # Main application logic
├── Dockerfile          # Container configuration
├── docker-compose.yml  # Multi-container orchestration
├── requirements.txt    # Python dependencies
└── .env                # API Keys (Not tracked by Git)
```

---

# 🚀 Getting Started

## 1. Prerequisites

- Python 3.10+ or Conda
- A Google Gemini API Key

Get your API key from Google AI Studio:
https://aistudio.google.com

---

## 2. Installation & Setup

### Clone the Repository

```bash
git clone https://github.com/HJ1981/pdf-rag-chat.git
cd pdf-rag-chat
```

### Create and Activate Environment

```bash
conda create -n rag python=3.10 -y
conda activate rag
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

# ⚙️ Configuration

Create a `.env` file in the root directory:

```env
GOOGLE_API_KEY=your_google_api_key_here
```

---

# ▶️ Running the Application

## Via Python

```bash
python app.py
```

## Via Docker (Recommended)

```bash
docker-compose up --build
```

Once running, access the application at:

```plaintext
http://localhost:7860
```

---

# 🧠 How It Works

## 1. Ingestion
PyPDF2 extracts raw text from the uploaded PDF document.

## 2. Chunking
Text is split into 1,000-character chunks with 200-character overlap to preserve context continuity.

## 3. Vectorization
Chunks are converted into embeddings using Sentence Transformers.

## 4. Retrieval
When a user asks a question, the system retrieves the most semantically relevant chunks from ChromaDB using cosine similarity.

## 5. Generation
The user query and retrieved chunks are passed into Google Gemini to generate grounded and context-aware responses.

---

# 📝 Example Queries

- "Summarize the main arguments of this paper."
- "What are the methodologies mentioned in Chapter 3?"
- "Extract all key dates and deadlines from the document."

---

# 💾 Persistent Database

The vector database is stored locally in:

```plaintext
./my_vector_db
```

This allows embeddings and indexed documents to persist between sessions.

---

# 🔒 Security Note

The `.env` file contains sensitive API keys and should NOT be committed to GitHub.

Add the following to your `.gitignore`:

```gitignore
.env
my_vector_db/
```

---

# 📜 License

This project is licensed under the MIT License.

---
