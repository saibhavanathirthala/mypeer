#!/usr/bin/env python3
"""
Test Response Matching
Demonstrates: Better response matching for user questions and requests
"""

import os
import sys
from dotenv import load_dotenv
from langgraph_pipeline import LangGraphVoicePipeline

def main():
    """Test response matching improvements"""
    print("🤖 Response Matching Test")
    print("🎯 Testing: Better response matching for user questions")
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
        print("🚀 Initializing Response Matching Pipeline...")
        pipeline = LangGraphVoicePipeline()

        print("✅ Response Matching Pipeline initialized successfully!")
        print()
        print("🔧 RESPONSE MATCHING IMPROVEMENTS:")
        print("   • Better detection of language support questions")
        print("   • Appropriate responses for 'What other languages do you support?'")
        print("   • Helpful language lists when users ask about options")
        print("   • Better context-aware responses")
        print()
        print("💡 TESTING INSTRUCTIONS:")
        print("   1. Say 'Blueberry' to start")
        print("   2. Say 'Write a function to print hello world'")
        print("   3. When asked for language, say 'No, I don't want Python. What other languages do you support?'")
        print("   4. System should respond with language list instead of generic help")
        print()
        print("🎯 EXPECTED FLOW:")
        print("   Blueberry → Voice Input → STT → Confirmation → Intent Classification")
        print("   → Language Selection → User asks about languages → System provides language list")
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
