from openai import OpenAI
from sentence_transformers import SentenceTransformer
import faiss

# OpenAI client
client = OpenAI(api_key="YOUR_API_KEY")

# 1. Knowledge base
documents = [
    "AWS is a cloud computing platform provided by Amazon.",
    "Amazon EC2 provides virtual servers in the cloud.",
    "Amazon S3 is used for storing files and objects.",
    "Azure is Microsoft's cloud computing platform.",
    "Python is widely used for artificial intelligence and data science."
]

# 2. Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# 3. Convert documents into embeddings
embeddings = model.encode(documents)

# 4. Create FAISS vector index
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)

index.add(embeddings)

# 5. User question
question = "What is AWS?"

# 6. Convert question into embedding
question_embedding = model.encode([question])

# 7. Search for most relevant document
distances, indices = index.search(question_embedding, k=2)

# 8. Retrieve documents
context = ""

for i in indices[0]:
    context += documents[i] + "\n"

print("Retrieved Information:")
print(context)

# 9. Send context + question to LLM
prompt = f"""
Answer the question using the retrieved information.

Retrieved Information:
{context}

Question:
{question}

Answer:
"""

response = client.responses.create(
    model="gpt-4.1-mini",
    input=prompt
)

# 10. Display answer
print("\nAnswer:")
print(response.output_text)