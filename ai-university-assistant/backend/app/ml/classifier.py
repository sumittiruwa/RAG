import os
import pickle
import numpy as np
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer
from typing import List, Tuple

class IntentClassifier:
    """Classify student questions into intents"""
    
    INTENTS = ["Attendance", "Examination", "Course", "Admission", "Fee", "Other"]
    
    def __init__(self, model_path: str = "ml_dataset/classifier.pkl",
                 vectorizer_path: str = "ml_dataset/vectorizer.pkl"):
        self.model_path = model_path
        self.vectorizer_path = vectorizer_path
        self.vectorizer = None
        self.model = None
        
        # Try to load existing model
        self.load()
    
    def train(self, texts: List[str], labels: List[int]) -> None:
        """Train the classifier"""
        self.vectorizer = TfidfVectorizer(max_features=100)
        X = self.vectorizer.fit_transform(texts)
        
        self.model = MultinomialNB()
        self.model.fit(X, labels)
        
        self.save()
    
    def predict(self, text: str) -> Tuple[str, float]:
        """Predict intent for text"""
        if self.model is None or self.vectorizer is None:
            return "Other", 0.0
        
        try:
            X = self.vectorizer.transform([text])
            probabilities = self.model.predict_proba(X)[0]
            intent_idx = np.argmax(probabilities)
            confidence = probabilities[intent_idx]
            
            return self.INTENTS[intent_idx], float(confidence)
        
        except Exception as e:
            print(f"Error in classification: {e}")
            return "Other", 0.0
    
    def save(self) -> None:
        """Save model and vectorizer"""
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        
        with open(self.model_path, 'wb') as f:
            pickle.dump(self.model, f)
        
        with open(self.vectorizer_path, 'wb') as f:
            pickle.dump(self.vectorizer, f)
    
    def load(self) -> None:
        """Load existing model"""
        if os.path.exists(self.model_path) and os.path.exists(self.vectorizer_path):
            try:
                with open(self.model_path, 'rb') as f:
                    self.model = pickle.load(f)
                
                with open(self.vectorizer_path, 'rb') as f:
                    self.vectorizer = pickle.load(f)
            except:
                pass
