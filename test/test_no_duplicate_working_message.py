#!/usr/bin/env python3
"""
Test No Duplicate Working Message
Demonstrates: System should not speak the same working message twice
"""

import os
import sys
from dotenv import load_dotenv
from langgraph_pipeline import LangGraphVoicePipeline

def main():
    """Test no duplicate working message"""
    print("🤖 No Duplicate Working Message Test")
    print("🎯 Testing: System should not speak the same working message twice")
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
        print("🚀 Initializing No Duplicate Working Message Pipeline...")
        pipeline = LangGraphVoicePipeline()

        print("✅ No Duplicate Working Message Pipeline initialized successfully!")
        print()
        print("🔧 DUPLICATE WORKING MESSAGE FIXES:")
        print("   • Removed duplicate print statement")
        print("   • Single TTS call per working message")
        print("   • Clean console output")
        print("   • No repeated 'I'm working on...' messages")
        print()
        print("💡 TESTING INSTRUCTIONS:")
        print("   1. Say 'Blueberry' to start")
        print("   2. Say 'Write a function to print hello world'")
        print("   3. System should speak 'I'm working on...' message only once")
        print("   4. No duplicate TTS output")
        print()
        print("🎯 EXPECTED BEHAVIOR:")
        print("   • Each working message spoken only once")
        print("   • Clean console output")
        print("   • No repeated 'I'm working on...' messages")
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
