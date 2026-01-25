import os
import re
import argparse
from encryption_utils import EncryptionModule
from url_classifier import URLClassifier
from text_classifier import TextClassifier
from ocr_utils import OCRUtils

class PhishingDetectionSystem:
    def __init__(self):
        self.encryption = EncryptionModule()
        self.url_classifier = URLClassifier()
        self.text_classifier = TextClassifier()
        self.ocr = OCRUtils()
        
        # Training data paths
        self.url_data = "malicious_phish.csv"
        self.email_data = "phishing_email.csv"

    def initialize_models(self):
        """
        Train models if data exists.
        """
        print("[SYSTEM] Initializing models...")
        self.url_classifier.train(self.url_data)
        self.text_classifier.train(self.email_data)
        print("[SYSTEM] Initialization complete.")

    def detect_input_type(self, decrypted_input):
        """
        Dynamic input type detection.
        """
        # Check if it's a file path to an image
        if os.path.exists(decrypted_input) and self.ocr.is_image(decrypted_input):
            return 'IMAGE'
        
        # Check if URL (simple regex)
        if re.match(r"https?://", decrypted_input) or re.match(r"www\.", decrypted_input):
            return 'URL'
        
        # Default to text
        return 'TEXT'

    def process_input(self, input_data):
        """
        Main processing logic: Decrypt -> Identify -> Predict
        """
        # 1. Decrypt
        decrypted = self.encryption.try_decrypt(input_data)
        
        # 2. Identify Type
        input_type = self.detect_input_type(decrypted)
        
        score = 0
        details = ""

        # 3. Dispatch
        if input_type == 'URL':
            val = self.url_classifier.predict(decrypted)
            score = val
            details = f"URL Probability: {val:.4f}"
        
        elif input_type == 'IMAGE':
            text = self.ocr.extract_text(decrypted)
            if not text.strip():
                details = "OCR extracted empty text."
                score = 0
            else:
                val = self.text_classifier.predict(text)
                score = val
                details = f"Image Text Probability: {val:.4f} (Extracted: {text[:30]}...)"
        
        elif input_type == 'TEXT':
            val = self.text_classifier.predict(decrypted)
            score = val
            details = f"Text Probability: {val:.4f}"

        verdict = "PHISHING" if score >= 0.5 else "LEGITIMATE"
        
        return {
            "input": decrypted[:50] + "..." if len(decrypted) > 50 else decrypted,
            "type": input_type,
            "score": score,
            "verdict": verdict,
            "details": details
        }

    def run_demo(self):
        """
        Runs a demonstration with sample encrypted inputs.
        """
        print("\n[DEMO] Running Phishing Detection Demo with Mixed Inputs")
        
        # Sample inputs
        inputs = [
            "http://secure-bank-verify.com/login", # Phishing URL
            "https://google.com",                  # Legit URL
            "URGENT: Verify your account immediately", # Phishing Text
            "Meeting notes attached for review",       # Legit Text
            # "sample_image.png" # Uncomment if image exists
        ]
        
        # Encrypt inputs to simulate secure ingestion
        encrypted_inputs = [self.encryption.encrypt(i) for i in inputs]
        
        # Add a plaintext input to test fallback
        encrypted_inputs.append("http://plaintext-phish.com/login")

        results = []
        for enc_data in encrypted_inputs:
            res = self.process_input(enc_data)
            results.append(res)
            
        # Aggregation (Average score just for demonstration)
        avg_score = sum(r['score'] for r in results) / len(results) if results else 0
        final_verdict = "PHISHING" if avg_score >= 0.5 else "LEGITIMATE"

        print("\n" + "="*50)
        print(f"Final Aggregated Verdict: {final_verdict} (Avg Score: {avg_score:.4f})")
        print("="*50)
        for i, r in enumerate(results):
            print(f"Input {i+1} [{r['type']}]: {r['verdict']} (Score: {r['score']:.4f})")
            print(f"  > Content: {r['input']}")
            print(f"  > Details: {r['details']}")
        print("="*50 + "\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Multi-Modal Phishing Detection System")
    parser.add_argument('--train', action='store_true', help="Train models")
    parser.add_argument('--demo', action='store_true', help="Run demo")
    
    args = parser.parse_args()
    
    system = PhishingDetectionSystem()
    
    # Always train for now since we don't save/load models persistently in this simple script
    system.initialize_models()
    
    if args.demo:
        system.run_demo()
    else:
        # Interactive mode
        print("Enter input (URL, Text, or Image Path). Type 'exit' to quit.")
        while True:
            user_in = input("Input> ")
            if user_in.lower() == 'exit':
                break
            
            # Simulate encryption
            enc_in = system.encryption.encrypt(user_in)
            
            result = system.process_input(enc_in)
            print(f"Verdict: {result['verdict']} (Score: {result['score']:.4f})")
