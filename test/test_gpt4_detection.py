#!/usr/bin/env python3
"""
Test GPT-4 Language Detection
Demonstrates: GPT-4 based language detection from various user inputs
"""

import os
import sys
from dotenv import load_dotenv
from langgraph_pipeline import LangGraphVoicePipeline

def test_gpt4_language_detection():
    """Test GPT-4 language detection with various inputs"""
    print("🤖 Testing GPT-4 Language Detection")
    print("=" * 50)
    
    # Load environment variables
    load_dotenv()
    
    if not os.getenv("OPENAI_API_KEY"):
        print("ERROR: OPENAI_API_KEY not found in environment variables.")
        return
    
    # Create pipeline instance
    pipeline = LangGraphVoicePipeline()
    
    # Test cases for language detection
    test_cases = [
        "I want to use C plus plus",
        "C++ please",
        "cpp",
        "I'd like to use Java",
        "Python would be good",
        "JavaScript is fine",
        "I want to use C sharp",
        "Go language",
        "Rust programming",
        "I don't know, maybe Python?",
        "Something modern like TypeScript",
        "Just use whatever you think is best"
    ]
    
    print("📝 Testing GPT-4 language detection:")
    print()
    
    for i, user_input in enumerate(test_cases, 1):
        try:
            detected = pipeline._extract_language_from_response(user_input)
            print(f"{i:2d}. Input: '{user_input}'")
            print(f"    Detected: '{detected}'")
            print()
        except Exception as e:
            print(f"{i:2d}. Input: '{user_input}'")
            print(f"    Error: {e}")
            print()
    
    print("✅ GPT-4 language detection test completed!")

if __name__ == "__main__":
    test_gpt4_language_detection()
