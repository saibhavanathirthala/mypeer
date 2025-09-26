#!/usr/bin/env python3
"""
Test Session End and Restart
Demonstrates: Session ends when user says "I don't want any help" and restarts at wake-up word detection
"""

import os
import sys
from dotenv import load_dotenv
from langgraph_pipeline import LangGraphVoicePipeline

def main():
    """Test session end and restart functionality"""
    print("🤖 Session End and Restart Test")
    print("🎯 Testing: Session ends when user says 'I don't want any help' and restarts at wake-up word detection")
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
        print("🚀 Initializing Session End and Restart Pipeline...")
        pipeline = LangGraphVoicePipeline()

        print("✅ Session End and Restart Pipeline initialized successfully!")
        print()
        print("🔄 SESSION END AND RESTART FEATURES:")
        print("   • When user says 'I don't want any help' → Session ends")
        print("   • After session ends → Goes back to wake-up word detection")
        print("   • System waits for 'Blueberry' to start new session")
        print("   • Continuous loop: End → Wait for Blueberry → New session")
        print()
        print("💡 TESTING INSTRUCTIONS:")
        print("   1. Say 'Blueberry' to start first session")
        print("   2. Complete a task (e.g., 'Write a function to print hello world')")
        print("   3. When asked 'Is there anything else I can help you with?':")
        print("      - Say 'I don't want any help' → Session ends")
        print("      - System goes back to wake-up word detection")
        print("   4. Say 'Blueberry' again to start new session")
        print("   5. Repeat the cycle")
        print()
        print("🎯 EXPECTED FLOW:")
        print("   Blueberry → Task → Completion → 'More help?' → 'I don't want any help' → Session ends")
        print("   → Wait for Blueberry → Blueberry → New Task")
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
