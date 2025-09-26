#!/usr/bin/env python3
"""
Test Continuous Help Loop
Demonstrates: Continuous help after task completion + New task initiation + Session management
"""

import os
import sys
from dotenv import load_dotenv
from langgraph_pipeline import LangGraphVoicePipeline

def main():
    """Test the continuous help loop feature"""
    print("🤖 Continuous Help Loop Test")
    print("🎯 Features: Continuous help after task completion + New task initiation + Session management + Blueberry wake-up")
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
        print("🚀 Initializing Continuous Help Loop Pipeline...")
        pipeline = LangGraphVoicePipeline()

        print("✅ Continuous Help Loop Pipeline initialized successfully!")
        print()
        print("🔄 CONTINUOUS HELP LOOP FEATURES:")
        print("   • After completing all todos, asks if user needs more help")
        print("   • If user says 'yes' → Goes back to intent classification")
        print("   • If user says 'no' → Ends session and waits for 'Blueberry'")
        print("   • Continuous loop for multiple tasks in one session")
        print("   • Session state management and reset")
        print()
        print("💬 CONTINUOUS HELP FLOW:")
        print("   1. User: 'Blueberry' → Wake-up word detected")
        print("   2. User: 'Create a function to print hello world'")
        print("   3. System: Completes task and generates code")
        print("   4. System: 'Is there anything else you'd like me to help you with?'")
        print("   5. User: 'Yes, create a Java class'")
        print("   6. System: 'Great! What would you like me to help you with next?'")
        print("   7. System: Starts new task flow")
        print("   8. After completion: 'Is there anything else you'd like me to help you with?'")
        print("   9. User: 'No'")
        print("   10. System: 'Perfect! Just say 'Blueberry' to start a new session. Goodbye!'")
        print()
        print("🎯 SESSION MANAGEMENT:")
        print("   • State reset between tasks")
        print("   • Fresh intent classification for each new task")
        print("   • Continuous conversation flow")
        print("   • Proper session ending and wake-up word detection")
        print()
        print("🔄 TASK FLOW EXAMPLES:")
        print("   Task 1: 'Create a Python function' → Completed")
        print("   System: 'Is there anything else you'd like me to help you with?'")
        print("   User: 'Yes'")
        print("   System: 'Great! What would you like me to help you with next?'")
        print("   Task 2: 'Create a JavaScript API' → Completed")
        print("   System: 'Is there anything else you'd like me to help you with?'")
        print("   User: 'No'")
        print("   System: 'Perfect! Just say 'Blueberry' to start a new session. Goodbye!'")
        print()
        print("💡 KEY BENEFITS:")
        print("   • Multiple tasks in one session")
        print("   • No need to say 'Blueberry' for each task")
        print("   • Continuous conversation flow")
        print("   • Efficient session management")
        print("   • Natural help loop")
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
