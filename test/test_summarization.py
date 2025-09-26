#!/usr/bin/env python3
"""
Test Summarization Function
Demonstrates: Better understanding of user requests
"""

from langgraph_pipeline import LangGraphVoicePipeline

def test_summarization():
    """Test the summarization function"""
    print("🤖 Testing Summarization Function")
    print("=" * 50)
    
    # Create pipeline instance
    pipeline = LangGraphVoicePipeline()
    
    # Test cases
    test_cases = [
        "Print, write a function to print hello world",
        "write a function to print hello world",
        "create a function to print hello world",
        "write a python function to print hello world",
        "create a hello world function",
        "write a function that prints something",
        "create a class for user management",
        "build an API for user authentication",
        "make a simple calculator function"
    ]
    
    print("📝 Testing summarization for various requests:")
    print()
    
    for i, request in enumerate(test_cases, 1):
        summary = pipeline._summarize_user_request(request)
        print(f"{i:2d}. Input:  '{request}'")
        print(f"    Output: '{summary}'")
        print()
    
    print("✅ Summarization test completed!")

if __name__ == "__main__":
    test_summarization()
