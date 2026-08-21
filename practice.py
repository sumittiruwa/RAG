from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.documents import Document


import os
# os.environ["OPENAI_API_KEY"] = "your-api-key"

# Step 1: Create documents
docs = [
    Document(page_content="Python is a programming language."),
    Document(page_content="RAG stands for Retrieval-Augmented Generation."),
    Document(page_content="FAISS is a vector database for similarity search.")
]

# Step 2: Create embeddings and vector store
embeddings = OpenAIEmbeddings()
vectorstore = FAISS.from_documents(docs, embeddings)

# Step 3: Retrieve relevant documents
query = "What is RAG?"
retrieved_docs = vectorstore.similarity_search(query, k=2)

# Step 4: Create context
context = "\n".join(doc.page_content for doc in retrieved_docs)

# Step 5: Ask the LLM
llm = ChatOpenAI(model="gpt-4.1-mini")

prompt = f"""
Answer the question using the context below.

Context:
{context}

Question:
{query}
"""

response = llm.invoke(prompt)

print(response.content)