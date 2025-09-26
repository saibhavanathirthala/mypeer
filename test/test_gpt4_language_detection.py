#!/usr/bin/env python3
"""
Test GPT-4 Language Detection and Improved TTS
Demonstrates: GPT-4 based language detection and natural TTS with filler sounds
"""

import os
import sys
from dotenv import load_dotenv
from langgraph_pipeline import LangGraphVoicePipeline

def main():
    """Test GPT-4 language detection and improved TTS"""
    print("🤖 GPT-4 Language Detection and Improved TTS Test")
    print("🎯 Testing: GPT-4 language detection and natural TTS with filler sounds")
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
        print("🚀 Initializing GPT-4 Language Detection Pipeline...")
        pipeline = LangGraphVoicePipeline()

        print("✅ GPT-4 Language Detection Pipeline initialized successfully!")
        print()
        print("🔧 GPT-4 LANGUAGE DETECTION FEATURES:")
        print("   • GPT-4 based language detection instead of hardcoded rules")
        print("   • Natural TTS with filler sounds (um, hmm, etc.)")
        print("   • Better summarization of user requests")
        print("   • More human-like conversation flow")
        print()
        print("💡 TESTING INSTRUCTIONS:")
        print("   1. Say 'Blueberry' to start")
        print("   2. Say 'Write a function to print hello world'")
        print("   3. When asked for language, say something like 'I want to use C plus plus'")
        print("   4. GPT-4 should detect 'c++' from your response")
        print("   5. Notice the natural TTS with filler sounds")
        print()
        print("🎯 EXPECTED FLOW:")
        print("   Blueberry → Voice Input → STT → Natural Confirmation → GPT-4 Language Detection")
        print("   → Natural TTS with filler sounds → Code Generation")
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
