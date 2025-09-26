"""
LangGraph Voice Pipeline - Confirmation Flow Only
Implements: Wake-up Word → Voice Input → Speech-to-Text → Confirmation
"""

import os
import time
from typing import TypedDict, Optional
from dotenv import load_dotenv

# LangGraph and LangChain imports
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

# Import our existing agents (only what we need for confirmation flow)
from agents import (
    STTAgent, TTSPromptAgent
)
from prompts import (
    WELCOME_MESSAGE
)

# Load environment variables
load_dotenv()


class VoiceCodingState(TypedDict):
    """State for the voice coding pipeline - confirmation flow only"""
    # Wake-up word detection
    wake_word_detected: bool
    
    # Voice input
    voice_input: str
    
    # Speech-to-text
    transcribed_text: str
    
    # Confirmation
    user_confirmed: bool
    confirmation_status: str  # "confirmed", "re_record", "cancelled"
    confirmation_spoken: bool  # Track if confirmation message has been spoken
    
    # Pipeline state
    current_step: str
    pipeline_status: str  # "active", "completed", "error"
    error_message: str
    
    # Session management
    interaction_count: int


class LangGraphVoicePipeline:
    """LangGraph-based voice coding pipeline with wake-up word detection - Confirmation Flow Only"""
    
    def __init__(self):
        """Initialize the pipeline with only confirmation flow agents"""
        # Initialize only the agents needed for confirmation flow
        self.stt_agent = STTAgent()
        self.tts_agent = TTSPromptAgent()
        
        # Create the workflow
        self.workflow = self._create_workflow()
        
        print("✅ LangGraph Voice Pipeline initialized successfully!")
        print("🎯 Flow: Wake-up → Voice → Speech-to-Text → Confirmation → Intent Classification")
    
    def _create_workflow(self) -> StateGraph:
        """Create the confirmation flow workflow"""
        
        # Create the workflow
        workflow = StateGraph(VoiceCodingState)
        
        # Add confirmation flow nodes
        workflow.add_node("wake_word_detection", self._wake_word_detection_node)
        workflow.add_node("voice_input", self._voice_input_node)
        workflow.add_node("speech_to_text", self._speech_to_text_node)
        workflow.add_node("confirmation", self._confirmation_node)
        workflow.add_node("intent_classification", self._intent_classification_node)
        
        # Define the flow
        workflow.set_entry_point("wake_word_detection")
        
        # Wake-up word detection routing
        workflow.add_conditional_edges(
            "wake_word_detection",
            self._should_continue_after_wake_word,
            {
                "voice_input": "voice_input",
                END: END
            }
        )
        
        # Main flow - Simple pipeline: Wake-up → Voice → Speech-to-Text → Confirmation
        workflow.add_edge("voice_input", "speech_to_text")
        workflow.add_edge("speech_to_text", "confirmation")
        
        # Confirmation routing - Simple flow
        workflow.add_conditional_edges(
            "confirmation",
            self._should_continue_after_confirmation_simple,
            {
                "voice_input": "voice_input",  # Go back to voice input if "no"
                "intent_classification": "intent_classification"  # Go to intent classification if confirmed
            }
        )
        
        # Intent classification goes to END
        workflow.add_edge("intent_classification", END)
        
        return workflow.compile()
    
    # ==================== NODE IMPLEMENTATIONS ====================
    
    def _wake_word_detection_node(self, state: VoiceCodingState) -> VoiceCodingState:
        """Node 1: Detect wake-up word using STT Agent"""
        print("🎧 [Node 1] Listening for wake-up word...")
        
        try:
            # Use STT agent's wake-up word detection
            wake_word_detected = self.stt_agent.listen_for_wake_word()
            
            state["wake_word_detected"] = wake_word_detected
            state["current_step"] = "wake_word_detection"
            
            if wake_word_detected:
                print("✅ Wake-up word detected! Starting voice input...")
            else:
                print("⏰ Wake-up word timeout. Ending session.")
                state["pipeline_status"] = "completed"
                
        except Exception as e:
            print(f"❌ Error in wake-up word detection: {e}")
            state["error_message"] = str(e)
            state["pipeline_status"] = "error"
        
        return state
    
    def _voice_input_node(self, state: VoiceCodingState) -> VoiceCodingState:
        """Node 2: Capture voice input using STT Agent"""
        print("🎤 [Node 2] Capturing voice input...")
        
        try:
            # Reset confirmation spoken flag when starting new voice input
            state["confirmation_spoken"] = False
            
            # Capture voice input using STT agent (no prompt needed after wake-up word)
            voice_input = self.stt_agent.auto_record_speech(max_duration=30)
            
            if voice_input:
                state["voice_input"] = voice_input
                state["current_step"] = "voice_input"
                print(f"🎤 Voice input captured: '{voice_input}'")
            else:
                state["error_message"] = "No voice input detected"
                state["pipeline_status"] = "error"
                
        except Exception as e:
            print(f"❌ Error in voice input: {e}")
            state["error_message"] = str(e)
            state["pipeline_status"] = "error"
        
        return state
    
    def _speech_to_text_node(self, state: VoiceCodingState) -> VoiceCodingState:
        """Node 3: Convert speech to text using STT Agent"""
        print("📝 [Node 3] Converting speech to text...")
        
        try:
            voice_input = state.get("voice_input", "")
            
            if voice_input:
                # Use STT agent to transcribe
                transcribed_text = self.stt_agent.run(voice_input)
                
                state["transcribed_text"] = transcribed_text
                state["current_step"] = "speech_to_text"
                
                print(f"📝 Transcribed: '{transcribed_text}'")
            else:
                state["error_message"] = "No voice input to transcribe"
                state["pipeline_status"] = "error"
                
        except Exception as e:
            print(f"❌ Error in speech-to-text: {e}")
            state["error_message"] = str(e)
            state["pipeline_status"] = "error"
        
        return state
    
    def _confirmation_node(self, state: VoiceCodingState) -> VoiceCodingState:
        """Node 4: Confirm transcribed text with user - Simple and clean"""
        print("✅ [Node 4] Confirming transcribed text...")
        
        try:
            transcribed_text = state.get("transcribed_text", "")
            
            if transcribed_text:
                # Only speak confirmation message once
                if not state.get("confirmation_spoken", False):
                    confirmation_msg = f"I heard you say: '{transcribed_text}'. Is this correct?"
                    print(f"🔊 Speaking: {confirmation_msg}")
                    self.tts_agent.run(confirmation_msg)
                    state["confirmation_spoken"] = True
                
                # Always process user response (even if confirmation was already spoken)
                print("🎤 Listening for your response...")
                confirmation_response = self.stt_agent.auto_record_speech(max_duration=5)
                
                if confirmation_response:
                    confirmation_lower = confirmation_response.lower().strip()
                    print(f"📝 You said: '{confirmation_response}'")
                    
                    if any(word in confirmation_lower for word in ["yes", "correct", "right", "yeah", "yep", "ok", "okay"]):
                        state["user_confirmed"] = True
                        state["confirmation_status"] = "confirmed"
                        print("✅ User confirmed! Ready for intent classification.")
                    else:
                        state["user_confirmed"] = False
                        state["confirmation_status"] = "re_record"
                        print("🔄 User wants to re-record. Going back to voice input.")
                        # Say sorry and ask to try again
                        sorry_msg = "I'm sorry, can you say it again?"
                        print(f"🔊 Speaking: {sorry_msg}")
                        self.tts_agent.run(sorry_msg)
                else:
                    state["user_confirmed"] = False
                    state["confirmation_status"] = "re_record"
                    print("⏰ No response. Going back to voice input.")
                    # Say sorry and ask to try again
                    sorry_msg = "I'm sorry, can you say it again?"
                    print(f"🔊 Speaking: {sorry_msg}")
                    self.tts_agent.run(sorry_msg)
                
                state["current_step"] = "confirmation"
            else:
                state["error_message"] = "No transcribed text to confirm"
                state["pipeline_status"] = "error"
                
        except Exception as e:
            print(f"❌ Error in confirmation: {e}")
            state["error_message"] = str(e)
            state["pipeline_status"] = "error"
        
        return state
    
    def _intent_classification_node(self, state: VoiceCodingState) -> VoiceCodingState:
        """Node 5: Classify user intent - Simple placeholder for now"""
        print("🧠 [Node 5] Classifying user intent...")
        
        try:
            transcribed_text = state.get("transcribed_text", "")
            
            if transcribed_text:
                # Simple intent classification (placeholder)
                # In a real implementation, you'd use an LLM or ML model here
                if any(word in transcribed_text.lower() for word in ["code", "program", "function", "class", "write"]):
                    intent = "coding"
                elif any(word in transcribed_text.lower() for word in ["explain", "what", "how", "why"]):
                    intent = "explanation"
                elif any(word in transcribed_text.lower() for word in ["review", "check", "analyze"]):
                    intent = "review"
                else:
                    intent = "general"
                
                state["user_intent"] = intent
                state["current_step"] = "intent_classification"
                
                print(f"🎯 Classified intent: {intent}")
                
                # For now, just end the pipeline after intent classification
                state["pipeline_status"] = "completed"
                print("✅ Intent classification completed. Pipeline finished.")
            else:
                state["error_message"] = "No transcribed text for intent classification"
                state["pipeline_status"] = "error"
                
        except Exception as e:
            print(f"❌ Error in intent classification: {e}")
            state["error_message"] = str(e)
            state["pipeline_status"] = "error"
        
        return state
    
    # ==================== ROUTING FUNCTIONS ====================
    
    def _should_continue_after_wake_word(self, state: VoiceCodingState) -> str:
        """Determine next step after wake word detection"""
        wake_word_detected = state.get("wake_word_detected", False)
        
        if wake_word_detected:
            return "voice_input"
        else:
            return END
    
    def _should_continue_after_confirmation_simple(self, state: VoiceCodingState) -> str:
        """Simple confirmation routing - Wake-up → Voice → Speech-to-Text → Confirmation → Intent Classification"""
        confirmation_status = state.get("confirmation_status", "confirmed")
        
        if confirmation_status == "confirmed":
            return "intent_classification"  # Go to intent classification after confirmation
        elif confirmation_status == "re_record":
            return "voice_input"  # Go back to voice input if "no"
        else:  # cancelled
            return END
    
    # ==================== MAIN EXECUTION METHODS ====================
    
    def run_pipeline(self, initial_state: Optional[VoiceCodingState] = None) -> VoiceCodingState:
        """Run the confirmation flow pipeline"""
        if initial_state is None:
            initial_state = {
                "wake_word_detected": False,
                "voice_input": "",
                "transcribed_text": "",
                "user_confirmed": False,
                "confirmation_status": "",
                "current_step": "wake_word_detection",
                "pipeline_status": "active",
                "error_message": "",
                "interaction_count": 0
            }
        
        try:
            print("🚀 Starting Confirmation Flow Pipeline...")
            result = self.workflow.invoke(initial_state)
            print("✅ Confirmation flow completed!")
            return result
            
        except Exception as e:
            print(f"❌ Pipeline error: {e}")
            return {
                "error_message": str(e),
                "pipeline_status": "error"
            }
    
    def start_continuous_session(self):
        """Start the continuous voice coding session with confirmation flow only"""
        print("\n🎯 Starting Voice Coding Session...")
        print("📋 Flow: Wake-up Word → Voice Input → Speech-to-Text → Confirmation → Intent Classification")
        print("💡 Say 'Blueberry' to start, then speak your request")
        print("🔄 After confirmation, intent will be classified")
        print("⏹️  Press Ctrl+C to exit anytime")
        print("\n" + "=" * 60)
        
        try:
            print("\n🔄 Starting interaction...")
            
            # Initialize state for this interaction
            initial_state = {
                "wake_word_detected": False,
                "voice_input": "",
                "transcribed_text": "",
                "user_confirmed": False,
                "confirmation_status": "",
                "confirmation_spoken": False,
                "current_step": "wake_word_detection",
                "pipeline_status": "active",
                "error_message": "",
                "interaction_count": 0
            }
            
            # Run the workflow
            result = self.workflow.invoke(initial_state)
            
            # Check if user confirmed
            if result.get("user_confirmed"):
                print("\n✅ User confirmed! Intent classification completed.")
                print(f"🎯 Intent: {result.get('user_intent', 'unknown')}")
            else:
                print("\n❌ User did not confirm. Flow ended.")
            
            print("\n✅ Session completed!")
                
        except KeyboardInterrupt:
            print("\n\n👋 Session interrupted by user. Goodbye!")
        except Exception as e:
            print(f"\n❌ Session error: {e}")
            print("Restarting session...")
            time.sleep(2)


def main():
    """Main entry point for LangGraph Voice Pipeline - Confirmation Flow Only"""
    print("🤖 LangGraph Voice Pipeline - Confirmation Flow")
    print("🎯 Testing: Wake-up → Voice → Speech-to-Text → Confirmation")
    print("=" * 60)
    
    # Initialize pipeline
    pipeline = LangGraphVoicePipeline()
    
    # Start continuous session
    pipeline.start_continuous_session()


if __name__ == "__main__":
    main()