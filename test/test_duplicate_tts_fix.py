#!/usr/bin/env python3
"""
Test Duplicate TTS Fix
Demonstrates: No duplicate TTS calls in interactive discussion loop
"""

import os
import sys
from unittest.mock import MagicMock, patch
from langgraph_pipeline import LangGraphVoicePipeline, VoiceCodingState
from typing import List

# Mock the STTAgent and TTSPromptAgent for testing
class MockSTTAgent:
    def __init__(self):
        self.transcriptions = []
        self.call_count = 0

    def run(self, audio_input):
        # Simulate transcription
        self.call_count += 1
        if self.transcriptions:
            return self.transcriptions.pop(0)
        return "default transcription"

    def auto_record_speech(self, max_duration=None):
        self.call_count += 1
        if self.transcriptions:
            return self.transcriptions.pop(0)
        return "default response"

    def listen_for_wake_word(self):
        self.call_count += 1
        return True # Always detect wake word for testing

class MockTTSPromptAgent:
    def __init__(self):
        self.speech_count = 0
        self.speech_messages = []

    def run(self, text):
        self.speech_count += 1
        self.speech_messages.append(text)
        print(f"[MockTTSPromptAgent] Speech #{self.speech_count}: {text}")

def test_duplicate_tts_fix():
    print("\n--- Running Duplicate TTS Fix Test ---")

    # Mock agents
    mock_stt_agent = MockSTTAgent()
    mock_tts_agent = MockTTSPromptAgent()

    # Patch the agents in the pipeline
    with patch('langgraph_pipeline.STTAgent', return_value=mock_stt_agent), \
         patch('langgraph_pipeline.TTSPromptAgent', return_value=mock_tts_agent):

        pipeline = LangGraphVoicePipeline()

        # Scenario: User asks for help during interactive discussion
        mock_stt_agent.transcriptions = [
            "create a function to print hello world", # Initial request
            "yes", # Confirmation
            "yes", # Proceed with first todo
            "help", # User asks for help
            "I want to know more about the function", # Help response
            "yes", # Proceed with second todo
            "yes", # Proceed with third todo
            "yes" # Continue after code generation
        ]

        print("\n--- Scenario: Help Request During Discussion ---")
        initial_state: VoiceCodingState = {
            "wake_word_detected": False,
            "voice_input": "",
            "transcribed_text": "",
            "user_confirmed": False,
            "confirmation_status": "",
            "confirmation_spoken": False,
            "current_step": "wake_word_detection",
            "pipeline_status": "active",
            "error_message": "",
            "user_intent": "",
            "generated_todos": [],
            "todos_completed": False,
            "generated_code": "",
            "code_file_path": "",
            "code_explanation": "",
            "code_review": "",
            "review_score": 0,
            "user_feedback": "",
            "feedback_processed": False,
            "iteration_count": 0,
            "max_iterations": 3,
            "final_response": "",
            "interaction_count": 0,
            "current_todo_index": 0
        }
        result = pipeline.workflow.invoke(initial_state)

        # Check for duplicate TTS calls
        print(f"\n📊 TTS Analysis:")
        print(f"   Total TTS calls: {mock_tts_agent.speech_count}")
        print(f"   TTS messages: {len(mock_tts_agent.speech_messages)}")
        
        # Check for duplicate messages
        duplicate_messages = []
        for i, message in enumerate(mock_tts_agent.speech_messages):
            if message in mock_tts_agent.speech_messages[i+1:]:
                duplicate_messages.append(message)
        
        if duplicate_messages:
            print(f"❌ Found duplicate TTS messages: {duplicate_messages}")
            return False
        else:
            print("✅ No duplicate TTS messages found!")
            return True

if __name__ == "__main__":
    # Set environment variables for testing
    os.environ["OPENAI_API_KEY"] = "test_key"
    os.environ["PORCUPINE_ACCESS_KEY"] = "test_key"
    test_duplicate_tts_fix()
