#!/usr/bin/env python3
"""
Test Smart File Naming and Enhanced Code Generation
Demonstrates: Smart filename generation based on user input and improved code quality
"""

import os
import sys
from dotenv import load_dotenv
from langgraph_pipeline import LangGraphVoicePipeline

def main():
    """Test the smart file naming and enhanced code generation"""
    print("🤖 Smart File Naming and Enhanced Code Generation Test")
    print("🎯 Features: Smart filename generation + Enhanced code quality + Interactive collaboration")
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
        print("🚀 Initializing Smart File Naming Pipeline...")
        pipeline = LangGraphVoicePipeline()

        print("✅ Smart File Naming Pipeline initialized successfully!")
        print()
        print("🎯 SMART FILE NAMING FEATURES:")
        print("   • Intelligent filename generation based on user input")
        print("   • Language-specific naming conventions")
        print("   • User-specified filename support")
        print("   • Content-aware naming (hello_world, main_function, etc.)")
        print()
        print("💻 ENHANCED CODE GENERATION:")
        print("   • Proper, working code generation")
        print("   • Language-specific best practices")
        print("   • Context-aware code templates")
        print("   • Hello World example: Creates actual working code")
        print()
        print("📁 FILENAME EXAMPLES:")
        print("   • 'Create a function to print hello world' → hello_world.py")
        print("   • 'Build a JavaScript API' → api_server.js")
        print("   • 'Create a Java class' → main_class.java")
        print("   • 'Write a Python function' → main_function.py")
        print("   • 'Create HTML page' → index.html")
        print("   • 'Write SQL queries' → database_schema.sql")
        print()
        print("💬 INTERACTIVE COLLABORATION:")
        print("   • Step-by-step todo generation")
        print("   • User confirmation for each step")
        print("   • Colleague-like communication")
        print("   • Smart file naming with user input")
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
