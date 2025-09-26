"""
Main entry point for LangGraph Voice Pipeline - Confirmation Flow Only
Tests: Wake-up Word → Voice Input → Speech-to-Text → Confirmation
"""

import os
import sys
from dotenv import load_dotenv
from langgraph_pipeline import LangGraphVoicePipeline

def main():
    """Main entry point - Confirmation Flow Test Only."""
    print("🤖 LangGraph Voice Pipeline - Confirmation Flow Test")
    print("🎯 Testing: Wake-up → Voice → Speech-to-Text → Confirmation")
    print("=" * 60)
    
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
        print("⚠️  WARNING: PORCUPINE_ACCESS_KEY not found.")
        print("   Wake-up word detection will be disabled.")
        print("   You can get a free API key from: https://picovoice.ai/")
        print("   Or the system will use manual activation instead.")
        print()
    
    try:
        # Initialize LangGraph pipeline
        print("🚀 Initializing LangGraph Voice Pipeline...")
        pipeline = LangGraphVoicePipeline()
        
        print("✅ Confirmation Flow Pipeline initialized successfully!")
        print()
        print("🎤 CONFIRMATION FLOW FEATURES:")
        print("   • Wake-up word detection (Blueberry)")
        print("   • Voice input capture")
        print("   • Speech-to-text conversion")
        print("   • User confirmation")
        print("   • Loop back if not confirmed")
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
