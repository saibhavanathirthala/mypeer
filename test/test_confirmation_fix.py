#!/usr/bin/env python3
"""
Test Confirmation Fix
Demonstrates: Proper confirmation handling with better timeout and fallback
"""

import os
import sys
from dotenv import load_dotenv
from langgraph_pipeline import LangGraphVoicePipeline

def main():
    """Test the confirmation fix"""
    print("🤖 Confirmation Fix Test")
    print("🎯 Testing: Better timeout and fallback for confirmation")
    print("=" * 80)

    # Load environment variables
    load_dotenv()

    # Verify OpenAI API key
    if not os.getenv("OPENAI_API_KEY"):
        print("ERROR: OPENAI_API_KEY not found in environment variables.")
        print("Please set your OpenAI API key in a .env file or environment variable.")
        sys.exit(1)

    try:
        # Initialize LangGraph pipeline
        print("🚀 Initializing Confirmation Fix Pipeline...")
        pipeline = LangGraphVoicePipeline()

        print("✅ Confirmation Fix Pipeline initialized successfully!")
        print()
        print("🔧 CONFIRMATION FIXES:")
        print("   • Increased timeout from 5 to 10 seconds")
        print("   • Better speech detection")
        print("   • Fallback handling for no response")
        print()
        print("💡 TESTING INSTRUCTIONS:")
        print("   1. Say 'Blueberry' to start")
        print("   2. Say 'create a python function to print hello world'")
        print("   3. When asked for confirmation, say 'yes' clearly")
        print("   4. The system should proceed to intent classification")
        print()
        print("🎯 EXPECTED FLOW:")
        print("   Blueberry → Voice Input → STT → Confirmation → Intent Classification")
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
