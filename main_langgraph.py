"""
Main entry point for LangGraph Voice Pipeline - Universal Code Generation
Tests: Wake-up Word → Voice Input → Speech-to-Text → Confirmation → Intent Classification → Universal Code Generation
"""

import os
import sys
from dotenv import load_dotenv
from langgraph_pipeline import LangGraphVoicePipeline

def main():
    """Main entry point - Universal Code Generation Pipeline."""
    print(" LangGraph Voice Pipeline - Universal Code Generation")
    print(" Testing: Wake-up → Voice → Speech-to-Text → Confirmation → Intent Classification → Universal Code Generation")
    print("=" * 80)

    # Load environment variables
    load_dotenv()

    # Verify OpenAI API key
    if not os.getenv("OPENAI_API_KEY"):
        print("ERROR: OPENAI_API_KEY not found in environment variables.")
        print("Please set your OpenAI API key in a .env file or environment variable.")
        sys.exit(1)

    # Check for Porcupine API key (optional, will fallback to manual activation)
    porcupine_key = os.getenv("PORCUPINE_ACCESS_KEY")
    if not porcupine_key:
        print("  WARNING: PORCUPINE_ACCESS_KEY not found.")
        print("   Wake-up word detection will be disabled.")
        print("   You can get a free API key from: https://picovoice.ai/")
        print("   Or the system will use manual activation instead.")
        print()

    try:
        # Initialize LangGraph pipeline
        print(" Initializing LangGraph Voice Pipeline...")
        pipeline = LangGraphVoicePipeline()

        print(" Universal Code Generation Pipeline initialized successfully!")
        print()
        print(" CONTINUOUS VOICE CODING FEATURES:")
        print("   • Continuous loop operation with session management")
        print("   • Wake-up word detection (Blueberry) for each new session")
        print("   • Voice input capture (10s max, 1.5s silence detection)")
        print("   • Speech-to-text conversion")
        print("   • User confirmation")
        print("   • Intent classification (coding, explanation, review)")
        print("   • Universal code generation for multiple languages:")
        print("     - Python, JavaScript, Java, C++, C#, Go, Rust")
        print("     - PHP, Ruby, Swift, Kotlin, TypeScript")
        print("     - HTML, CSS, SQL, Bash, PowerShell")
        print("     - YAML, JSON, XML")
        print("   • Multiple task types: functions, classes, APIs, databases, tests, scripts")
        print("   • Automatic file extension detection")
        print("   • Code iteration and feedback loops")
        print("   •  CodeRabbit AI Code Review:")
        print("     - Say 'Please review my code' to trigger CodeRabbit review")
        print("     - GPT-4 summarized review with natural filler sounds")
        print("     - Critical issues highlighted in voice feedback")
        print("     - Rate limit handling with graceful error messages")
        print("   • After completion: asks for more help")
        print("   • If 'I don't want any help': session ends, waits for Blueberry")
        print("   • If 'yes': starts new task immediately")
        print("   • Session end → Wake-up word detection → New session")
        print()

        # Start the continuous voice session
        pipeline.start_continuous_session()

    except KeyboardInterrupt:
        print("\n\n👋 Session ended by user. Goodbye!")
    except Exception as e:
        print(f"\n Fatal error: {str(e)}")
        print("Please check your configuration and try again.")
        sys.exit(1)


if __name__ == "__main__":
    main()
