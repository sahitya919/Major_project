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
            'has_ip': 1 if re.match(r"https?://(?:\d{1,3}\.){3}\d{1,3}(?:[:/]|$)", url) else 0,
            'has_login': 1 if 'login' in url.lower() else 0,
            'has_verify': 1 if 'verify' in url.lower() else 0,
            'has_account': 1 if 'account' in url.lower() else 0,
            'has_secure': 1 if 'secure' in url.lower() else 0
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
            target_col = None
            if 'URL' in url_df.columns and 'label' in url_df.columns:
                 # PhiUSIIL dataset: 0=Phishing, 1=Legitimate
                 # We want 1=Phishing, 0=Legitimate
                 url_df['label'] = url_df['label'].apply(lambda x: 1 if x == 0 else 0)
                 target_col = 'URL'
            elif 'url' in url_df.columns and 'type' in url_df.columns:
                 # Old dataset
                 url_df['label'] = url_df['type'].apply(lambda x: 0 if x == 'benign' else 1)
                 target_col = 'url'
            else:
                 print("[ERROR] CSV must contain ('URL', 'label') or ('url', 'type') columns.")
                 return
            
            # Feature extraction
            url_features = url_df[target_col].apply(self.extract_features)
            X = url_features
            y = url_df['label']

            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            
            self.model = RandomForestClassifier(n_estimators=100, random_state=42)
            print(f"[INFO] Model initialized. Fitting on {len(X_train)} samples...")
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
        
        features_series = self.extract_features(url)
        features_df = pd.DataFrame([features_series])
        prob = self.model.predict_proba(features_df)[0][1]
        return prob
