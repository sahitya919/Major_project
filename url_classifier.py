import pandas as pd
import numpy as np
import re
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import os
import joblib

class URLClassifier:
    def __init__(self):
        self.model = None
    
    def extract_features(self, url):
        """
        Extracts lexical and structural features from the URL.
        """
        features = {
            'url_length': len(url),
            'num_dots': url.count('.'),
            'count_at': url.count('@'),
            'count_dash': url.count('-'),
            'count_digits': sum(c.isdigit() for c in url),
            'count_slash': url.count('/'),
            'has_ip': 1 if re.match(r"https?://(?:\d{1,3}\.){3}\d{1,3}(?:[:/]|$)", url) else 0
        }
        match = re.match(r"https?://([^/]+)", url)
        features['hostname_length'] = len(match.group(1)) if match else 0
        return pd.Series(features)

    def train(self, csv_path):
        """
        Trains the Random Forest model on the provided CSV.
        """
        if not os.path.exists(csv_path):
            print(f"[ERROR] Dataset {csv_path} not found.")
            return

        print(f"[INFO] Training URL Classifier on {csv_path}...")
        try:
            url_df = pd.read_csv(csv_path)
            # Basic validation of columns
            if 'url' not in url_df.columns or 'type' not in url_df.columns:
                 print("[ERROR] CSV must contain 'url' and 'type' columns.")
                 return

            url_df['label'] = url_df['type'].apply(lambda x: 1 if x == 'phishing' else 0)
            
            # Feature extraction
            url_features = url_df['url'].apply(self.extract_features)
            X = url_features
            y = url_df['label']

            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            
            self.model = RandomForestClassifier(n_estimators=100, random_state=42)
            self.model.fit(X_train, y_train)
            
            # Evaluate
            score = self.model.score(X_test, y_test)
            print(f"[INFO] URL Classifier trained. Accuracy: {score:.4f}")
            
        except Exception as e:
            print(f"[ERROR] Training failed: {e}")

    def predict(self, url):
        """
        Predicts if a URL is phishing (1) or benign (0).
        """
        if not self.model:
            print("[WARNING] URL Model not trained.")
            return 0
        
        features = self.extract_features(url).values.reshape(1, -1)
        prob = self.model.predict_proba(features)[0][1]
        return prob
