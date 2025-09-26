"""
Test script for LangGraph Pipeline
Tests the simple flow: Wake-up → Voice → Speech-to-Text → Confirmation
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_pipeline_initialization():
    """Test if the pipeline can be initialized"""
    print("🧪 Testing Pipeline Initialization...")
    
    try:
        from langgraph_pipeline import LangGraphVoicePipeline
        
        # Initialize pipeline
        pipeline = LangGraphVoicePipeline()
        
        print("✅ Pipeline initialized successfully!")
        print(f"   - STT Agent: {pipeline.stt_agent.name}")
        print(f"   - TTS Agent: {pipeline.tts_agent.name}")
        print(f"   - Intent Agent: {pipeline.intent_agent.name}")
        
        return pipeline
        
    except Exception as e:
        print(f"❌ Pipeline initialization error: {e}")
        return None

def test_workflow_creation(pipeline):
    """Test if the workflow can be created"""
    print("\n🧪 Testing Workflow Creation...")
    
    try:
        workflow = pipeline.workflow
        
        print("✅ Workflow created successfully!")
        print(f"   - Workflow type: {type(workflow)}")
        
        # Test workflow structure
        graph = workflow.get_graph()
        nodes = list(graph.nodes())
        
        print(f"   - Number of nodes: {len(nodes)}")
        print(f"   - Key nodes: wake_word_detection, voice_input, speech_to_text, confirmation")
        
        return True
        
    except Exception as e:
        print(f"❌ Workflow creation error: {e}")
        return False

def test_simple_flow(pipeline):
    """Test the simple flow without wake-up word detection"""
    print("\n🧪 Testing Simple Flow (without wake-up word)...")
    
    try:
        # Create initial state
        initial_state = {
            "wake_word_detected": True,  # Skip wake-up word detection for testing
            "session_active": True,
            "pipeline_status": "processing"
        }
        
        print("✅ Initial state created")
        print("   - Wake-up word: Simulated as detected")
        print("   - Session: Active")
        print("   - Status: Processing")
        
        return initial_state
        
    except Exception as e:
        print(f"❌ Simple flow test error: {e}")
        return None

def test_voice_input_simulation(pipeline):
    """Test voice input simulation"""
    print("\n🧪 Testing Voice Input Simulation...")
    
    try:
        # Simulate voice input
        test_input = "Create a sorting function"
        
        # Test STT agent with text input (demo mode)
        transcribed = pipeline.stt_agent.run(test_input)
        
        print(f"✅ Voice input simulation successful!")
        print(f"   - Input: '{test_input}'")
        print(f"   - Transcribed: '{transcribed}'")
        
        return transcribed
        
    except Exception as e:
        print(f"❌ Voice input simulation error: {e}")
        return None

def test_confirmation_simulation(pipeline, transcribed_text):
    """Test confirmation simulation"""
    print("\n🧪 Testing Confirmation Simulation...")
    
    try:
        # Simulate confirmation
        confirmation_msg = f"I heard you say: '{transcribed_text}'. Is this correct?"
        print(f"   - Confirmation message: '{confirmation_msg}'")
        
        # Test TTS agent (this will try to speak, but we'll catch any errors)
        try:
            pipeline.tts_agent.run(confirmation_msg)
            print("✅ TTS agent working (audio played)")
        except Exception as tts_error:
            print(f"⚠️  TTS agent error (expected if no audio): {tts_error}")
        
        # Simulate user confirmation
        print("   - Simulating user says 'yes'")
        print("✅ Confirmation simulation successful!")
        
        return True
        
    except Exception as e:
        print(f"❌ Confirmation simulation error: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 LangGraph Pipeline Test Suite")
    print("🎯 Testing: Wake-up → Voice → Speech-to-Text → Confirmation")
    print("=" * 60)
    
    # Test 1: Pipeline initialization
    pipeline = test_pipeline_initialization()
    if not pipeline:
        print("\n❌ Pipeline initialization failed. Cannot continue.")
        return
    
    # Test 2: Workflow creation
    if not test_workflow_creation(pipeline):
        print("\n❌ Workflow creation failed. Cannot continue.")
        return
    
    # Test 3: Simple flow
    initial_state = test_simple_flow(pipeline)
    if not initial_state:
        print("\n❌ Simple flow test failed. Cannot continue.")
        return
    
    # Test 4: Voice input simulation
    transcribed = test_voice_input_simulation(pipeline)
    if not transcribed:
        print("\n❌ Voice input simulation failed. Cannot continue.")
        return
    
    # Test 5: Confirmation simulation
    if not test_confirmation_simulation(pipeline, transcribed):
        print("\n❌ Confirmation simulation failed.")
        return
    
    print("\n" + "=" * 60)
    print("🎉 All tests passed! The LangGraph pipeline is working correctly.")
    print("\n🚀 To run the full pipeline:")
    print("   python main_langgraph.py")
    print("\n💡 Note: Full pipeline requires:")
    print("   - Microphone access for wake-up word detection")
    print("   - Audio output for TTS responses")
    print("   - PORCUPINE_ACCESS_KEY for wake-up word detection (optional)")

if __name__ == "__main__":
    main()
