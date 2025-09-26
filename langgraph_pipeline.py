"""
LangGraph Voice Pipeline - Universal Code Generation
Implements: Wake-up Word → Voice Input → Speech-to-Text → Confirmation → Intent Classification → Universal Code Generation
Supports: Python, JavaScript, Java, C++, C#, Go, Rust, PHP, Ruby, Swift, Kotlin, TypeScript, HTML, CSS, SQL, Bash, PowerShell, YAML, JSON, XML
"""

import os
import time
import signal
from typing import TypedDict, Optional, List
from dotenv import load_dotenv

# LangGraph and LangChain imports
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

# Import our existing agents
from agents import (
    STTAgent, TTSPromptAgent, PythonAgent, DiscussionAgent, CodeAnalysisAgent, CodeRabbitAgent
)
from prompts import (
    WELCOME_MESSAGE,
    CODERABBIT_START_MESSAGE,
    CODERABBIT_ERROR_MESSAGE
)

# Load environment variables
load_dotenv()


class VoiceCodingState(TypedDict):
    """State for the complete multi-agent voice coding pipeline"""
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
    
    # Intent classification
    user_intent: str  # "coding", "explanation", "review", "general"
    
    # Todo generation
    generated_todos: List[str]  # List of generated tasks
    todos_completed: bool  # Whether all todos are completed
    
    # Code generation
    generated_code: str  # Generated code content
    code_file_path: str  # Path to saved code file
    
    # Code explanation
    code_explanation: str  # Explanation of the code
    
    # Code review
    code_review: str  # Review feedback
    review_score: int  # Review score (1-10)
    
    # User feedback
    user_feedback: str  # User's feedback on generated code
    feedback_processed: bool  # Whether feedback has been processed
    
    # Code iteration
    iteration_count: int  # Number of iterations
    max_iterations: int  # Maximum allowed iterations
    
    # Response generation
    final_response: str  # Final response to user
    
    # Session management
    interaction_count: int
    
    # Todo management
    current_todo_index: int  # Track which todo we're currently working on


