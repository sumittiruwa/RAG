from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

documents = [
    "Cloud computing provides computing resources over the internet.",
    "AWS is a cloud platform provided by Amazon.",
    "Azure is Microsoft's cloud computing platform.",
    "Python is a programming language used in AI and data science."
]

question = "What is AWS?"

# Convert documents to vectors
vectorizer = TfidfVectorizer()
vectors = vectorizer.fit_transform(documents)

# Convert question to vector
question_vector = vectorizer.transform([question])

# Calculate similarity
similarities = cosine_similarity(question_vector, vectors)[0]

# Get best document
best_index = similarities.argmax()
best_document = documents[best_index]

print("Retrieved Document:")
print(best_document)