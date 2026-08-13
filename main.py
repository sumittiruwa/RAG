from groq import Groq
from sentence_transformers import SentenceTransformer
from pypdf import PdfReader
from dotenv import load_dotenv
import faiss
import numpy as np
import os


# ==========================================
# 1. Load API key
# ==========================================

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


# ==========================================
# 2. Read PDF
# ==========================================

reader = PdfReader("document.pdf")

text = ""

for page in reader.pages:
    text += page.extract_text() + "\n"

print("PDF loaded successfully!")


# ==========================================
# 3. Split text into chunks
# ==========================================

chunk_size = 500

chunks = [
    text[i:i + chunk_size]
    for i in range(0, len(text), chunk_size)
]

print("Number of chunks:", len(chunks))


# ==========================================
# 4. Create embeddings
# ==========================================

model = SentenceTransformer("all-MiniLM-L6-v2")

embeddings = model.encode(chunks)

embeddings = np.array(embeddings).astype("float32")

print("Embeddings created!")


# ==========================================
# 5. Create FAISS vector database
# ==========================================

dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)

index.add(embeddings)

print("FAISS database created!")


# ==========================================
# 6. Ask user a question
# ==========================================

question = input("\nAsk a question about the PDF: ")


# ==========================================
# 7. Convert question into embedding
# ==========================================

question_embedding = model.encode([question])

question_embedding = np.array(
    question_embedding
).astype("float32")


# ==========================================
# 8. Search for relevant chunks
# ==========================================

k = 3

distances, indices = index.search(
    question_embedding,
    k
)

retrieved_chunks = [
    chunks[i]
    for i in indices[0]
]


# ==========================================
# 9. Create context
# ==========================================

context = "\n\n".join(retrieved_chunks)


# ==========================================
# 10. Send context + question to Groq
# ==========================================

prompt = f"""
Answer the question using only the context below.

Context:
{context}

Question:
{question}

If the answer is not present in the context,
say "I don't know based on the provided document."
"""


response = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ],
    temperature=0
)


# ==========================================
# 11. Display answer
# ==========================================

answer = response.choices[0].message.content

print("\nAnswer:")
print(answer)