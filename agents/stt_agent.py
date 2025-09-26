"""
Speech-to-Text Agent using OpenAI Whisper API.
Handles voice input transcription with live microphone recording capability.
Enhanced with wake-up word detection using Porcupine.

__init__ - Initialize the agent
_initialize_porcupine - Set up wake-up word detection
set_wake_word_callback - Set callback for wake-up word
listen_for_wake_word - Listen for "Hey lily"
run - Main transcription function
record_and_transcribe - Fixed-duration recording
get_voice_confirmation - Voice confirmation (deprecated)
is_speech - Voice activity detection
auto_record_speech - Intelligent speech recording
_wait_for_speech_start - Wait for speech to begin
_record_until_silence - Record until silence
_transcribe_audio_data - Transcribe audio data
get_voice_confirmation_auto - Auto voice confirmation
"""

import os
import tempfile
import time
import threading
import numpy as np
import sounddevice as sd
import scipy.io.wavfile as wav
import webrtcvad
import pyaudio
import pvporcupine
from typing import Union, Optional, Callable
from openai import OpenAI
from .base_agent import BaseAgent


class STTAgent(BaseAgent):
    """Speech-to-Text Agent using OpenAI Whisper API with automatic voice detection and wake-up word."""
    
    def __init__(self, config: dict = None):
        super().__init__("STTAgent", config)
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        # Voice Activity Detection settings
        self.vad = webrtcvad.Vad(2)  # Aggressiveness level (0-3, 2 is balanced)
        self.sample_rate = 16000  # Required for webrtcvad
        self.frame_duration = 30  # ms (10, 20, or 30)
        self.frame_size = int(self.sample_rate * self.frame_duration / 1000)
        
        # Speech detection settings
        self.silence_threshold = 1.5  # seconds of silence to stop recording
        self.min_speech_duration = 0.5  # minimum seconds of speech to consider valid
        self.listening = False
        
        # Wake-up word detection settings
        self.wake_word_enabled = True
        self.wake_word = "blueberry"  # Default wake word (using available keyword)
        self.porcupine = None
        self.wake_word_detected = threading.Event()
        self.wake_word_callback = None
        self._initialize_porcupine()
    
    def _initialize_porcupine(self):
        """Initialize Porcupine for wake-up word detection."""
        try:
            # Initialize Porcupine with default wake word
            self.porcupine = pvporcupine.create(
                keywords=["blueberry"],  # Default wake word (using available keyword)
                access_key=os.getenv("PORCUPINE_ACCESS_KEY", ""),  # You'll need to get this from Picovoice
                sensitivities=[0.5]  # Sensitivity level (0.0 to 1.0)
            )
            self.log("Wake-up word detection initialized successfully")
        except Exception as e:
            self.log(f"Failed to initialize wake-up word detection: {e}")
            self.wake_word_enabled = False
    
    def set_wake_word_callback(self, callback: Callable):
        """Set callback function to be called when wake word is detected."""
        self.wake_word_callback = callback
    
    def listen_for_wake_word(self, timeout: Optional[float] = None) -> bool:
        """
        Listen for wake-up word continuously.
        
        Args:
            timeout: Maximum time to listen (None for infinite)
            
        Returns:
            True if wake word detected, False if timeout or error
        """
        if not self.wake_word_enabled or not self.porcupine:
            self.log("Wake-up word detection not available")
            return False
        
        try:
            self.log(f"🎧 Listening for wake-up word: '{self.wake_word}'")
            
            # Audio stream settings
            pa = pyaudio.PyAudio()
            stream = pa.open(
                rate=self.porcupine.sample_rate,
                channels=1,
                format=pyaudio.paInt16,
                input=True,
                frames_per_buffer=self.porcupine.frame_length
            )
            
            start_time = time.time()
            
            while True:
                # Check timeout
                if timeout and (time.time() - start_time) > timeout:
                    self.log("Wake-up word listening timeout")
                    break
                
                # Read audio frame
                pcm = stream.read(self.porcupine.frame_length)
                pcm = np.frombuffer(pcm, dtype=np.int16)
                
                # Process with Porcupine
                keyword_index = self.porcupine.process(pcm)
                
                if keyword_index >= 0:
                    self.log(f"🎯 Wake-up word detected!")
                    if self.wake_word_callback:
                        self.wake_word_callback()
                    stream.stop_stream()
                    stream.close()
                    pa.terminate()
                    return True
            
            stream.stop_stream()
            stream.close()
            pa.terminate()
            return False
            
        except Exception as e:
            self.log(f"Error in wake-up word detection: {e}")
            return False
    
    def run(self, input_data: Union[str, bytes]) -> str:
        """
        Transcribe audio input to text or process text input directly.
        
        Args:
            input_data: Audio file path/bytes or text string (for demo fallback)
            
        Returns:
            Transcribed text
        """
        try:
            # If input is already text (demo mode), return it directly
            if isinstance(input_data, str) and not os.path.isfile(input_data):
                self.log(f"Demo mode: Using text input directly: '{input_data}'")
                return input_data
            
            # Handle audio file transcription
            if isinstance(input_data, str) and os.path.isfile(input_data):
                self.log(f"Transcribing audio file: {input_data}")
                with open(input_data, "rb") as audio_file:
                    transcript = self.client.audio.transcriptions.create(
                        model="whisper-1",
                        file=audio_file,
                        language="en"  # Force English transcription
                    )
                transcribed_text = transcript.text
                self.log(f"Transcription result: '{transcribed_text}'")
                return transcribed_text
            
            # Handle raw audio bytes
            elif isinstance(input_data, bytes):
                self.log("Transcribing audio from bytes")
                # For bytes, we'd need to save to a temporary file first
                import tempfile
                with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
                    temp_file.write(input_data)
                    temp_path = temp_file.name
                
                try:
                    with open(temp_path, "rb") as audio_file:
                        transcript = self.client.audio.transcriptions.create(
                            model="whisper-1",
                            file=audio_file,
                            language="en"  # Force English transcription
                        )
                    transcribed_text = transcript.text
                    self.log(f"Transcription result: '{transcribed_text}'")
                    return transcribed_text
                finally:
                    os.unlink(temp_path)
            
            else:
                raise ValueError(f"Unsupported input type: {type(input_data)}")
                
        except Exception as e:
            self.log(f"Error in transcription: {str(e)}")
            # Fallback for demo purposes
            return input_data if isinstance(input_data, str) else "Error in transcription"
    
    def record_and_transcribe(self, duration: int = 5, sample_rate: int = 44100) -> str:
        """
        Record audio from microphone and transcribe it.
        
        Args:
            duration: Recording duration in seconds
            sample_rate: Audio sample rate
            
        Returns:
            Transcribed text
        """
        try:
            self.log(f"🎤 Recording for {duration} seconds... Speak now!")
            print(f"🔴 RECORDING - Speak now for {duration} seconds...")
            
            # Record audio
            audio_data = sd.rec(int(duration * sample_rate), 
                               samplerate=sample_rate, 
                               channels=1, 
                               dtype='float64')
            sd.wait()  # Wait until recording is finished
            print("🟢 Recording finished!")
            
            # Save to temporary file
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
                temp_path = temp_file.name
                wav.write(temp_path, sample_rate, audio_data)
            
            try:
                # Transcribe the recorded audio
                with open(temp_path, "rb") as audio_file:
                    transcript = self.client.audio.transcriptions.create(
                        model="whisper-1",
                        file=audio_file,
                        language="en"  # Force English transcription
                    )
                transcribed_text = transcript.text.strip()
                self.log(f"Transcribed: '{transcribed_text}'")
                return transcribed_text
            finally:
                os.unlink(temp_path)
                
        except Exception as e:
            self.log(f"Error in voice recording: {str(e)}")
            return ""
    
    def get_voice_confirmation(self, prompt: str = "Please respond with yes or no") -> bool:
        """
        Get voice confirmation from user (DEPRECATED - use get_voice_confirmation_auto instead).
        
        Args:
            prompt: Prompt to display to user
            
        Returns:
            True if user confirms, False otherwise
        """
        print(f"\n{prompt}")
        print("🎤 Listening for your response...")
        
        response = self.record_and_transcribe(duration=3)
        
        if not response:
            self.log("No voice input detected")
            return False
        
        affirmative_responses = ['yes', 'y', 'correct', 'ok', 'true', 'yeah', 'yep', 'approve']
        is_confirmed = any(word in response.lower() for word in affirmative_responses)
        
        self.log(f"User response: '{response}' -> {'Confirmed' if is_confirmed else 'Declined'}")
        return is_confirmed
    
    def is_speech(self, audio_frame: bytes) -> bool:
        """
        Check if audio frame contains speech using Voice Activity Detection.
        
        Args:
            audio_frame: Audio frame bytes
            
        Returns:
            True if speech detected, False otherwise
        """
        try:
            return self.vad.is_speech(audio_frame, self.sample_rate)
        except Exception:
            return False
    
    def auto_record_speech(self, max_duration: int = 30) -> str:
        """
        Automatically record speech with voice activity detection.
        Starts recording when speech is detected, stops after silence.
        
        Args:
            max_duration: Maximum recording duration in seconds
            
        Returns:
            Transcribed text
        """
        try:
            print("🎧 Listening... Start speaking when ready!")
            self.log("Starting automatic voice detection...")
            
            # Wait for speech to start
            speech_detected = self._wait_for_speech_start(timeout=60)
            if not speech_detected:
                self.log("No speech detected within timeout")
                return ""
            
            print("🔴 RECORDING - Speak now...")
            self.log("Speech detected, starting recording...")
            
            # Record with automatic stop on silence
            audio_data = self._record_until_silence(max_duration)
            
            if len(audio_data) < self.sample_rate * self.min_speech_duration:
                self.log("Recording too short, ignoring")
                return ""
            
            print("🟢 Recording complete!")
            
            # Save and transcribe
            return self._transcribe_audio_data(audio_data)
            
        except Exception as e:
            self.log(f"Error in auto speech recording: {str(e)}")
            return ""
    
    def _wait_for_speech_start(self, timeout: int = 60) -> bool:
        """
        Wait for speech to start using voice activity detection.
        
        Args:
            timeout: Maximum wait time in seconds
            
        Returns:
            True if speech detected, False if timeout
        """
        start_time = time.time()
        chunk_size = self.frame_size
        
        # Callback to check for speech
        speech_detected = threading.Event()
        
        def audio_callback(indata, frames, time_info, status):
            if status:
                return
                
            # Convert to bytes for VAD
            audio_bytes = (indata[:, 0] * 32767).astype(np.int16).tobytes()
            
            # Check if speech is detected
            if len(audio_bytes) >= self.frame_size * 2:  # 2 bytes per sample
                frame = audio_bytes[:self.frame_size * 2]
                if self.is_speech(frame):
                    speech_detected.set()
        
        # Start listening
        with sd.InputStream(callback=audio_callback, 
                           channels=1, 
                           samplerate=self.sample_rate,
                           blocksize=chunk_size):
            
            while not speech_detected.is_set():
                if time.time() - start_time > timeout:
                    return False
                time.sleep(0.1)
        
        return True
    
    def _record_until_silence(self, max_duration: int) -> np.ndarray:
        """
        Record audio until silence is detected.
        
        Args:
            max_duration: Maximum recording duration
            
        Returns:
            Recorded audio data
        """
        audio_data = []
        silence_start = None
        recording = True
        
        def audio_callback(indata, frames, time_info, status):
            nonlocal silence_start, recording
            
            if not recording:
                return
                
            audio_data.extend(indata[:, 0])
            
            # Convert to bytes for VAD
            audio_bytes = (indata[:, 0] * 32767).astype(np.int16).tobytes()
            
            # Check for speech in this frame
            has_speech = False
            if len(audio_bytes) >= self.frame_size * 2:
                frame = audio_bytes[:self.frame_size * 2]
                has_speech = self.is_speech(frame)
            
            # Track silence
            if has_speech:
                silence_start = None  # Reset silence timer
            else:
                if silence_start is None:
                    silence_start = time.time()
                elif time.time() - silence_start > self.silence_threshold:
                    recording = False  # Stop recording
        
        # Start recording
        start_time = time.time()
        with sd.InputStream(callback=audio_callback,
                           channels=1,
                           samplerate=self.sample_rate,
                           blocksize=self.frame_size):
            
            while recording and (time.time() - start_time) < max_duration:
                time.sleep(0.1)
        
        return np.array(audio_data)
    
    def _transcribe_audio_data(self, audio_data: np.ndarray) -> str:
        """
        Transcribe audio data using OpenAI Whisper.
        
        Args:
            audio_data: Audio data array
            
        Returns:
            Transcribed text
        """
        try:
            # Save to temporary file
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
                temp_path = temp_file.name
                wav.write(temp_path, self.sample_rate, audio_data.astype(np.float32))
            
            try:
                # Transcribe
                with open(temp_path, "rb") as audio_file:
                    transcript = self.client.audio.transcriptions.create(
                        model="whisper-1",
                        file=audio_file,
                        language="en"  # Force English transcription
                    )
                transcribed_text = transcript.text.strip()
                self.log(f"Transcribed: '{transcribed_text}'")
                return transcribed_text
            finally:
                os.unlink(temp_path)
                
        except Exception as e:
            self.log(f"Error transcribing audio: {str(e)}")
            return ""
    
    def get_voice_confirmation_auto(self, prompt: str = "Please respond with yes or no") -> bool:
        """
        Get voice confirmation with automatic detection (no typing fallback).
        
        Args:
            prompt: Prompt to display to user
            
        Returns:
            True if user confirms, False otherwise
        """
        print(f"\n{prompt}")
        print("🎧 Say 'yes' or 'no' when ready...")
        
        response = self.auto_record_speech(max_duration=10)
        
        if not response:
            self.log("No voice input detected")
            return False
        
        affirmative_responses = ['yes', 'y', 'correct', 'ok', 'true', 'yeah', 'yep', 'approve']
        is_confirmed = any(word in response.lower() for word in affirmative_responses)
        
        self.log(f"User response: '{response}' -> {'Confirmed' if is_confirmed else 'Declined'}")
        return is_confirmed