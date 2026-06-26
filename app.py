import os
import string
import uuid
import chromadb
import gradio as gr

from PyPDF2 import PdfReader
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

# -----------------------------
# Configuration
# -----------------------------

DB_PATH = "./my_vector_db"

client = chromadb.PersistentClient(path=DB_PATH)

embedder = SentenceTransformer("all-MiniLM-L6-v2")

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash"
)

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

# -----------------------------
# Chroma Collection
# -----------------------------

def get_collection():
    return client.get_or_create_collection(
        name="pdf_documents"
    )

# -----------------------------
# PDF Indexing
# -----------------------------

def process_pdf(pdf_file):

    if pdf_file is None:
        return "Please upload a PDF."

    try:

        reader = PdfReader(pdf_file.name)

        text = "".join(
            page.extract_text() or ""
            for page in reader.pages
        )

        if not text.strip():
            return (
                "Error: No text extracted. "
                "Is the PDF image-based?"
            )

        print("Contains ZIMOMO:", "ZIMOMO" in text)
        print("Contains Zimomo:", "Zimomo" in text)
        print("Contains zimomo:", "zimomo" in text)

        filename = os.path.basename(pdf_file.name)

        chunks = splitter.split_text(text)

        embeddings = embedder.encode(
            chunks,
            normalize_embeddings=True
        ).tolist()

        ids = [
            str(uuid.uuid4())
            for _ in chunks
        ]

        metadatas = [
            {"source": filename}
            for _ in chunks
        ]

        collection = get_collection()

        existing = collection.get(
            where={"source": filename}
        )

        if existing and existing.get("ids"):
            return (
                f"PDF '{filename}' has already "
                f"been indexed."
            )

        collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=chunks,
            metadatas=metadatas
        )

        print(
            f"Indexed: {filename} "
            f"({len(chunks)} chunks)"
        )

        return (
            f"Successfully indexed "
            f"{filename} "
            f"({len(chunks)} chunks)"
        )

    except Exception as e:
        return f"Indexing Error: {str(e)}"

# -----------------------------
# Chat
# -----------------------------

def chat_response(message, history):

    message_lower = (
        message.lower()
        .translate(str.maketrans("", "", string.punctuation))
        .strip()
    )

    small_talk = {
        "hi",
        "hello",
        "hey",
        "good morning",
        "good afternoon",
        "good evening",
        "thanks",
        "thank you",
        "bye",
        "goodbye"
    }
   
    if message_lower in small_talk:
        return llm.invoke(message).content

    collection = get_collection()

    total_chunks = collection.count()

    print(
        f"Chat Search: "
        f"{total_chunks} chunks"
    )

    if total_chunks == 0:
        return (
            "The database is empty. "
            "Please upload and index "
            "a PDF first."
        )

    query_embedding = embedder.encode(
        [message],
        normalize_embeddings=True
    ).tolist()

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=min(total_chunks, 3),
        include=["documents", "metadatas", "distances"]
    )

    print("\n===== Raw Query Results =====")
    print("Metadatas:")
    print(results["metadatas"])

    print("\nDistances:")
    print(results["distances"])

    print("\nDocuments:")
    print(results["documents"])

    if (
        not results["documents"]
        or not results["documents"][0]
    ):
        return "No relevant information found."

    sources = {
        m["source"]
        for m in results["metadatas"][0]
        if m is not None
    }

    print("\nRetrieved chunks:")

    for i, (doc, meta, distance) in enumerate(
        zip(results["documents"][0], results["metadatas"][0], results["distances"][0]), 1
    ):
        print(f"\nChunk {i}")
        print("Source:", meta["source"])
        print("Distance:", distance)
        print(doc[:300])

    context = ""

    for i, (doc, meta) in enumerate(
        zip(results["documents"][0], results["metadatas"][0]),
        start=1,
    ):
        context += (
            f"========== Chunk {i} ==========\n"
            f"Source: {meta['source']}\n\n"
            f"{doc}\n\n"
        )

    prompt = f"""
You are a helpful assistant.

For greetings, thanks, farewells,
and simple conversational messages,
respond naturally.

For questions about uploaded documents,
answer using only the retrieved context below.

If the answer is explicitly stated,
extract it faithfully.

Do not add information that is not present
in the retrieved context.

If multiple documents or multiple entities
contain similar information,
choose the answer that is most directly
supported by the retrieved context.

If the retrieved context does not contain
enough information to answer the question,
reply exactly:

"I cannot find that information in the uploaded documents."

Context:
{context}

Question:
{message}
"""

    try:

        response = llm.invoke(prompt)

        print("\n===== Prompt =====")
        print(prompt)

        return (
            response.content
            + "\n\nSources:\n"
            + "\n".join(sorted(sources))
        )

    except Exception:

        return (
            "The language model is currently "
            "unavailable. This may be due to "
            "API quota limits or temporary "
            "service issues. Please try again later."
        )

# -----------------------------
# Gradio UI
# -----------------------------

with gr.Blocks() as demo:

    gr.Markdown(
        "# Persistent PDF RAG Chatbot"
    )

    with gr.Row():

        pdf_input = gr.File(
            label="Upload PDF",
            file_types=[".pdf"]
        )

        status = gr.Textbox(
            label="Status",
            interactive=False
        )

    upload_btn = gr.Button(
        "Index PDF"
    )

    upload_btn.click(
        process_pdf,
        inputs=[pdf_input],
        outputs=[status]
    )

    gr.ChatInterface(
        fn=chat_response
    )

if __name__ == "__main__":
    demo.launch()