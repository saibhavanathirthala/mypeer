#!/usr/bin/env python3
"""
Test Continuous Loop
Demonstrates: Continuous session with wake-up word detection loop
"""

import os
import sys
from dotenv import load_dotenv
from langgraph_pipeline import LangGraphVoicePipeline

def main():
    """Test continuous loop functionality"""
    print("🤖 Continuous Loop Test")
    print("🎯 Testing: Continuous session with wake-up word detection")
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
        print("🚀 Initializing Continuous Loop Pipeline...")
        pipeline = LangGraphVoicePipeline()

        print("✅ Continuous Loop Pipeline initialized successfully!")
        print()
        print("🔄 CONTINUOUS LOOP FEATURES:")
        print("   • Infinite loop for continuous interaction")
        print("   • Wake-up word detection for each new session")
        print("   • 10-second max recording with 1.5-second silence detection")
        print("   • After task completion: asks if user needs more help")
        print("   • If 'no': goes back to wake-up word detection")
        print("   • If 'yes': starts new task from intent classification")
        print("   • No session ending - continuous operation")
        print()
        print("💡 TESTING INSTRUCTIONS:")
        print("   1. Say 'Blueberry' to start first session")
        print("   2. Complete a task (e.g., 'Write a function to print hello world')")
        print("   3. When asked 'Is there anything else I can help you with?':")
        print("      - Say 'no' → System goes back to wake-up word detection")
        print("      - Say 'yes' → System starts new task")
        print("   4. Repeat the cycle indefinitely")
        print()
        print("🎯 EXPECTED FLOW:")
        print("   Blueberry → Task → Completion → 'More help?' → 'no' → Blueberry (repeat)")
        print("   Blueberry → Task → Completion → 'More help?' → 'yes' → New Task")
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
