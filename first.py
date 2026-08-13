from groq import Groq
from sentence_transformers import SentenceTransformer
import faiss
from pypdf import PdfReader
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import cosine_similarity

print("All libraries imported successfully!")