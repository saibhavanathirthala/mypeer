#!/usr/bin/env python3
"""
Test Interactive Flow - Collaborative Code Generation
Demonstrates: Wake-up → Voice → Speech-to-Text → Confirmation → Intent Classification → Interactive Todo Generation → Collaborative Code Generation
"""

import os
import sys
from dotenv import load_dotenv
from langgraph_pipeline import LangGraphVoicePipeline

def main():
    """Test the interactive collaborative flow"""
    print("🤖 Interactive Collaborative Code Generation Test")
    print("🎯 Flow: Wake-up → Voice → Speech-to-Text → Confirmation → Intent Classification → Interactive Todo Generation → Collaborative Code Generation")
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
        print("🚀 Initializing Interactive Collaborative Pipeline...")
        pipeline = LangGraphVoicePipeline()

        print("✅ Interactive Collaborative Pipeline initialized successfully!")
        print()
        print("🤝 INTERACTIVE COLLABORATIVE FEATURES:")
        print("   • Wake-up word detection (Blueberry)")
        print("   • Voice input capture")
        print("   • Speech-to-text conversion")
        print("   • User confirmation")
        print("   • Intent classification (coding, explanation, review)")
        print("   • Interactive todo generation with step-by-step collaboration")
        print("   • Collaborative code generation with user feedback")
        print("   • Real-time todo completion checking")
        print("   • Colleague-like communication throughout the process")
        print()
        print("💬 Example interaction:")
        print("   User: 'Create a function to print hello world'")
        print("   System: 'Great! I've created a plan with 3 tasks. Let's start with the first one: Create a new file with appropriate name and extension. Should I proceed with this?'")
        print("   User: 'Yes'")
        print("   System: 'Perfect! I've created the Python code for Create a new file. It's saved as generated_code_123.py. Ready for the next task?'")
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
