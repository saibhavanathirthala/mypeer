#!/usr/bin/env python3
"""
Test Language Specification Feature
Demonstrates: Language detection, user prompting for language choice, and smart filename generation
"""

import os
import sys
from dotenv import load_dotenv
from langgraph_pipeline import LangGraphVoicePipeline

def main():
    """Test the language specification feature"""
    print("🤖 Language Specification Feature Test")
    print("🎯 Features: Language detection + User prompting + Smart filename generation + Interactive collaboration")
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
        print("🚀 Initializing Language Specification Pipeline...")
        pipeline = LangGraphVoicePipeline()

        print("✅ Language Specification Pipeline initialized successfully!")
        print()
        print("🎯 LANGUAGE SPECIFICATION FEATURES:")
        print("   • Automatic language detection from user input")
        print("   • User prompting when language not specified")
        print("   • Support for 20+ programming languages")
        print("   • Smart filename generation based on language")
        print("   • Interactive language selection")
        print()
        print("💻 SUPPORTED LANGUAGES:")
        print("   • Python, JavaScript, Java, C++, C#, Go, Rust")
        print("   • PHP, Ruby, Swift, Kotlin, TypeScript")
        print("   • HTML, CSS, SQL, Bash, PowerShell")
        print("   • YAML, JSON, XML")
        print()
        print("📝 EXAMPLE INTERACTIONS:")
        print("   User: 'Create a function to print hello world'")
        print("   System: 'I need to know which programming language you'd like me to use. Please specify: Python, JavaScript, Java, C++, Go, Rust, PHP, Ruby, Swift, Kotlin, TypeScript, HTML, CSS, SQL, Bash, or PowerShell?'")
        print("   User: 'JavaScript'")
        print("   System: 'Great! I'll use JavaScript for this task.'")
        print()
        print("   User: 'Create a Python function to calculate fibonacci'")
        print("   System: 'I'll use Python for this task.' (Language detected automatically)")
        print()
        print("💬 INTERACTIVE FLOW:")
        print("   1. User makes request")
        print("   2. System detects language (if specified)")
        print("   3. If no language specified, system asks user to choose")
        print("   4. User specifies language")
        print("   5. System confirms language choice")
        print("   6. System generates code in specified language")
        print("   7. System saves with appropriate filename and extension")
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
