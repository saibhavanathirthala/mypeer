"""
Text-to-Speech Agent using OpenAI TTS API.
Handles voice confirmations and responses to the user.
"""

import os
import tempfile
import pygame
from pathlib import Path
from openai import OpenAI
from .base_agent import BaseAgent


class TTSPromptAgent(BaseAgent):
    """Text-to-Speech Agent for confirmations and responses."""
    
    def __init__(self, config: dict = None):
        super().__init__("TTSPromptAgent", config)
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        # Initialize pygame mixer for audio playback
        pygame.mixer.init()
        # Flag to stop TTS when interrupted
        self._stop_tts = False
    
    def run(self, input_data: str) -> str:
        """
        Convert text to speech and play it back.
        
        Args:
            input_data: Text to convert to speech
            
        Returns:
            The same text that was spoken
        """
        try:
            self.log(f"Converting to speech: '{input_data}'")
            
            # Generate speech using OpenAI TTS
            response = self.client.audio.speech.create(
                model="tts-1",
                voice="alloy",  # You can change to: alloy, echo, fable, onyx, nova, shimmer
                input=input_data
            )
            
            # Save to temporary file
            with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_file:
                temp_path = temp_file.name
                response.stream_to_file(temp_path)
            
            # Play the audio
            self._play_audio(temp_path)
            
            # Clean up temporary file
            os.unlink(temp_path)
            
            self.log("Speech playback completed")
            return input_data
            
        except Exception as e:
            self.log(f"Error in TTS: {str(e)}")
            # Fallback: just print the text
            print(f"[TTS FALLBACK] {input_data}")
            return input_data
    
    def _play_audio(self, file_path: str) -> None:
        """Play audio file using pygame with interruption handling."""
        try:
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.play()
            
            # Wait for playback to complete with interruption handling
            while pygame.mixer.music.get_busy() and not self._stop_tts:
                pygame.time.wait(100)
                
        except KeyboardInterrupt:
            # Stop audio playback immediately on Ctrl+C
            pygame.mixer.music.stop()
            print("\n🔇 TTS interrupted by user")
        except Exception as e:
            self.log(f"Error playing audio: {str(e)}")
            # Just continue without audio playback
            pass
    
    def stop_tts(self):
        """Stop TTS playback immediately."""
        self._stop_tts = True
        pygame.mixer.music.stop()
        print("🔇 TTS stopped")
    
    def confirm_request(self, user_request: str) -> str:
        """
        Create and speak a confirmation message.
        
        Args:
            user_request: The user's original request
            
        Returns:
            Confirmation message
        """
        confirmation_msg = f"So you are asking me to {user_request}, am I correct?"
        self.run(confirmation_msg)
        return confirmation_msg
    
    def get_user_confirmation(self, stt_agent, use_voice=True, auto_detect=True) -> bool:
        """
        Get user confirmation via voice only (no typing allowed).
        
        Args:
            stt_agent: STT agent for voice input (required)
            use_voice: Whether to use voice input (always True)
            auto_detect: Whether to use automatic voice detection (always True)
            
        Returns:
            True if user confirms, False otherwise
        """
        self.log("Waiting for voice confirmation...")
        
        # Always use automatic voice detection in voice-only mode
        is_confirmed = stt_agent.get_voice_confirmation_auto(
            "Do you confirm this request?"
        )
        
        if is_confirmed:
            self.run("Perfect! Let me proceed with your request.")
        else:
            self.run("No problem. Please give me a new request when you're ready.")
        
        return is_confirmed
    
    def notify_completion(self, message: str) -> str:
        """
        Notify the user of task completion.
        
        Args:
            message: Completion message
            
        Returns:
            The notification message
        """
        notification = f"Task completed: {message}"
        self.run(notification)
        return notification