import os
import uuid
import chromadb
import gradio as gr
from PyPDF2 import PdfReader
from sentence_transformers import SentenceTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

# Setup Persistence and Models
DB_PATH = "./my_vector_db"
client = chromadb.PersistentClient(path=DB_PATH)
embedder = SentenceTransformer("all-MiniLM-L6-v2")
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

# Helper function to get or create collection
def get_collection():
    # DEBUG: Check if collection exists before getting or creating
    return client.get_or_create_collection(name="pdf_documents")

def process_pdf(pdf_file):
    # DEBUG: Check if pdf file is received
    if pdf_file is None:
        return "Please upload a PDF."
    
    try:
        reader = PdfReader(pdf_file.name)
        text = "".join([page.extract_text() or "" for page in reader.pages])
        
        if not text.strip():
            return "Error: No text extracted. Is the PDF an image?"

        chunks = splitter.split_text(text) # Split text into chunks
        embeddings = embedder.encode(chunks, normalize_embeddings=True).tolist() # Get embeddings for all chunks
        ids = [str(uuid.uuid4()) for _ in chunks]

        # Reset Collection
        try:
            client.delete_collection("pdf_documents")
        except:
            pass
        # DEBUG: Check if collection is reset before adding new data
        collection = get_collection() # Get or create collection after reset
        collection.add(ids=ids, embeddings=embeddings, documents=chunks) # Add chunks to collection
        
        # DEBUG: Verify count in terminal
        print(f"Index Success: {collection.count()} chunks in DB at {DB_PATH}")
        
        return f"Successfully indexed {len(chunks)} chunks."
    except Exception as e:
        return f"Indexing Error: {str(e)}"

def chat_response(message, history):
    # DEBUG: Check if message is received
    collection = get_collection()
    total_chunks = collection.count() # Get total number of chunks in the collection
    
    # DEBUG: See what the chat function sees
    print(f"Chat Search: Database contains {total_chunks} chunks.")

    if total_chunks == 0:
        return "The database is empty. Please upload and index a PDF first."
    # Perform similarity search
    query_embedding = embedder.encode([message], normalize_embeddings=True).tolist() # Get embedding for the query
    results = collection.query(
        query_embeddings=query_embedding, 
        n_results=min(total_chunks, 3)
    )
    
    if not results["documents"] or not results["documents"][0]:
        return "No relevant information found."
      
    context = "\n\n".join(results["documents"][0]) # Combine retrieved chunks into context
    prompt = f"Use the context below to answer. Context:\n{context}\n\nQuestion: {message}"
    
    response = llm.invoke(prompt) # Generate response using LLM
    return response.content

# Gradio interface
with gr.Blocks() as demo:
    gr.Markdown("# Persistent PDF RAG Chatbot")
    with gr.Row():
        pdf_input = gr.File(label="Upload PDF", file_types=[".pdf"])
        status = gr.Textbox(label="Status", interactive=False)
    upload_btn = gr.Button("Index PDF")
    upload_btn.click(process_pdf, inputs=[pdf_input], outputs=[status])
    gr.ChatInterface(fn=chat_response)

if __name__ == "__main__":
    demo.launch()