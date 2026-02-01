
import re
import os
from main import PhishingDetectionSystem

def test_inputs():
    system = PhishingDetectionSystem()
    
    inputs = [
        "http://google.com",
        "https://google.com",
        "www.google.com",
        "google.com",
        "youtube.com",
        "subdomain.example.com",
        "random text here"
    ]
    
    print("--- Input Detection Test ---")
    for i in inputs:
        # Simulate clean_input logic from main.py (we can't call detect_input_type directly easily without mocking encryption, 
        # but wait, detect_input_type is a method we can call if we pass a string. 
        # decryption happens before. Let's assume passed string IS decrypted)
        
        # We need to replicate the stripping logic from main.py before calling detect_input_type? 
        # No, detect_input_type in my recent edit takes 'decrypted_input' and strips it inside.
        
        # However, to call it, I need an instance.
        # But 'decrypted_input' in 'detect_input_type' does:
        # clean_input = decrypted_input.strip('"\'')
        # if re.match(r"https?://", clean_input) or re.match(r"www\.", clean_input): ...
        
        # Let's inspect what detect_input_type returns.
        
        detected_type = system.detect_input_type(i)
        print(f"'{i}' -> {detected_type}")

if __name__ == "__main__":
    test_inputs()
