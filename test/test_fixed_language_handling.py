#!/usr/bin/env python3
"""
Test Fixed Language Handling
Demonstrates: Proper language detection, file extension handling, and user feedback processing
"""

import os
import sys
from dotenv import load_dotenv
from langgraph_pipeline import LangGraphVoicePipeline

def main():
    """Test the fixed language handling"""
    print("🤖 Fixed Language Handling Test")
    print("🎯 Features: Proper language detection + Correct file extensions + User feedback processing + Smart filename generation")
    print("=" * 100)

    # Load environment variables
    load_dotenv()

    # Verify OpenAI API key
    if not os.getenv("OPENAI_API_KEY"):
        print("ERROR: OPENAI_API_KEY not found in environment variables.")
        print("Please set your OpenAI API key in a .env file or environment variable.")
        sys.exit(1)

    try:
        # Initialize LangGraph pipeline
        print("🚀 Initializing Fixed Language Handling Pipeline...")
        pipeline = LangGraphVoicePipeline()

        print("✅ Fixed Language Handling Pipeline initialized successfully!")
        print()
        print("🔧 FIXED LANGUAGE HANDLING FEATURES:")
        print("   • Proper language detection from user feedback")
        print("   • Correct file extension generation")
        print("   • Smart filename generation based on language")
        print("   • Real-time language switching")
        print("   • User feedback processing")
        print()
        print("💻 LANGUAGE DETECTION EXAMPLES:")
        print("   User: 'I want a Java function' → Detects: Java → Creates: .java file")
        print("   User: 'Create a JavaScript API' → Detects: JavaScript → Creates: .js file")
        print("   User: 'Write a Python script' → Detects: Python → Creates: .py file")
        print("   User: 'Build a C++ program' → Detects: C++ → Creates: .cpp file")
        print("   User: 'Make a Go service' → Detects: Go → Creates: .go file")
        print()
        print("📁 SMART FILENAME EXAMPLES:")
        print("   Java function → hello_world.java")
        print("   JavaScript API → api_server.js")
        print("   Python script → main_function.py")
        print("   C++ program → main.cpp")
        print("   Go service → main.go")
        print()
        print("🔄 USER FEEDBACK PROCESSING:")
        print("   User: 'I want something else'")
        print("   System: 'What would you like me to change?'")
        print("   User: 'Create a Java function instead'")
        print("   System: 'Got it! I'll work on Create a Java function using Java. Let's continue.'")
        print("   Result: Creates hello_world.java (not .py file)")
        print()
        print("🎯 INTERACTIVE FLOW:")
        print("   1. User makes request")
        print("   2. System detects language")
        print("   3. User says 'I want something else'")
        print("   4. System asks what to change")
        print("   5. User specifies new language")
        print("   6. System re-analyzes language")
        print("   7. System creates correct file type")
        print()

        # Start the continuous voice session
        pipeline.start_continuous_session()

    except KeyboardInterrupt:
        print("\n\n👋 Session ended by user. Goodbye!")
    except Exception as e:
        print(f"\n❌ Fatal error: {str(e)}")
        print("Please check your configuration and try again.")
        sys.exit(1)


if __name__ == "__main__":
    main()