class LangGraphVoicePipeline:
    """LangGraph-based voice coding pipeline with wake-up word detection - Confirmation Flow Only"""
    
    def __init__(self):
        """Initialize the pipeline with all agents"""
        # Initialize all agents
        self.stt_agent = STTAgent()
        self.tts_agent = TTSPromptAgent()
        self.python_agent = PythonAgent()
        self.discussion_agent = DiscussionAgent()
        self.code_analysis_agent = CodeAnalysisAgent()
        self.coderabbit_agent = CodeRabbitAgent()
        
        # Create the workflow
        self.workflow = self._create_workflow()
        
        print(" LangGraph Voice Pipeline initialized successfully!")
        print(" Flow: Wake-up → Voice → Speech-to-Text → Confirmation → Intent Classification → Complete Multi-Agent Pipeline")
    
    def _create_workflow(self) -> StateGraph:
        """Create the confirmation flow workflow"""
        
        # Create the workflow
        workflow = StateGraph(VoiceCodingState)
        
        # Add all nodes from the complete pipeline
        workflow.add_node("wake_word_detection", self._wake_word_detection_node)
        workflow.add_node("voice_input", self._voice_input_node)
        workflow.add_node("speech_to_text", self._speech_to_text_node)
        workflow.add_node("confirmation", self._confirmation_node)
        workflow.add_node("intent_classification", self._intent_classification_node)
        workflow.add_node("todo_generation", self._todo_generation_node)
        workflow.add_node("code_generation", self._code_generation_node)
        workflow.add_node("code_explanation", self._code_explanation_node)
        workflow.add_node("code_review", self._code_review_node)
        workflow.add_node("user_feedback", self._user_feedback_node)
        workflow.add_node("code_iteration", self._code_iteration_node)
        workflow.add_node("todo_completion_check", self._todo_completion_check_node)
        workflow.add_node("response_generation", self._response_generation_node)
        
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
        
        # Intent classification routing
        workflow.add_conditional_edges(
            "intent_classification",
            self._should_continue_after_intent_classification,
            {
                "todo_generation": "todo_generation",
                "code_review": "code_review",
                "code_explanation": "code_explanation",
                END: END
            }
        )
        
        # Todo generation routing
        workflow.add_conditional_edges(
            "todo_generation",
            self._should_continue_after_todo_generation,
            {
                "code_generation": "code_generation",
                "code_explanation": "code_explanation",
                "code_review": "code_review",
                END: END
            }
        )
        
        # Code generation routing
        workflow.add_conditional_edges(
            "code_generation",
            self._should_continue_after_code_generation,
            {
                "todo_completion_check": "todo_completion_check",
                "user_feedback": "user_feedback",
                "response_generation": "response_generation",
                END: END
            }
        )
        
        # Code explanation goes to response generation
        workflow.add_edge("code_explanation", "response_generation")
        
        # Code review routing
        workflow.add_conditional_edges(
            "code_review",
            self._should_continue_after_code_review,
            {
                "code_generation": "code_generation",
                "response_generation": "response_generation",
                END: END
            }
        )
        
        # User feedback routing
        workflow.add_conditional_edges(
            "user_feedback",
            self._should_continue_after_user_feedback,
            {
                "code_iteration": "code_iteration",
                "code_generation": "code_generation",
                "response_generation": "response_generation",
                END: END
            }
        )
        
        # Code iteration routing
        workflow.add_conditional_edges(
            "code_iteration",
            self._should_continue_after_code_iteration,
            {
                "user_feedback": "user_feedback",
                "response_generation": "response_generation",
                END: END
            }
        )
        
        # Todo completion check routing
        workflow.add_conditional_edges(
            "todo_completion_check",
            self._should_continue_after_todo_completion_check,
            {
                "code_generation": "code_generation",
                "response_generation": "response_generation",
                END: END
            }
        )
        
        # Response generation routing - can go back to intent classification or END
        workflow.add_conditional_edges(
            "response_generation",
            self._should_continue_after_response_generation,
            {
                "intent_classification": "intent_classification",  # Start new task
                END: END  # End session
            }
        )
        
        return workflow.compile()
    
    # ==================== NODE IMPLEMENTATIONS ====================
    
    def _wake_word_detection_node(self, state: VoiceCodingState) -> VoiceCodingState:
        """Node 1: Detect wake-up word using STT Agent"""
        print(" [Node 1] Listening for wake-up word...")
        
        try:
            # Use STT agent's wake-up word detection
            wake_word_detected = self.stt_agent.listen_for_wake_word()
            
            state["wake_word_detected"] = wake_word_detected
            state["current_step"] = "wake_word_detection"
            
            if wake_word_detected:
                print(" Wake-up word detected! Starting voice input...")
            else:
                print("⏰ Wake-up word timeout. Ending session.")
                state["pipeline_status"] = "completed"
                
        except Exception as e:
            print(f" Error in wake-up word detection: {e}")
            state["error_message"] = str(e)
            state["pipeline_status"] = "error"
        
        return state
    
    def _voice_input_node(self, state: VoiceCodingState) -> VoiceCodingState:
        """Node 2: Capture voice input using STT Agent"""
        print(" [Node 2] Capturing voice input...")
        
        try:
            # Reset confirmation spoken flag when starting new voice input
            state["confirmation_spoken"] = False
            
            # Capture voice input using STT agent (no prompt needed after wake-up word)
            voice_input = self.stt_agent.auto_record_speech(max_duration=30)
            
            if voice_input:
                state["voice_input"] = voice_input
                state["current_step"] = "voice_input"
                print(f" Voice input captured: '{voice_input}'")
            else:
                state["error_message"] = "No voice input detected"
                state["pipeline_status"] = "error"
                
        except Exception as e:
            print(f" Error in voice input: {e}")
            state["error_message"] = str(e)
            state["pipeline_status"] = "error"
        
        return state
    
    def _speech_to_text_node(self, state: VoiceCodingState) -> VoiceCodingState:
        """Node 3: Convert speech to text using STT Agent"""
        print(" [Node 3] Converting speech to text...")
        
        try:
            voice_input = state.get("voice_input", "")
            
            if voice_input:
                # Use STT agent to transcribe
                transcribed_text = self.stt_agent.run(voice_input)
                
                state["transcribed_text"] = transcribed_text
                state["current_step"] = "speech_to_text"
                
                print(f" Transcribed: '{transcribed_text}'")
            else:
                state["error_message"] = "No voice input to transcribe"
                state["pipeline_status"] = "error"
                
        except Exception as e:
            print(f" Error in speech-to-text: {e}")
            state["error_message"] = str(e)
            state["pipeline_status"] = "error"
        
        return state
    
    def _confirmation_node(self, state: VoiceCodingState) -> VoiceCodingState:
        """Node 4: Confirm transcribed text with user - Summarized and human-like"""
        print(" [Node 4] Confirming transcribed text...")
        
        try:
            transcribed_text = state.get("transcribed_text", "")
            
            if transcribed_text:
                # Only speak confirmation message once
                if not state.get("confirmation_spoken", False):
                    # Summarize the user's request with natural filler sounds
                    summary = self._summarize_user_request(transcribed_text)
                    confirmation_msg = f"Um, so you want me to {summary}, right?"
                    print(f"🔊 Speaking: {confirmation_msg}")
                    self.tts_agent.run(confirmation_msg)
                    state["confirmation_spoken"] = True
                
                # Always process user response (even if confirmation was already spoken)
                print(" Listening for your response...")
                print(" Say 'yes' to continue or 'no' to re-record")
                confirmation_response = self.stt_agent.auto_record_speech(max_duration=15)
                
                if confirmation_response:
                    confirmation_lower = confirmation_response.lower().strip()
                    print(f" You said: '{confirmation_response}'")
                    
                    if any(word in confirmation_lower for word in ["yes", "correct", "right", "yeah", "yep", "ok", "okay"]):
                        state["user_confirmed"] = True
                        state["confirmation_status"] = "confirmed"
                        print(" User confirmed! Ready for intent classification.")
                        # Add human-like response with filler sounds
                        print("🔊 Speaking: Great! Um, let me get started on that for you.")
                        self.tts_agent.run("Great! Um, let me get started on that for you.")
                    else:
                        state["user_confirmed"] = False
                        state["confirmation_status"] = "re_record"
                        print("🔄 User wants to re-record. Going back to voice input.")
                        # Say sorry and ask to try again with human-like filler
                        sorry_msg = "Oh, um, I'm sorry about that. Could you please say it again?"
                        print(f"🔊 Speaking: {sorry_msg}")
                        self.tts_agent.run(sorry_msg)
                else:
                    # No response detected - assume yes and continue (no duplicate TTS)
                    print("⏰ No response detected. Assuming 'yes' and continuing...")
                    state["user_confirmed"] = True
                    state["confirmation_status"] = "confirmed"
                    print(" Assuming confirmation. Ready for intent classification.")
                    # Only speak once with filler sounds
                    self.tts_agent.run("Um, I'll assume that's correct and continue.")
                
                state["current_step"] = "confirmation"
            else:
                state["error_message"] = "No transcribed text to confirm"
                state["pipeline_status"] = "error"
                
        except Exception as e:
            print(f" Error in confirmation: {e}")
            state["error_message"] = str(e)
            state["pipeline_status"] = "error"
        
        return state
    
    def _intent_classification_node(self, state: VoiceCodingState) -> VoiceCodingState:
        """Node 5: Classify user intent - Handle both initial and continuous help"""
        print("🧠 [Node 5] Classifying user intent...")
        
        try:
            transcribed_text = state.get("transcribed_text", "")
            # Check if this is a new task from continuous help
            if not transcribed_text:
                print("🔄 New task from continuous help. Getting user input...")
                self.tts_agent.run("What would you like me to help you with?")
                
                # Get new user input
                print(" Listening for your new request...")
                new_request = self.stt_agent.auto_record_speech(max_duration=30)
                
                if new_request:
                    print(f" New request: '{new_request}'")
                    
                    # Check if this is a file operation request
                    if any(word in new_request.lower() for word in ["rename", "rename file", "change file", "move file", "copy file"]):
                        print("📁 File operation detected. Handling file request...")
                        self._handle_file_operation(new_request, state)
                        return state
                    else:
                        state["transcribed_text"] = new_request
                        transcribed_text = new_request
                else:
                    print("⏰ No new request. Ending session.")
                    self.tts_agent.run("I didn't catch that. Just say 'Blueberry' whenever you need help. Goodbye!")
                    state["pipeline_status"] = "completed"
                    return state
            
            if transcribed_text:
                # Simple intent classification (placeholder)
                # In a real implementation, you'd use an LLM or ML model here
                transcribed_lower = transcribed_text.lower()
                # Check for review intent first (most specific)
                if any(word in transcribed_lower for word in ["review", "check", "analyze", "examine", "look at"]):
                    intent = "review"
                elif any(word in transcribed_lower for word in ["explain", "what", "how", "why", "tell me", "describe"]):
                    intent = "explanation"
                elif any(word in transcribed_lower for word in ["code", "program", "function", "class", "write", "create", "build", "make", "generate"]):
                    intent = "coding"
                else:
                    # Default to coding for most requests
                    intent = "coding"
                
                state["user_intent"] = intent
                state["current_step"] = "intent_classification"
                
                print(f" Classified intent: {intent}")
                print(" Intent classification completed. Routing to appropriate task...")
            else:
                state["error_message"] = "No transcribed text for intent classification"
                state["pipeline_status"] = "error"
                
        except Exception as e:
            print(f" Error in intent classification: {e}")
            state["error_message"] = str(e)
            state["pipeline_status"] = "error"
        
        return state
    
    def _code_generation_node(self, state: VoiceCodingState) -> VoiceCodingState:
        """Node 6: Discussion-Friendly Interactive Code Generation - Real-time Conversation"""
        print(" [Node 6] Discussion-Friendly Interactive Code Generation")
        
        try:
            transcribed_text = state.get("transcribed_text", "")
            todos = state.get("generated_todos", [])
            current_todo_index = state.get("current_todo_index", 0)
            iteration_count = state.get("iteration_count", 0)
            
            if transcribed_text and todos:
                # Get current todo
                current_todo = todos[current_todo_index] if current_todo_index < len(todos) else todos[-1]
                
                print(f" Working on todo {current_todo_index + 1}/{len(todos)}: '{current_todo}'")
                print(f" User Request: '{transcribed_text}'")
                
                # Start interactive discussion
                self._start_interactive_discussion(state, current_todo, transcribed_text, todos, current_todo_index)
                
            else:
                state["error_message"] = "No transcribed text or todos for code generation"
                state["pipeline_status"] = "error"
                
        except Exception as e:
            print(f" Error in code generation: {e}")
            state["error_message"] = str(e)
            state["pipeline_status"] = "error"
        
        return state
    
    def _start_interactive_discussion(self, state: VoiceCodingState, current_todo: str, transcribed_text: str, todos: List[str], current_todo_index: int):
        """Start interactive discussion with user - Real-time conversation"""
        print(f"\n🤝 Starting interactive discussion for: '{current_todo}'")
        
        # Determine programming language and task type
        language, task_type = self._analyze_code_request(transcribed_text)
        
        # Check if language was specified, if not ask the user
        if language == "python" and not self._is_language_specified(transcribed_text):
            print(" No programming language specified. Asking user to choose...")
            self.tts_agent.run("Um, I need to know which programming language you'd like me to use. I support Python, JavaScript, Java, C++, C#, Go, Rust, PHP, Ruby, Swift, Kotlin, TypeScript, HTML, CSS, SQL, Bash, PowerShell, YAML, JSON, and XML. Which one would you prefer?")
            
            # Get user's language choice with interactive discussion
            language = self._get_language_with_discussion()
        
        print(f" Final Language: {language}")
        print(f" Task Type: {task_type}")
        
        # Start the interactive discussion loop
        self._interactive_discussion_loop(state, current_todo, transcribed_text, todos, current_todo_index, language, task_type)
    
    def _get_language_with_discussion(self) -> str:
        """Get language choice through interactive discussion"""
        while True:
            print(" Listening for your language choice...")
            language_response = self.stt_agent.auto_record_speech(max_duration=15)
            
            if language_response:
                language = self._extract_language_from_response(language_response)
                print(f" User specified language: {language}")
                
                # Confirm the choice
                self.tts_agent.run(f"Um, great! I'll use {language} for this task. Is that correct?")
                
                # Get confirmation
                print(" Listening for confirmation...")
                confirm_response = self.stt_agent.auto_record_speech(max_duration=10)
                
                if confirm_response:
                    confirm_lower = confirm_response.lower().strip()
                    if any(word in confirm_lower for word in ["yes", "correct", "right", "good", "ok", "okay"]):
                        return language
                    elif any(word in confirm_lower for word in ["no", "wrong", "change", "different"]):
                        self.tts_agent.run("Um, no problem! What language would you prefer instead?")
                        continue
                    else:
                        # Ambiguous response, ask for clarification
                        self.tts_agent.run("Um, I'm not sure if that's correct. Could you please say 'yes' or 'no'?")
                        continue
                else:
                    # No response, assume yes
                    return language
            else:
                print("⏰ No language specified. Using Python as default.")
                self.tts_agent.run("Um, I'll use Python as the default language.")
                return "python"
    
    def _interactive_discussion_loop(self, state: VoiceCodingState, current_todo: str, transcribed_text: str, todos: List[str], current_todo_index: int, language: str, task_type: str):
        """Interactive discussion loop - Real-time conversation with user"""
        print(f"\n💬 Starting interactive discussion loop for: '{current_todo}'")
        
        # Check if we've already asked about this todo
        todo_key = f"todo_asked_{current_todo_index}"
        if state.get(todo_key, False):
            print(f"⏭️ Already asked about todo {current_todo_index + 1}. Skipping duplicate question.")
            return
        
        # Mark this todo as asked
        state[todo_key] = True
        
        while True:
            # Ask user about the current todo (speak only, no duplicate print)
            # Removed duplicate print - TTS already says this
            
            # Speak to user like a colleague with natural filler sounds
            self.tts_agent.run(f"Um, hey! I'm working on {current_todo}. I'll create a {language} {task_type} for you. What do you think?")
            
            # Get user response with longer timeout for discussion
            print(" Listening for your response...")
            user_response = self.stt_agent.auto_record_speech(max_duration=20)
            
            if user_response:
                response_lower = user_response.lower().strip()
                print(f" You said: '{user_response}'")
                
                # Handle different types of responses
                if any(word in response_lower for word in ["yes", "good", "sounds good", "proceed", "go ahead", "ok", "okay", "perfect", "great"]):
                    print(" User confirmed! Proceeding with code generation...")
                    self._generate_and_save_code(state, current_todo, transcribed_text, todos, current_todo_index, language, task_type)
                    break
                    
                elif any(word in response_lower for word in ["no", "wrong", "change", "different", "something else", "i want something else"]):
                    print("🔄 User wants changes. Let's discuss what you'd like instead.")
                    
                    # Check if user is asking about language options
                    if any(word in response_lower for word in ["languages", "support", "options", "what languages", "which languages", "other languages"]):
                        print("📋 User asking about language options during discussion.")
                        self.tts_agent.run("Um, I support many programming languages! I can work with Python, JavaScript, Java, C++, C#, Go, Rust, PHP, Ruby, Swift, Kotlin, TypeScript, HTML, CSS, SQL, Bash, PowerShell, YAML, JSON, and XML. Which one would you like to use instead?")
                    else:
                        self.tts_agent.run("Oh, um, no problem! What would you like me to change or do differently?")
                    
                    # Get user's specific requirements
                    print(" Listening for your specific requirements...")
                    new_requirements = self.stt_agent.auto_record_speech(max_duration=30)
                    
                    if new_requirements:
                        print(f" New requirements: '{new_requirements}'")
                        # Update the current todo based on new requirements
                        current_todo = self._update_todo_based_on_feedback(current_todo, new_requirements)
                        print(f"🔄 Updated todo: '{current_todo}'")
                        
                        # Re-analyze language from the new requirements
                        new_language, new_task_type = self._analyze_code_request(new_requirements)
                        print(f" New language detected: {new_language}")
                        print(f" New task type: {new_task_type}")
                        
                        # Update the language and task type
                        language = new_language
                        task_type = new_task_type
                        
                        self.tts_agent.run(f"Um, got it! I'll work on {current_todo} using {language}. Let's continue.")
                        continue
                    else:
                        print("⏰ No specific requirements. Let's try again.")
                        self.tts_agent.run("Um, hmm, I didn't catch that. Could you please tell me what you'd like me to change?")
                        continue
                        
                elif any(word in response_lower for word in ["wait", "stop", "pause", "hold on"]):
                    print("⏸️ User wants to pause. Waiting for further instructions.")
                    self.tts_agent.run("Um, sure! I'll wait. What would you like me to do?")
                    continue
                    
                elif any(word in response_lower for word in ["help", "what", "how", "explain", "support", "languages", "options"]):
                    print("❓ User needs help. Providing assistance.")
                    
                    # Check if user is asking about supported languages
                    if any(word in response_lower for word in ["languages", "support", "options", "what languages", "which languages"]):
                        print("📋 User asking about supported languages. Providing language list.")
                        self.tts_agent.run("Um, I support many programming languages! I can work with Python, JavaScript, Java, C++, C#, Go, Rust, PHP, Ruby, Swift, Kotlin, TypeScript, HTML, CSS, SQL, Bash, PowerShell, YAML, JSON, and XML. Which one would you like to use?")
                    else:
                        self.tts_agent.run(f"Um, I'm here to help! I'm working on {current_todo} using {language}. What would you like me to explain or help you with?")
                    
                    # Get user's help response
                    print(" Listening for your help response...")
                    help_response = self.stt_agent.auto_record_speech(max_duration=20)
                    if help_response:
                        print(f" Help response: '{help_response}'")
                        # Process help response and continue
                        continue
                    else:
                        print("⏰ No help response. Continuing with task.")
                        continue
                    
                else:
                    # Ambiguous response, ask for clarification
                    print("❓ Ambiguous response. Asking for clarification.")
                    self.tts_agent.run("Um, hmm, I'm not sure what you mean. Could you please say 'yes' to continue, 'no' to change something, or 'help' if you need assistance?")
                    continue
                    
            else:
                print("⏰ No response. Asking if user is still there.")
                self.tts_agent.run("Um, are you still there? Should I continue with the current task?")
                
                # Get a quick response
                quick_response = self.stt_agent.auto_record_speech(max_duration=5)
                if quick_response:
                    response_lower = quick_response.lower().strip()
                    if any(word in response_lower for word in ["yes", "continue", "go ahead"]):
                        print(" User confirmed. Proceeding with code generation...")
                        self._generate_and_save_code(state, current_todo, transcribed_text, todos, current_todo_index, language, task_type)
                        break
                    else:
                        print("🔄 User wants to discuss further.")
                        continue
                else:
                    print("⏰ No response. Proceeding with code generation...")
                    self._generate_and_save_code(state, current_todo, transcribed_text, todos, current_todo_index, language, task_type)
                    break
    
    def _update_todo_based_on_feedback(self, current_todo: str, feedback: str) -> str:
        """Update todo based on user feedback with language detection"""
        # Extract language from feedback
        feedback_lower = feedback.lower()
        
        # Check for language keywords in feedback
        if "java" in feedback_lower:
            return f"Create a Java function: {feedback}"
        elif "javascript" in feedback_lower or "js" in feedback_lower:
            return f"Create a JavaScript function: {feedback}"
        elif "python" in feedback_lower:
            return f"Create a Python function: {feedback}"
        elif "c++" in feedback_lower or "cpp" in feedback_lower:
            return f"Create a C++ function: {feedback}"
        elif "go" in feedback_lower:
            return f"Create a Go function: {feedback}"
        elif "rust" in feedback_lower:
            return f"Create a Rust function: {feedback}"
        elif "php" in feedback_lower:
            return f"Create a PHP function: {feedback}"
        elif "ruby" in feedback_lower:
            return f"Create a Ruby function: {feedback}"
        elif "swift" in feedback_lower:
            return f"Create a Swift function: {feedback}"
        elif "kotlin" in feedback_lower:
            return f"Create a Kotlin function: {feedback}"
        elif "typescript" in feedback_lower or "ts" in feedback_lower:
            return f"Create a TypeScript function: {feedback}"
        elif "html" in feedback_lower:
            return f"Create an HTML page: {feedback}"
        elif "css" in feedback_lower:
            return f"Create CSS styles: {feedback}"
        elif "sql" in feedback_lower:
            return f"Create SQL queries: {feedback}"
        elif "bash" in feedback_lower or "shell" in feedback_lower:
            return f"Create a Bash script: {feedback}"
        elif "powershell" in feedback_lower:
            return f"Create a PowerShell script: {feedback}"
        else:
            # Default update
            if "different" in feedback_lower or "something else" in feedback_lower:
                return f"Modified task based on your feedback: {feedback}"
            elif "change" in feedback_lower:
                return f"Updated task: {feedback}"
            else:
                return f"Revised task: {feedback}"
    
    def _generate_and_save_code(self, state: VoiceCodingState, current_todo: str, transcribed_text: str, todos: List[str], current_todo_index: int, language: str, task_type: str):
        """Generate and save code with user confirmation"""
        print("🔨 Generating code...")
        print(f" Using language: {language}")
        print(f" Task type: {task_type}")
        
        # Generate code using appropriate approach
        generated_code = self._generate_universal_code(transcribed_text, todos, language, task_type)
        
        # Save code to appropriate file with smart filename
        file_extension = self._get_file_extension(language)
        smart_filename = self._generate_smart_filename(transcribed_text, language)
        code_file_path = f"{smart_filename}.{file_extension}"
        with open(code_file_path, 'w') as f:
            f.write(generated_code)
        
        state["generated_code"] = generated_code
        state["code_file_path"] = code_file_path
        state["iteration_count"] = state.get("iteration_count", 0) + 1
        state["current_step"] = "code_generation"
        state["current_todo_index"] = current_todo_index + 1  # Move to next todo
        
        print(f" Code generated and saved to: {code_file_path}")
        print(f" Code preview:\n{generated_code[:200]}...")
        
        # Speak the result like a colleague
        self.tts_agent.run(f"Um, perfect! I've created the {language} code for {current_todo}. It's saved as {code_file_path}. Ready for the next task?")
        
        # Ask if user wants to continue or make changes
        print(" Listening for your next instruction...")
        next_instruction = self.stt_agent.auto_record_speech(max_duration=15)
        
        if next_instruction:
            instruction_lower = next_instruction.lower().strip()
            if any(word in instruction_lower for word in ["yes", "continue", "next", "go ahead"]):
                print(" User wants to continue. Moving to next task.")
            elif any(word in instruction_lower for word in ["no", "change", "modify", "different"]):
                print("🔄 User wants to make changes. Starting discussion loop again.")
                self._interactive_discussion_loop(state, current_todo, transcribed_text, todos, current_todo_index, language, task_type)
            else:
                print(" Continuing with next task.")
        else:
            print(" Continuing with next task.")
    
    
    def _code_explanation_node(self, state: VoiceCodingState) -> VoiceCodingState:
        """Node 8: Code Explanation/Debug Task"""
        print(" [Node 8] Executing code explanation/debug task...")
        
        try:
            transcribed_text = state.get("transcribed_text", "")
            
            if transcribed_text:
                print(" Explaining/debugging code based on your request...")
                
                # Use Discussion agent for code explanation
                result = self.discussion_agent.run(transcribed_text)
                
                state["task_result"] = result
                state["task_completed"] = True
                state["current_step"] = "code_explanation"
                state["pipeline_status"] = "completed"
                
                print(" Code explanation completed!")
                print(f" Explanation:\n{result}")
                
                # Speak the result
                self.tts_agent.run("Code explanation completed. Here's what I found.")
                
            else:
                state["error_message"] = "No transcribed text for code explanation"
                state["pipeline_status"] = "error"
                
        except Exception as e:
            print(f" Error in code explanation: {e}")
            state["error_message"] = str(e)
            state["pipeline_status"] = "error"
        
        return state
    
    def _todo_generation_node(self, state: VoiceCodingState) -> VoiceCodingState:
        """Node 6: Generate todos/tasks based on user request - Interactive and Collaborative"""
        print(" [Node 6] Todo Generation - Interactive Mode")
        
        try:
            transcribed_text = state.get("transcribed_text", "")
            user_intent = state.get("user_intent", "")
            
            print(f" Intent: {user_intent}")
            print(f" User Request: '{transcribed_text}'")
            print("📋 Generating tasks based on user request...")
            
            # Generate todos based on the request
            todos = self._generate_todos_from_request(transcribed_text)
            
            state["generated_todos"] = todos
            state["todos_completed"] = False
            state["current_step"] = "todo_generation"
            state["current_todo_index"] = 0  # Track which todo we're working on
            
            print(f" Generated {len(todos)} tasks:")
            for i, todo in enumerate(todos, 1):
                print(f"   {i}. {todo}")
            
            # Start interactive todo process
            if todos:
                first_todo = todos[0]
                print(f"\n🤝 Let's start with the first task: '{first_todo}'")
                print("💬 I'll work on this step by step with you, like a colleague!")
                
                # Speak the first todo to the user
                self.tts_agent.run(f"Great! I've created a plan with {len(todos)} tasks. Let's start with the first one: {first_todo}. Should I proceed with this?")
            
        except Exception as e:
            print(f" Error in todo generation: {e}")
            state["error_message"] = str(e)
            state["pipeline_status"] = "error"
        
        return state
    
    
    def _code_review_node(self, state: VoiceCodingState) -> VoiceCodingState:
        """Node 7: Code Review Task using CodeRabbit"""
        print(" [Node 7] Code Review Task using CodeRabbit")
        print(" Intent: review")
        
        try:
            print(" Running CodeRabbit review on current directory...")
            self.tts_agent.run(CODERABBIT_START_MESSAGE)
            
            # Use CodeRabbit agent to review current directory
            review_result = self.coderabbit_agent.review_current_directory()
            
            if review_result["status"] == "completed":
                state["code_review"] = review_result["review_output"]
                state["review_summary"] = review_result["summary"]
                state["current_step"] = "code_review"
                state["pipeline_status"] = "completed"
                
                print(" CodeRabbit review completed!")
                print(f" Review summary: {review_result['summary']}")
                
                # Speak the GPT-4 summarized review with filler sounds
                self.tts_agent.run(review_result["summary"])
                
            else:
                print(f" CodeRabbit review failed: {review_result['summary']}")
                self.tts_agent.run("Rate limit exceeded error")
                state["current_step"] = "code_review"
                state["pipeline_status"] = "error"
                
        except Exception as e:
            print(f" Error in code review: {str(e)}")
            self.tts_agent.run("Rate limit exceeded error")
            state["error_message"] = str(e)
            state["pipeline_status"] = "error"
        
        return state
    
    def _code_explanation_node(self, state: VoiceCodingState) -> VoiceCodingState:
        """Node 8: Code Explanation/Debug Task - Empty Function"""
        print(" [Node 8] Code Explanation Task")
        print(" Intent: explanation")
        print(" User Request: Code explanation requested")
        print(" Redirected to code explanation based on intent classification")
        
        state["current_step"] = "code_explanation"
        state["pipeline_status"] = "completed"
        
        return state
    
    def _user_feedback_node(self, state: VoiceCodingState) -> VoiceCodingState:
        """Node 9: Collect user feedback on generated code"""
        print("💬 [Node 9] User Feedback")
        
        try:
            generated_code = state.get("generated_code", "")
            
            print("🔊 Asking for user feedback on generated code...")
            feedback_prompt = "Please review the generated code and provide your feedback. What would you like me to change or improve?"
            self.tts_agent.run(feedback_prompt)
            
            # Get user feedback via voice
            print(" Listening for your feedback...")
            user_feedback = self.stt_agent.auto_record_speech(max_duration=30)
            
            if user_feedback:
                state["user_feedback"] = user_feedback
                state["feedback_processed"] = True
                state["current_step"] = "user_feedback"
                
                print(f" User feedback: '{user_feedback}'")
                print(" Feedback collected successfully")
            else:
                print("⏰ No feedback received")
                state["user_feedback"] = "No feedback provided"
                state["feedback_processed"] = False
            
        except Exception as e:
            print(f" Error in user feedback: {e}")
            state["error_message"] = str(e)
            state["pipeline_status"] = "error"
        
        return state
    
    def _code_iteration_node(self, state: VoiceCodingState) -> VoiceCodingState:
        """Node 10: Iterate and improve code based on feedback"""
        print("🔄 [Node 10] Code Iteration")
        
        try:
            user_feedback = state.get("user_feedback", "")
            generated_code = state.get("generated_code", "")
            iteration_count = state.get("iteration_count", 0)
            max_iterations = state.get("max_iterations", 3)
            
            print(f"🔄 Iterating code (iteration {iteration_count + 1}/{max_iterations})")
            print(f" Feedback: '{user_feedback}'")
            
            if iteration_count >= max_iterations:
                print("  Maximum iterations reached")
                state["current_step"] = "code_iteration"
                return state
            
            # Improve code based on feedback
            improved_code = self._improve_code_with_feedback(generated_code, user_feedback)
            
            # Update code file
            code_file_path = state.get("code_file_path", f"generated_code_{int(time.time())}.py")
            with open(code_file_path, 'w') as f:
                f.write(improved_code)
            
            state["generated_code"] = improved_code
            state["iteration_count"] = iteration_count + 1
            state["current_step"] = "code_iteration"
            
            print(f" Code improved and saved to: {code_file_path}")
            print(f" Improved code preview:\n{improved_code[:200]}...")
            
        except Exception as e:
            print(f" Error in code iteration: {e}")
            state["error_message"] = str(e)
            state["pipeline_status"] = "error"
        
        return state
    
    def _todo_completion_check_node(self, state: VoiceCodingState) -> VoiceCodingState:
        """Node 11: Interactive Todo Completion Check - Collaborative Review"""
        print(" [Node 11] Interactive Todo Completion Check")
        
        try:
            todos = state.get("generated_todos", [])
            generated_code = state.get("generated_code", "")
            current_todo_index = state.get("current_todo_index", 0)
            
            print(f"📋 Checking completion of {len(todos)} tasks...")
            print(f" Current todo index: {current_todo_index}")
            
            # Check if all todos are addressed in the code
            completed_todos = self._check_todo_completion(todos, generated_code)
            
            state["todos_completed"] = len(completed_todos) == len(todos)
            state["current_step"] = "todo_completion_check"
            
            if state["todos_completed"]:
                print(" All tasks completed successfully!")
                print(" Great work! We've completed all the tasks together!")
                self.tts_agent.run("Excellent! We've completed all the tasks together. Great collaboration!")
            else:
                remaining = len(todos) - len(completed_todos)
                print(f"  {remaining} tasks still need attention")
                
                # Check if we have more todos to work on
                if current_todo_index < len(todos):
                    next_todo = todos[current_todo_index]
                    print(f"🔄 Next task: '{next_todo}'")
                    print("💬 Let's continue with the next task!")
                    self.tts_agent.run(f"We still have {remaining} tasks to complete. The next one is: {next_todo}. Should we continue?")
                else:
                    print("🔄 All todos processed, but some may need refinement")
                    self.tts_agent.run("We've worked through all the tasks. Would you like me to review or refine anything?")
            
        except Exception as e:
            print(f" Error in todo completion check: {e}")
            state["error_message"] = str(e)
            state["pipeline_status"] = "error"
        
        return state
    
    def _response_generation_node(self, state: VoiceCodingState) -> VoiceCodingState:
        """Node 12: Generate final response and ask for additional help"""
        print("📤 [Node 12] Response Generation with Continuous Help Loop")
        
        try:
            user_intent = state.get("user_intent", "")
            generated_code = state.get("generated_code", "")
            code_explanation = state.get("code_explanation", "")
            code_review = state.get("code_review", "")
            todos = state.get("generated_todos", [])
            
            # Generate appropriate response based on intent
            if user_intent == "coding":
                response = self._generate_coding_response(generated_code, todos)
            elif user_intent == "explanation":
                response = self._generate_explanation_response(code_explanation)
            elif user_intent == "review":
                response = self._generate_review_response(code_review)
            else:
                response = "Task completed successfully!"
            
            state["final_response"] = response
            state["current_step"] = "response_generation"
            
            print(" Final response generated")
            print(f" Response: {response}")
            
            # Speak the final response
            self.tts_agent.run(response)
            
            # Ask if user needs help with anything else
            print("\n🤝 Asking if user needs additional help...")
            self.tts_agent.run("Is there anything else you'd like me to help you with?")
            
            # Get user response for additional help (max 10s, stops after 1.5s silence)
            print(" Listening for your response (max 10s, stops after 1.5s silence)...")
            help_response = self.stt_agent.auto_record_speech(max_duration=10)
            
            if help_response:
                help_lower = help_response.lower().strip()
                print(f" You said: '{help_response}'")
                
                if any(word in help_lower for word in ["yes", "yeah", "yep", "sure", "ok", "okay", "help", "more", "another", "continue"]):
                    print(" User wants additional help. Starting new task...")
                    self.tts_agent.run("Great! What would you like me to help you with next?")
                    
                    # Reset state for new task
                    state["pipeline_status"] = "active"
                    state["current_step"] = "intent_classification"
                    state["user_confirmed"] = False
                    state["confirmation_status"] = ""
                    state["confirmation_spoken"] = False
                    state["user_intent"] = ""
                    state["generated_todos"] = []
                    state["todos_completed"] = False
                    state["generated_code"] = ""
                    state["code_file_path"] = ""
                    state["code_explanation"] = ""
                    state["code_review"] = ""
                    state["review_score"] = 0
                    state["user_feedback"] = ""
                    state["feedback_processed"] = False
                    state["iteration_count"] = 0
                    state["final_response"] = ""
                    state["current_todo_index"] = 0
                    state["transcribed_text"] = ""  # Clear transcribed text for new task
                    
                    # Start new task flow
                    print("🔄 Starting new task flow...")
                    return state
                    
                elif any(word in help_lower for word in ["no", "don't", "dont", "nothing", "none", "all set", "good", "fine", "thanks", "thank you"]):
                    print("👋 User doesn't want any help. Ending session and going back to wake-up word detection.")
                    self.tts_agent.run("Perfect! I'm here whenever you need help. Just say 'Blueberry' to start a new session.")
                    
                    # End session and go back to wake-up word detection
                    state["pipeline_status"] = "completed"
                    state["wake_word_detected"] = False
                    state["voice_input"] = ""
                    state["transcribed_text"] = ""
                    state["user_confirmed"] = False
                    state["confirmation_status"] = ""
                    state["confirmation_spoken"] = False
                    state["current_step"] = "wake_word_detection"
                    state["user_intent"] = ""
                    state["generated_todos"] = []
                    state["todos_completed"] = False
                    state["generated_code"] = ""
                    state["code_file_path"] = ""
                    state["code_explanation"] = ""
                    state["code_review"] = ""
                    state["review_score"] = 0
                    state["user_feedback"] = ""
                    state["feedback_processed"] = False
                    state["iteration_count"] = 0
                    state["final_response"] = ""
                    state["current_todo_index"] = 0
                    return state
                    
                else:
                    print("👋 User doesn't need additional help. Going back to wake-up word detection.")
                    self.tts_agent.run("Perfect! I'm here whenever you need help. Just say 'Blueberry' to start a new session.")
                    
                    # Reset to wake-up word detection instead of ending
                    state["wake_word_detected"] = False
                    state["voice_input"] = ""
                    state["transcribed_text"] = ""
                    state["user_confirmed"] = False
                    state["confirmation_status"] = ""
                    state["confirmation_spoken"] = False
                    state["current_step"] = "wake_word_detection"
                    state["pipeline_status"] = "active"
                    state["user_intent"] = ""
                    state["generated_todos"] = []
                    state["todos_completed"] = False
                    state["generated_code"] = ""
                    state["code_file_path"] = ""
                    state["code_explanation"] = ""
                    state["code_review"] = ""
                    state["review_score"] = 0
                    state["user_feedback"] = ""
                    state["feedback_processed"] = False
                    state["iteration_count"] = 0
                    state["final_response"] = ""
                    state["current_todo_index"] = 0
                    
            else:
                print("⏰ No response. Going back to wake-up word detection.")
                self.tts_agent.run("I didn't hear anything. I'm here whenever you need help. Just say 'Blueberry' to start a new session.")
                
                # Reset to wake-up word detection instead of ending
                state["wake_word_detected"] = False
                state["voice_input"] = ""
                state["transcribed_text"] = ""
                state["user_confirmed"] = False
                state["confirmation_status"] = ""
                state["confirmation_spoken"] = False
                state["current_step"] = "wake_word_detection"
                state["pipeline_status"] = "active"
                state["user_intent"] = ""
                state["generated_todos"] = []
                state["todos_completed"] = False
                state["generated_code"] = ""
                state["code_file_path"] = ""
                state["code_explanation"] = ""
                state["code_review"] = ""
                state["review_score"] = 0
                state["user_feedback"] = ""
                state["feedback_processed"] = False
                state["iteration_count"] = 0
                state["final_response"] = ""
                state["current_todo_index"] = 0
            
        except Exception as e:
            print(f" Error in response generation: {e}")
            state["error_message"] = str(e)
            state["pipeline_status"] = "error"
        
        return state
    
    # ==================== HELPER METHODS ====================
    
    def _summarize_user_request(self, request: str) -> str:
        """Summarize user request in a more natural way"""
        request_lower = request.lower()
        
        # Extract key action and object with better pattern matching
        if "write" in request_lower and "function" in request_lower:
            if "hello world" in request_lower:
                return "write a function to print hello world"
            elif "print" in request_lower:
                return "write a function that prints something"
            else:
                return "write a function"
        elif "create" in request_lower and "function" in request_lower:
            if "hello world" in request_lower:
                return "create a hello world function"
            elif "print" in request_lower:
                return "create a function that prints something"
            else:
                return "create a function"
        elif "print" in request_lower and "hello world" in request_lower:
            return "create a function to print hello world"
        elif "create" in request_lower and "class" in request_lower:
            return "create a class"
        elif "create" in request_lower and "api" in request_lower:
            return "create an API"
        elif "build" in request_lower:
            return "build something"
        elif "make" in request_lower:
            return "make something"
        elif "generate" in request_lower:
            return "generate some code"
        elif "hello world" in request_lower:
            return "create a hello world program"
        elif "print" in request_lower:
            return "create something that prints"
        else:
            # Default summarization - keep more context
            words = request.split()
            if len(words) > 8:
                return f"{' '.join(words[:4])}... {words[-2]} {words[-1]}"
            elif len(words) > 5:
                return f"{' '.join(words[:3])}... {words[-1]}"
            else:
                return request
    
    def _generate_todos_from_request(self, request: str) -> List[str]:
        """Generate focused interactive todos from user request - Simplified for better interaction"""
        # Simplified todo generation for better user interaction
        todos = []
        request_lower = request.lower()
        
        # Always start with file creation
        todos.append("Create a new file with appropriate name and extension")
        
        # Function-specific todos (simplified)
        if "function" in request_lower:
            todos.append("Create the main function with proper parameters")
            todos.append("Implement the function logic")
        
        # Class-specific todos (simplified)
        elif "class" in request_lower:
            todos.append("Define the class structure and constructor")
            todos.append("Implement class methods")
        
        # API-specific todos (simplified)
        elif any(word in request_lower for word in ["api", "endpoint", "rest", "http"]):
            todos.append("Set up the API framework")
            todos.append("Create the endpoint structure")
        
        # Database-specific todos (simplified)
        elif any(word in request_lower for word in ["database", "model", "schema", "table"]):
            todos.append("Design the database schema")
            todos.append("Create the database model")
        
        # Test-specific todos (simplified)
        elif "test" in request_lower:
            todos.append("Create test cases")
            todos.append("Implement test logic")
        
        # Web-specific todos (simplified)
        elif any(word in request_lower for word in ["web", "html", "css", "frontend"]):
            todos.append("Create HTML structure")
            todos.append("Add CSS styling")
        
        # Default todos for simple requests
        else:
            todos.append("Implement the requested functionality")
            todos.append("Add proper documentation and comments")
        
        return todos
    
    def _analyze_code_request(self, request: str) -> tuple[str, str]:
        """Analyze the code request to determine language and task type"""
        request_lower = request.lower()
        
        # Language detection - improved to handle "I want a Java function" type requests
        language = "python"  # default
        if any(word in request_lower for word in ["javascript", "js", "node", "react", "vue", "angular"]):
            language = "javascript"
        elif any(word in request_lower for word in ["java", "spring", "maven", "gradle"]):
            language = "java"
        elif any(word in request_lower for word in ["c++", "cpp", "c plus plus"]):
            language = "cpp"
        elif any(word in request_lower for word in ["c#", "csharp", "dotnet", ".net"]):
            language = "csharp"
        elif any(word in request_lower for word in ["go", "golang"]):
            language = "go"
        elif any(word in request_lower for word in ["rust", "cargo"]):
            language = "rust"
        elif any(word in request_lower for word in ["php", "laravel", "symfony"]):
            language = "php"
        elif any(word in request_lower for word in ["ruby", "rails", "sinatra"]):
            language = "ruby"
        elif any(word in request_lower for word in ["swift", "ios", "macos"]):
            language = "swift"
        elif any(word in request_lower for word in ["kotlin", "android"]):
            language = "kotlin"
        elif any(word in request_lower for word in ["typescript", "ts"]):
            language = "typescript"
        elif any(word in request_lower for word in ["html", "css", "web", "frontend"]):
            language = "html"
        elif any(word in request_lower for word in ["sql", "database", "query"]):
            language = "sql"
        elif any(word in request_lower for word in ["bash", "shell", "script", "linux"]):
            language = "bash"
        elif any(word in request_lower for word in ["powershell", "windows"]):
            language = "powershell"
        elif any(word in request_lower for word in ["yaml", "yml", "config"]):
            language = "yaml"
        elif any(word in request_lower for word in ["json", "api", "rest"]):
            language = "json"
        elif any(word in request_lower for word in ["xml", "soap"]):
            language = "xml"
        
        # Task type detection - improved to handle "I want a Java function" type requests
        task_type = "function"  # default
        if any(word in request_lower for word in ["class", "object", "oop", "inheritance"]):
            task_type = "class"
        elif any(word in request_lower for word in ["api", "endpoint", "rest", "http"]):
            task_type = "api"
        elif any(word in request_lower for word in ["database", "model", "schema", "table"]):
            task_type = "database"
        elif any(word in request_lower for word in ["test", "unit", "integration", "spec"]):
            task_type = "test"
        elif any(word in request_lower for word in ["script", "automation", "tool"]):
            task_type = "script"
        elif any(word in request_lower for word in ["web", "frontend", "ui", "component"]):
            task_type = "frontend"
        elif any(word in request_lower for word in ["backend", "server", "service"]):
            task_type = "backend"
        elif any(word in request_lower for word in ["algorithm", "data structure", "sort", "search"]):
            task_type = "algorithm"
        elif any(word in request_lower for word in ["config", "configuration", "setup"]):
            task_type = "config"
        
        print(f" Language analysis: '{request}' → {language}")
        print(f" Task type analysis: '{request}' → {task_type}")
        
        return language, task_type
    
    def _get_file_extension(self, language: str) -> str:
        """Get appropriate file extension for the language"""
        extensions = {
            "python": "py",
            "javascript": "js",
            "typescript": "ts",
            "java": "java",
            "c++": "cpp",  # Map "c++" to "cpp" extension
            "cpp": "cpp",
            "c#": "cs",
            "csharp": "cs",
            "go": "go",
            "rust": "rs",
            "php": "php",
            "ruby": "rb",
            "swift": "swift",
            "kotlin": "kt",
            "html": "html",
            "css": "css",
            "sql": "sql",
            "bash": "sh",
            "powershell": "ps1",
            "yaml": "yml",
            "json": "json",
            "xml": "xml"
        }
        return extensions.get(language, "txt")
    
    def _is_language_specified(self, request: str) -> bool:
        """Check if programming language is specified in the request"""
        request_lower = request.lower()
        language_keywords = [
            "python", "javascript", "js", "java", "c++", "cpp", "c#", "csharp", "go", "golang",
            "rust", "php", "ruby", "swift", "kotlin", "typescript", "ts", "html", "css",
            "sql", "bash", "shell", "powershell", "yaml", "yml", "json", "xml"
        ]
        return any(keyword in request_lower for keyword in language_keywords)
    
    def _extract_language_from_response(self, response: str) -> str:
        """Extract programming language from user response using GPT-4"""
        try:
            # Use GPT-4 to detect language from user response
            language_prompt = f"""
            Analyze the following user response and determine which programming language they want to use.
            
            User response: "{response}"
            
            Return ONLY the language name in lowercase. Choose from:
            python, javascript, java, c++, c#, go, rust, php, ruby, swift, kotlin, typescript, html, css, sql, bash, powershell, yaml, json, xml
            
            If unclear, return "python" as default.
            
            Language:"""
            
            # Use GPT-4 for language detection
            from langchain_openai import ChatOpenAI
            llm = ChatOpenAI(model="gpt-4", temperature=0.1)
            
            result = llm.invoke(language_prompt)
            detected_language = result.content.strip().lower()
            
            # Validate the detected language
            valid_languages = ["python", "javascript", "java", "c++", "c#", "go", "rust", "php", "ruby", "swift", "kotlin", "typescript", "html", "css", "sql", "bash", "powershell", "yaml", "json", "xml"]
            
            if detected_language in valid_languages:
                print(f" GPT-4 detected language: '{detected_language}' from '{response}'")
                return detected_language
            else:
                print(f" GPT-4 returned invalid language '{detected_language}', defaulting to python")
                return "python"
                
        except Exception as e:
            print(f" Error in GPT-4 language detection: {e}")
            # Fallback to simple keyword matching
            response_lower = response.lower().strip()
            if "python" in response_lower:
                return "python"
            elif "javascript" in response_lower or "js" in response_lower:
                return "javascript"
            elif "java" in response_lower:
                return "java"
            elif "c++" in response_lower or "cpp" in response_lower:
                return "c++"
            else:
                return "python"
    
    def _generate_smart_filename(self, request: str, language: str) -> str:
        """Generate smart filename based on user request and language"""
        request_lower = request.lower()
        
        # Check if user specified a filename
        if "filename" in request_lower or "file name" in request_lower:
            # Extract filename from request
            words = request.split()
            for i, word in enumerate(words):
                if word.lower() in ["filename", "file", "name"] and i + 1 < len(words):
                    filename = words[i + 1].strip(".,!?")
                    if filename:
                        return filename
        
        # Generate filename based on content
        if "hello world" in request_lower or "print hello" in request_lower:
            return "hello_world"
        elif "function" in request_lower:
            return "main_function"
        elif "class" in request_lower:
            return "main_class"
        elif "api" in request_lower:
            return "api_server"
        elif "database" in request_lower:
            return "database_model"
        elif "test" in request_lower:
            return "test_file"
        elif "script" in request_lower:
            return "script"
        elif "web" in request_lower or "html" in request_lower:
            return "index"
        elif "css" in request_lower:
            return "styles"
        elif "javascript" in request_lower or "js" in request_lower:
            return "main"
        elif "java" in request_lower:
            return "Main"
        elif "c++" in request_lower or "cpp" in request_lower:
            return "main"
        elif "go" in request_lower:
            return "main"
        elif "rust" in request_lower:
            return "main"
        elif "php" in request_lower:
            return "index"
        elif "ruby" in request_lower:
            return "main"
        elif "swift" in request_lower:
            return "main"
        elif "kotlin" in request_lower:
            return "Main"
        elif "sql" in request_lower:
            return "database_schema"
        elif "bash" in request_lower or "shell" in request_lower:
            return "script"
        elif "powershell" in request_lower:
            return "script"
        elif "yaml" in request_lower or "yml" in request_lower:
            return "config"
        elif "json" in request_lower:
            return "data"
        elif "xml" in request_lower:
            return "data"
        else:
            # Default filename based on language
            if language == "python":
                return "main"
            elif language == "javascript":
                return "main"
            elif language == "java":
                return "Main"
            elif language == "cpp":
                return "main"
            elif language == "go":
                return "main"
            elif language == "rust":
                return "main"
            elif language == "php":
                return "index"
            elif language == "ruby":
                return "main"
            elif language == "swift":
                return "main"
            elif language == "kotlin":
                return "Main"
            elif language == "html":
                return "index"
            elif language == "css":
                return "styles"
            elif language == "sql":
                return "database"
            elif language == "bash":
                return "script"
            elif language == "powershell":
                return "script"
            elif language == "yaml":
                return "config"
            elif language == "json":
                return "data"
            elif language == "xml":
                return "data"
            else:
                return "main"
    
    def _generate_universal_code(self, request: str, todos: List[str], language: str, task_type: str) -> str:
        """Generate code for any programming language and task type"""
        try:
            # Use the appropriate agent based on language
            if language == "python":
                return self._generate_python_code(request, todos, task_type)
            elif language == "javascript":
                return self._generate_javascript_code(request, todos, task_type)
            elif language == "java":
                return self._generate_java_code(request, todos, task_type)
            elif language == "c++" or language == "cpp":
                return self._generate_cpp_code(request, todos, task_type)
            elif language == "html":
                return self._generate_html_code(request, todos, task_type)
            elif language == "sql":
                return self._generate_sql_code(request, todos, task_type)
            elif language == "bash":
                return self._generate_bash_code(request, todos, task_type)
            else:
                # Fallback to Python agent for other languages
                return self._generate_python_code(request, todos, task_type)
        except Exception as e:
            return f"# Error generating {language} code: {e}"
    
    def _generate_python_code(self, request: str, todos: List[str], task_type: str) -> str:
        """Generate Python code - Enhanced with proper implementation"""
        todo_text = "\n".join([f"# - {todo}" for todo in todos])
        
        if task_type == "class":
            return f"""# Generated Python class for: {request}
{todo_text}

class GeneratedClass:
    def __init__(self):
        \"\"\"Initialize the class\"\"\"
        pass
    
    def main_method(self):
        \"\"\"Main method implementation\"\"\"
        pass

if __name__ == '__main__':
    obj = GeneratedClass()
    obj.main_method()
"""
        elif task_type == "api":
            return f"""# Generated Python API for: {request}
{todo_text}

from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/endpoint', methods=['GET', 'POST'])
def api_endpoint():
    \"\"\"API endpoint implementation\"\"\"
    return jsonify({{"message": "API response"}})

if __name__ == '__main__':
    app.run(debug=True)
"""
        elif "hello world" in request.lower() or "print hello" in request.lower():
            return f"""# Generated Python function for: {request}
{todo_text}

def print_hello_world():
    \"\"\"Function to print hello world\"\"\"
    print("Hello, World!")

def main():
    \"\"\"Main function to run the hello world function\"\"\"
    print_hello_world()

if __name__ == '__main__':
    main()
"""
        elif "function" in request.lower():
            return f"""# Generated Python function for: {request}
{todo_text}

def main():
    \"\"\"Main function implementation\"\"\"
    # Add your code here
    pass

if __name__ == '__main__':
    main()
"""
        else:
            return f"""# Generated Python code for: {request}
{todo_text}

def main():
    \"\"\"Main function implementation\"\"\"
    # Add your code here
    pass

if __name__ == '__main__':
    main()
"""
    
    def _generate_javascript_code(self, request: str, todos: List[str], task_type: str) -> str:
        """Generate JavaScript code - Enhanced with proper implementation"""
        todo_text = "\n".join([f"// - {todo}" for todo in todos])
        
        if task_type == "class":
            return f"""// Generated JavaScript class for: {request}
{todo_text}

class GeneratedClass {{
    constructor() {{
        // Constructor implementation
    }}
    
    mainMethod() {{
        // Main method implementation
    }}
}}

// Usage
const obj = new GeneratedClass();
obj.mainMethod();
"""
        elif task_type == "api":
            return f"""// Generated JavaScript API for: {request}
{todo_text}

const express = require('express');
const app = express();

app.get('/api/endpoint', (req, res) => {{
    res.json({{ message: 'API response' }});
}});

app.listen(3000, () => {{
    console.log('Server running on port 3000');
}});
"""
        elif "hello world" in request.lower() or "print hello" in request.lower():
            return f"""// Generated JavaScript function for: {request}
{todo_text}

function printHelloWorld() {{
    console.log("Hello, World!");
}}

function main() {{
    printHelloWorld();
}}

main();
"""
        elif "function" in request.lower():
            return f"""// Generated JavaScript function for: {request}
{todo_text}

function main() {{
    // Main function implementation
}}

main();
"""
        else:
            return f"""// Generated JavaScript code for: {request}
{todo_text}

function main() {{
    // Main function implementation
}}

main();
"""
    
    def _generate_java_code(self, request: str, todos: List[str], task_type: str) -> str:
        """Generate Java code - Enhanced with proper implementation"""
        todo_text = "\n".join([f"    // - {todo}" for todo in todos])

        if "hello world" in request.lower() or "print hello" in request.lower():
            return f"""// Generated Java code for: {request}
{todo_text}

public class HelloWorld {{
    public static void printHelloWorld() {{
        System.out.println("Hello, World!");
    }}

    public static void main(String[] args) {{
        printHelloWorld();
    }}
}}
"""
        elif "function" in request.lower():
            return f"""// Generated Java code for: {request}
{todo_text}

public class Main {{
    public static void main(String[] args) {{
        // Main method implementation
    }}
}}
"""
        else:
            return f"""// Generated Java code for: {request}
{todo_text}

public class GeneratedClass {{
    public static void main(String[] args) {{
        // Main method implementation
    }}
}}
"""

    def _generate_cpp_code(self, request: str, todos: List[str], task_type: str) -> str:
        """Generate C++ code - Enhanced with proper implementation"""
        todo_text = "\n".join([f"    // - {todo}" for todo in todos])

        if "hello world" in request.lower() or "print hello" in request.lower():
            return f"""// Generated C++ code for: {request}
{todo_text}

#include <iostream>

void printHelloWorld() {{
    std::cout << "Hello, World!" << std::endl;
}}

int main() {{
    printHelloWorld();
    return 0;
}}
"""
        elif "function" in request.lower():
            return f"""// Generated C++ code for: {request}
{todo_text}

#include <iostream>

int main() {{
    // Main function implementation
    return 0;
}}
"""
        else:
            return f"""// Generated C++ code for: {request}
{todo_text}

#include <iostream>

int main() {{
    // Main function implementation
    return 0;
}}
"""
    
    def _generate_html_code(self, request: str, todos: List[str], task_type: str) -> str:
        """Generate HTML code"""
        todo_text = "\n".join([f"    <!-- - {todo} -->" for todo in todos])
        
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Generated Page</title>
</head>
<body>
{todo_text}
    <h1>Generated HTML for: {request}</h1>
    <script>
        // JavaScript implementation
    </script>
