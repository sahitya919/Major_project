import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
import os

class TextClassifier:
    def __init__(self):
        self.model = None

    def train(self, csv_path):
        """
        Trains the Naive Bayes model on the provided CSV.
        """
        if not os.path.exists(csv_path):
            print(f"[ERROR] Dataset {csv_path} not found.")
            return

        print(f"[INFO] Training Text Classifier on {csv_path}...")
        try:
            email_df = pd.read_csv(csv_path)
            # Basic validation
            if 'text_combined' not in email_df.columns or 'label' not in email_df.columns:
                print("[ERROR] CSV must contain 'text_combined' and 'label' columns.")
                return

            email_df = email_df.dropna(subset=['text_combined', 'label'])
            
            X = email_df['text_combined']
            y = email_df['label']

            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            
            self.model = make_pipeline(TfidfVectorizer(), MultinomialNB())
            self.model.fit(X_train, y_train)
            
            score = self.model.score(X_test, y_test)
            print(f"[INFO] Text Classifier trained. Accuracy: {score:.4f}")

        except Exception as e:
            print(f"[ERROR] Training failed: {e}")

    def predict(self, text):
        """
        Predicts if text is phishing (1) or benign (0).
        """
        if not self.model:
             print("[WARNING] Text Model not trained.")
             return 0
        
        # Pipeline handles vectorization
        prob = self.model.predict_proba([text])[0][1]
        return prob
