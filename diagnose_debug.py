
import pandas as pd
import numpy as np
from url_classifier import URLClassifier
import os

def diagnose():
    print("--- DIAGNOSTIC START ---")
    
    # 1. Check File Size and Head
    if not os.path.exists("malicious_phish.csv"):
        print("ERROR: malicious_phish.csv not found!")
        return

    print("Reading CSV...")
    try:
        df = pd.read_csv("malicious_phish.csv")
        print(f"Dataset Shape: {df.shape}")
        print("Class Distribution:")
        print(df['type'].value_counts())
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return

    # 2. Test Feature Extraction
    clf = URLClassifier()
    test_urls = ["http://google.com", "http://facebook.com", "http://secure-login.com"]
    print("\nFeature Extraction Test:")
    for url in test_urls:
        feats = clf.extract_features(url)
        print(f"URL: {url}")
        print(feats)
    
    # 3. Train on a subset (to be fast) and check importance
    print("\nTraining on subset (first 1000 rows)...")
    try:
        # Hack to train on small subset for diagnosis
        small_csv = "temp_diag.csv"
        df.head(1000).to_csv(small_csv, index=False)
        
        clf.train(small_csv)
        
        # Check feature importances
        if hasattr(clf.model, 'feature_importances_'):
            print("\nFeature Importances:")
            feats = ['url_length', 'num_dots', 'count_at', 'count_dash', 'count_digits', 'count_slash', 'has_ip', 'has_login', 'has_verify', 'has_account', 'has_secure', 'hostname_length']
            # Note: The order must match extract_features. 
            # In extract_features, we return a Series. Dict order in Python 3.7+ is insertion order.
            # Let's trust the order for now or just print raw.
            print(clf.model.feature_importances_)
            
        # 4. Predict
        print("\nPredictions:")
        for url in test_urls:
            prob = clf.predict(url)
            print(f"{url} -> Prob: {prob:.4f} ({'PHISHING' if prob >= 0.5 else 'LEGITIMATE'})")
            
        os.remove(small_csv)
            
    except Exception as e:
        print(f"Error during training/testing: {e}")

if __name__ == "__main__":
    diagnose()
