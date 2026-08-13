import os
from pathlib import Path

import faiss
import numpy as np
from dotenv import load_dotenv
from groq import Groq
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer


# =========================================================
# CONFIGURATION
# =========================================================

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found in .env")

client = Groq(api_key=GROQ_API_KEY)

DOCUMENTS_DIR = Path("documents")

EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# Use a currently available Groq model from your account.
LLM_MODEL = "llama-3.1-8b-instant"

CHUNK_SIZE = 800
CHUNK_OVERLAP = 150
TOP_K = 4


# =========================================================
# LOAD EMBEDDING MODEL
# =========================================================

print("Loading embedding model...")

embedding_model = SentenceTransformer(
    EMBEDDING_MODEL
)

print("Embedding model loaded.")


# =========================================================
# LOAD PDF DOCUMENTS
# =========================================================

def load_documents():
    documents = []

    pdf_files = list(DOCUMENTS_DIR.glob("*.pdf"))

    if not pdf_files:
        raise FileNotFoundError(
            "No PDF files found inside documents/"
        )

    for pdf_path in pdf_files:

        print(f"Reading: {pdf_path.name}")

        reader = PdfReader(pdf_path)

        for page_number, page in enumerate(reader.pages, start=1):

            text = page.extract_text()

            if not text:
                continue

            documents.append({
                "text": text,
                "source": pdf_path.name,
                "page": page_number
            })

    return documents


# =========================================================
# CHUNK TEXT
# =========================================================

def create_chunks(documents):

    chunks = []

    for document in documents:

        text = document["text"]

        start = 0

        while start < len(text):

            end = start + CHUNK_SIZE

            chunk_text = text[start:end].strip()

            if chunk_text:

                chunks.append({
                    "text": chunk_text,
                    "source": document["source"],
                    "page": document["page"]
                })

            start += CHUNK_SIZE - CHUNK_OVERLAP

    return chunks


# =========================================================
# CREATE EMBEDDINGS
# =========================================================

def create_embeddings(chunks):

    texts = [
        chunk["text"]
        for chunk in chunks
    ]

    embeddings = embedding_model.encode(
        texts,
        normalize_embeddings=True,
        show_progress_bar=True
    )

    return np.asarray(
        embeddings,
        dtype="float32"
    )


# =========================================================
# CREATE FAISS INDEX
# =========================================================

def create_vector_database(embeddings):

    dimension = embeddings.shape[1]

    # Inner product works well with normalized embeddings
    index = faiss.IndexFlatIP(dimension)

    index.add(embeddings)

    return index


# =========================================================
# RETRIEVE RELEVANT DOCUMENTS
# =========================================================

def retrieve(question, index, chunks):

    question_embedding = embedding_model.encode(
        [question],
        normalize_embeddings=True
    )

    question_embedding = np.asarray(
        question_embedding,
        dtype="float32"
    )

    scores, indices = index.search(
        question_embedding,
        TOP_K
    )

    results = []

    for score, index_number in zip(
        scores[0],
        indices[0]
    ):

        if index_number == -1:
            continue

        chunk = chunks[index_number].copy()

        chunk["score"] = float(score)

        results.append(chunk)

    return results


# =========================================================
# BUILD CONTEXT
# =========================================================

def build_context(results):

    context_parts = []

    for i, result in enumerate(results, start=1):

        context_parts.append(
            f"""
SOURCE {i}
File: {result['source']}
Page: {result['page']}
Similarity: {result['score']:.3f}

Content:
{result['text']}
"""
        )

    return "\n".join(context_parts)


# =========================================================
# GENERATE ANSWER
# =========================================================

def generate_answer(question, context, history):

    system_prompt = """
You are a helpful RAG assistant.

Answer questions using the provided document context.

Rules:
1. Use the retrieved context as the primary source.
2. Do not invent information.
3. If the answer is not present in the context, say:
   "I couldn't find that information in the provided documents."
4. Keep answers clear and useful.
5. Mention the source file and page when appropriate.
"""

    messages = [
        {
            "role": "system",
            "content": system_prompt
        }
    ]

    # Add previous conversation
    messages.extend(history)

    messages.append({
        "role": "user",
        "content": f"""
Context:

{context}

Question:

{question}
"""
    })

    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=messages,
        temperature=0.2,
        max_tokens=1000
    )

    return response.choices[0].message.content


# =========================================================
# DISPLAY SOURCES
# =========================================================

def display_sources(results):

    print("\nSources:")

    for result in results:

        print(
            f"- {result['source']} "
            f"(Page {result['page']}, "
            f"Score: {result['score']:.3f})"
        )


# =========================================================
# MAIN
# =========================================================

def main():

    print("\n==============================")
    print("      ADVANCED RAG SYSTEM")
    print("==============================\n")

    # Load documents
    documents = load_documents()

    print(
        f"\nLoaded {len(documents)} pages."
    )

    # Create chunks
    chunks = create_chunks(documents)

    print(
        f"Created {len(chunks)} chunks."
    )

    # Create embeddings
    print("\nCreating embeddings...")

    embeddings = create_embeddings(chunks)

    print(
        f"Embedding dimension: {embeddings.shape[1]}"
    )

    # Create FAISS
    index = create_vector_database(
        embeddings
    )

    print(
        f"FAISS index contains "
        f"{index.ntotal} vectors."
    )

    # Conversation history
    history = []

    print("\nRAG system ready!")

    print(
        "\nType 'exit' to stop."
    )

    # Chat loop
    while True:

        question = input(
            "\nYou: "
        ).strip()

        if question.lower() == "exit":
            break

        if not question:
            continue

        # Retrieve
        results = retrieve(
            question,
            index,
            chunks
        )

        if not results:

            print(
                "\nNo relevant information found."
            )

            continue

        # Context
        context = build_context(
            results
        )

        # Generate
        try:

            answer = generate_answer(
                question,
                context,
                history
            )

            print(
                f"\nAssistant:\n{answer}"
            )

            display_sources(
                results
            )

            # Save conversation
            history.append({
                "role": "user",
                "content": question
            })

            history.append({
                "role": "assistant",
                "content": answer
            })

            # Prevent history from becoming huge
            if len(history) > 10:

                history = history[-10:]

        except Exception as error:

            print(
                f"\nError: {error}"
            )


if __name__ == "__main__":
    main()