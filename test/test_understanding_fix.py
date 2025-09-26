#!/usr/bin/env python3
"""
Test Understanding Fix
Demonstrates: Better understanding of user requests with proper summarization
"""

import os
import sys
from dotenv import load_dotenv
from langgraph_pipeline import LangGraphVoicePipeline

def main():
    """Test the understanding fix"""
    print("🤖 Understanding Fix Test")
    print("🎯 Testing: Better understanding of user requests")
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
        print("🚀 Initializing Understanding Fix Pipeline...")
        pipeline = LangGraphVoicePipeline()

        print("✅ Understanding Fix Pipeline initialized successfully!")
        print()
        print("🔧 UNDERSTANDING FIXES:")
        print("   • Better pattern matching for 'write function to print hello world'")
        print("   • Improved summarization that keeps context")
        print("   • More accurate confirmation messages")
        print()
        print("💡 TESTING INSTRUCTIONS:")
        print("   1. Say 'Blueberry' to start")
        print("   2. Say 'Print, write a function to print hello world'")
        print("   3. The system should now understand: 'write a function to print hello world'")
        print("   4. When asked for confirmation, say 'yes' clearly")
        print()
        print("🎯 EXPECTED FLOW:")
        print("   Blueberry → Voice Input → STT → Better Confirmation → Intent Classification")
        print("   (Should understand the full request, not just 'write a function')")
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
