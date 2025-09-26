#!/usr/bin/env python3
"""
Test Simple Confirmation
Demonstrates: Simple confirmation without duplicate TTS calls
"""

import os
import sys
from dotenv import load_dotenv
from langgraph_pipeline import LangGraphVoicePipeline

def main():
    """Test simple confirmation"""
    print("🤖 Simple Confirmation Test")
    print("🎯 Testing: No duplicate TTS calls, better confirmation handling")
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
        print("🚀 Initializing Simple Confirmation Pipeline...")
        pipeline = LangGraphVoicePipeline()

        print("✅ Simple Confirmation Pipeline initialized successfully!")
        print()
        print("🔧 CONFIRMATION FIXES:")
        print("   • Removed duplicate TTS calls")
        print("   • Increased timeout to 15 seconds")
        print("   • Added clear instructions for user")
        print("   • Simplified fallback logic")
        print()
        print("💡 TESTING INSTRUCTIONS:")
        print("   1. Say 'Blueberry' to start")
        print("   2. Say 'create a python function to print hello world'")
        print("   3. When asked for confirmation, say 'yes' clearly")
        print("   4. The system should proceed without duplicate voices")
        print()
        print("🎯 EXPECTED FLOW:")
        print("   Blueberry → Voice Input → STT → Confirmation → Intent Classification")
        print("   (No duplicate TTS calls)")
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