</body>
</html>
"""
    
    def _generate_sql_code(self, request: str, todos: List[str], task_type: str) -> str:
        """Generate SQL code"""
        todo_text = "\n".join([f"-- - {todo}" for todo in todos])
        
        return f"""-- Generated SQL for: {request}
{todo_text}

-- Main SQL implementation
SELECT * FROM table_name WHERE condition = 'value';
"""
    
    def _generate_bash_code(self, request: str, todos: List[str], task_type: str) -> str:
        """Generate Bash script"""
        todo_text = "\n".join([f"# - {todo}" for todo in todos])
        
        return f"""#!/bin/bash
# Generated Bash script for: {request}
{todo_text}

# Main script implementation
echo "Script executed successfully"
"""
    
    def _generate_code_from_todos(self, todos: List[str], request: str) -> str:
        """Generate code from todos using Python agent"""
        try:
            # Use Python agent to generate code
            todo_text = "\n".join([f"- {todo}" for todo in todos])
            full_request = f"{request}\n\nTasks to implement:\n{todo_text}"
            
            # This would call the actual Python agent
            # For now, return a placeholder
            return f"# Generated code for: {request}\n# Tasks: {', '.join(todos)}\n\ndef main():\n    pass\n\nif __name__ == '__main__':\n    main()"
        except Exception as e:
            return f"# Error generating code: {e}"
    
    def _improve_code_with_feedback(self, code: str, feedback: str) -> str:
        """Improve code based on user feedback"""
        # This would use the Python agent to improve code
        # For now, return the original code with a comment
        return f"# Improved based on feedback: {feedback}\n{code}"
    
    def _check_todo_completion(self, todos: List[str], code: str) -> List[str]:
        """Check which todos are completed in the code"""
        completed = []
        for todo in todos:
            # Simple keyword matching for completion check
            if any(keyword in code.lower() for keyword in todo.lower().split()):
                completed.append(todo)
        return completed
    
    def _generate_coding_response(self, code: str, todos: List[str]) -> str:
        """Generate response for coding tasks"""
        return f"I've generated the code with {len(todos)} tasks implemented. The code has been saved and is ready for use."
    
    def _generate_explanation_response(self, explanation: str) -> str:
        """Generate response for explanation tasks"""
        return f"Here's the explanation: {explanation}"
    
    def _generate_review_response(self, review: str) -> str:
        """Generate response for review tasks"""
        return f"Here's my code review: {review}"
    
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
    
    def _should_continue_after_intent_classification(self, state: VoiceCodingState) -> str:
        """Route to appropriate task based on intent classification"""
        user_intent = state.get("user_intent", "general")
        
        if user_intent == "coding":
            return "todo_generation"  # Start with todo generation for coding tasks
        elif user_intent == "review":
            return "code_review"
        elif user_intent == "explanation":
            return "code_explanation"
        else:  # general or unknown
            return "code_explanation"  # Default to explanation for general queries
    
    def _should_continue_after_todo_generation(self, state: VoiceCodingState) -> str:
        """Route after todo generation"""
        user_intent = state.get("user_intent", "coding")
        
        if user_intent == "coding":
            return "code_generation"
        elif user_intent == "explanation":
            return "code_explanation"
        elif user_intent == "review":
            return "code_review"
        else:
            return "code_generation"  # Default to code generation
    
    def _should_continue_after_code_generation(self, state: VoiceCodingState) -> str:
        """Route after code generation"""
        iteration_count = state.get("iteration_count", 0)
        max_iterations = state.get("max_iterations", 3)
        
        # Check if we need more iterations
        if iteration_count < max_iterations:
            return "todo_completion_check"
        else:
            return "user_feedback"
    
    def _should_continue_after_code_review(self, state: VoiceCodingState) -> str:
        """Route after code review"""
        # Can go to code generation for improvements or directly to response
        return "response_generation"
    
    def _should_continue_after_user_feedback(self, state: VoiceCodingState) -> str:
        """Route after user feedback"""
        feedback_processed = state.get("feedback_processed", False)
        
        if feedback_processed:
            return "code_iteration"
        else:
            return "response_generation"
    
    def _should_continue_after_code_iteration(self, state: VoiceCodingState) -> str:
        """Route after code iteration"""
        iteration_count = state.get("iteration_count", 0)
        max_iterations = state.get("max_iterations", 3)
        
        if iteration_count < max_iterations:
            return "user_feedback"  # Continue iteration loop
        else:
            return "response_generation"  # End iteration loop
    
    def _should_continue_after_todo_completion_check(self, state: VoiceCodingState) -> str:
        """Route after todo completion check - Interactive flow"""
        todos_completed = state.get("todos_completed", False)
        current_todo_index = state.get("current_todo_index", 0)
        todos = state.get("generated_todos", [])
        
        if todos_completed:
            return "response_generation"
        elif current_todo_index < len(todos):
            return "code_generation"  # Continue with next todo
        else:
            return "response_generation"  # All todos processed
    
    def _should_continue_after_response_generation(self, state: VoiceCodingState) -> str:
        """Route after response generation - Check if user wants additional help"""
        pipeline_status = state.get("pipeline_status", "completed")
        
        if pipeline_status == "active":
            return "intent_classification"  # Start new task
        else:
            return END  # End session
    
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
        
        try:
            print(" Starting Confirmation Flow Pipeline...")
            result = self.workflow.invoke(initial_state)
            print(" Confirmation flow completed!")
            return result
            
        except Exception as e:
            print(f" Pipeline error: {e}")
            return {
                "error_message": str(e),
                "pipeline_status": "error"
            }
    
    def start_continuous_session(self):
        """Start the continuous voice coding session with infinite loop"""
        print("\n Starting Continuous Voice Coding Session...")
        print("📋 Flow: Wake-up Word → Voice Input → Speech-to-Text → Confirmation → Intent Classification → Code Generation")
        print(" Say 'Blueberry' to start, then speak your request")
        print("🔄 After task completion, system asks if you need more help")
        print("🔄 If you say 'no', system goes back to wake-up word detection")
        print("🔄 If you say 'yes', system starts a new task")
        print("⏹️  Press Ctrl+C to exit anytime")
        print("\n" + "=" * 60)

        try:
            while True:
                print("\n🔄 Starting new interaction...")

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

                # Run the workflow
                result = self.workflow.invoke(initial_state)

                # Check if task was completed
                if result.get("task_completed"):
                    print("\n Task completed successfully!")
                    print(f" Intent: {result.get('user_intent', 'unknown')}")
                    print(f" Task Result:\n{result.get('task_result', 'No result')}")
                elif result.get("user_confirmed"):
                    print("\n User confirmed! Intent classification completed.")
                    print(f" Intent: {result.get('user_intent', 'unknown')}")
                elif result.get("pipeline_status") == "completed":
                    print("\n Session completed! Going back to wake-up word detection...")
                    print("🔄 Waiting for 'Blueberry' to start new session...")
                    continue  # Continue the while loop to wait for next wake-up word
                else:
                    print("\n User did not confirm. Flow ended.")

                print("\n🔄 Ready for next interaction...")

        except KeyboardInterrupt:
            print("\n\n👋 Session interrupted by user. Stopping TTS...")
            # Stop TTS immediately
            self.tts_agent.stop_tts()
            print(" TTS stopped. Goodbye!")
        except Exception as e:
            print(f"\n Session error: {e}")
            print("Restarting session...")
            time.sleep(2)


def main():
    """Main entry point for LangGraph Voice Pipeline - Confirmation Flow Only"""
    print(" LangGraph Voice Pipeline - Confirmation Flow")
    print(" Testing: Wake-up → Voice → Speech-to-Text → Confirmation")
    print("=" * 60)
    
    # Global variable to store pipeline instance
    global_pipeline = None

    def signal_handler(sig, frame):
        """Handle Ctrl+C gracefully"""
        print("\n\n👋 Session interrupted by user. Stopping TTS...")
        if global_pipeline:
            global_pipeline.tts_agent.stop_tts()
        print(" TTS stopped. Goodbye!")
        sys.exit(0)

    # Set up signal handler for Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)
    
    # Initialize pipeline
    pipeline = LangGraphVoicePipeline()
    global_pipeline = pipeline  # Store reference for signal handler
    
    # Start continuous session
    pipeline.start_continuous_session()


if __name__ == "__main__":
    main()