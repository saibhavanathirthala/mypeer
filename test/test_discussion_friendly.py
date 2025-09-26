#!/usr/bin/env python3
"""
Test Discussion-Friendly Interactive Features
Demonstrates: Real-time conversation, user interruption handling, and collaborative discussion
"""

import os
import sys
from dotenv import load_dotenv
from langgraph_pipeline import LangGraphVoicePipeline

def main():
    """Test the discussion-friendly interactive features"""
    print("🤖 Discussion-Friendly Interactive Features Test")
    print("🎯 Features: Real-time conversation + User interruption handling + Collaborative discussion + Interactive adaptation")
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
        print("🚀 Initializing Discussion-Friendly Interactive Pipeline...")
        pipeline = LangGraphVoicePipeline()

        print("✅ Discussion-Friendly Interactive Pipeline initialized successfully!")
        print()
        print("🤝 DISCUSSION-FRIENDLY FEATURES:")
        print("   • Real-time conversation with user")
        print("   • User can interrupt at any time")
        print("   • Interactive discussion loop")
        print("   • User can say 'I want something else'")
        print("   • System adapts to user feedback")
        print("   • Colleague-like communication")
        print("   • Pause and resume functionality")
        print("   • Help and clarification requests")
        print()
        print("💬 INTERACTIVE CONVERSATION FLOW:")
        print("   1. System: 'Hey! I'm working on [task]. I'll create a [language] [type] for you. What do you think?'")
        print("   2. User: 'Yes' → System proceeds")
        print("   3. User: 'No, I want something else' → System asks what to change")
        print("   4. User: 'Wait, stop' → System pauses and waits")
        print("   5. User: 'Help' → System provides assistance")
        print("   6. User: 'Change the language to JavaScript' → System adapts")
        print()
        print("🔄 USER INTERRUPTION HANDLING:")
        print("   • 'I want something else' → System asks what to change")
        print("   • 'Wait, stop, pause' → System pauses and waits")
        print("   • 'Help, what, how' → System provides assistance")
        print("   • 'Change, different' → System adapts to new requirements")
        print("   • 'No, wrong' → System asks for clarification")
        print()
        print("💻 COLLABORATIVE DISCUSSION EXAMPLES:")
        print("   System: 'Hey! I'm working on Create a new file. I'll create a Python function for you. What do you think?'")
        print("   User: 'I want something else'")
        print("   System: 'No problem! What would you like me to change or do differently?'")
        print("   User: 'Create a JavaScript API instead'")
        print("   System: 'Got it! I'll work on Create a JavaScript API instead. Let's continue.'")
        print()
        print("🎯 ADAPTIVE BEHAVIOR:")
        print("   • System listens to user feedback")
        print("   • Updates tasks based on user input")
        print("   • Maintains conversation context")
        print("   • Provides real-time assistance")
        print("   • Handles ambiguous responses")
        print("   • Offers clarification when needed")
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
