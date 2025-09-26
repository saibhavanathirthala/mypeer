"""
AI Pair Programming Multi-Agent Framework
Central Orchestrator that manages the workflow between agents.

Workflow: STT → TTS (confirmation) → To-do → TTS → Python Code → TTS
"""

import os
import sys
from dotenv import load_dotenv
from agents import (STTAgent, TTSPromptAgent, TodoAgent, ProgrammingAgent, 
                   IntentAgent, DiscussionAgent, FileAgent, CodeAnalysisAgent)


class PairProgrammingOrchestrator:
    """Central orchestrator for the AI Pair Programming multi-agent framework - VOICE ONLY."""
    
    def __init__(self):
        """Initialize the orchestrator with all agents in voice-only mode."""
        # Load environment variables
        load_dotenv()
        
        # Verify OpenAI API key
        if not os.getenv("OPENAI_API_KEY"):
            print("ERROR: OPENAI_API_KEY not found in environment variables.")
            print("Please set your OpenAI API key in a .env file or environment variable.")
            sys.exit(1)
        
        # Initialize agents - DYNAMIC VOICE MODE
        self.stt_agent = STTAgent()
        self.tts_agent = TTSPromptAgent()
        self.intent_agent = IntentAgent()
        self.discussion_agent = DiscussionAgent()
        self.file_agent = FileAgent()
        self.code_analysis_agent = CodeAnalysisAgent()
        self.todo_agent = TodoAgent()
        self.programming_agent = ProgrammingAgent()
        
        print("🤖 AI Pair Programming Framework - INTELLIGENT VOICE MODE")
        print("🎤 100% hands-free operation with smart intent detection")
        print("📋 Available modes: Discussion, Coding, File Operations, Code Analysis")
        print("🧠 Smart routing based on your voice commands")
        print("-" * 60)
    
    def run_workflow(self, input_data: str = None) -> str:
        """
        Run the intelligent workflow with dynamic intent routing.
        
        Args:
            input_data: Initial user input (optional, will use voice if None)
            
        Returns:
            Result message or file path
        """
        try:
            # Step 1: Get Voice Input
            print("\n🎧 Listening for your request...")
            if input_data is None:
                user_request = self.stt_agent.auto_record_speech(max_duration=30)
                if not user_request:
                    print("❌ No voice input detected. Please try again.")
                    return ""
            else:
                user_request = input_data
            
            print(f"📝 Understood: '{user_request}'")
            
            # Step 2: Classify Intent
            print("\n🧠 Analyzing your request...")
            intent_result = self.intent_agent.run(user_request)
            intent = intent_result["intent"]
            confidence = intent_result["confidence"]
            
            print(f"🎯 Detected intent: {intent} (confidence: {confidence:.2f})")
            
            # Step 3: Route to Appropriate Handler
            if intent == "exit":
                return self._handle_exit()
            elif intent == "discussion":
                return self._handle_discussion(user_request, intent_result)
            elif intent == "file_operations":
                return self._handle_file_operations(user_request, intent_result)
            elif intent == "code_analysis":
                return self._handle_code_analysis(user_request, intent_result)
            elif intent == "coding":
                return self._handle_coding(user_request, intent_result)
            else:
                self.tts_agent.run("I'm not sure what you want me to do. Could you try asking differently?")
                return ""
                
        except KeyboardInterrupt:
            print("\n\n👋 Voice session interrupted by user.")
            return ""
        except Exception as e:
            print(f"\n❌ Error in workflow: {str(e)}")
            self.tts_agent.run("I encountered an error processing your request. Please try again.")
            return ""
    
    def _handle_exit(self) -> str:
        """Handle session exit."""
        print("\n👋 Ending session...")
        self.tts_agent.run("Thank you for using the AI Pair Programming Framework! Goodbye!")
        return "EXIT_SESSION"
    
    def _handle_discussion(self, user_request: str, intent_result: dict) -> str:
        """Handle discussion/question mode."""
        print(f"\n💬 Discussion Mode: {intent_result['message']}")
        
        # Get response from discussion agent
        response = self.discussion_agent.run(user_request)
        
        # Speak the response
        self.tts_agent.run(response)
        
        print(f"✅ Discussion completed")
        return "DISCUSSION_COMPLETED"
    
    def _handle_file_operations(self, user_request: str, intent_result: dict) -> str:
        """Handle file operations mode."""
        print(f"\n📁 File Operations Mode: {intent_result['message']}")
        
        # Extract file operation details
        file_operation = self.file_agent.extract_file_operation(user_request)
        
        # Execute file operation
        result = self.file_agent.run(file_operation)
        
        # Speak the result
        self.tts_agent.run(result)
        
        print(f"✅ File operation completed")
        return "FILE_OPERATION_COMPLETED"
    
    def _handle_code_analysis(self, user_request: str, intent_result: dict) -> str:
        """Handle code analysis mode."""
        print(f"\n🔍 Code Analysis Mode: {intent_result['message']}")
        
        # Extract code analysis details
        code_analysis_request = self.code_analysis_agent.extract_code_analysis_request(user_request)
        
        # Check if we have code to analyze
        if not code_analysis_request.get("code", "").strip():
            no_code_msg = """I don't see any code to analyze. Here's how you can provide code:

1. Copy the code to your clipboard, then say 'explain this code'
2. Say 'analyze the code in my clipboard'  
3. Or try selecting the code first, then ask me to explain it

Please copy some code and try again."""
            
            self.tts_agent.run(no_code_msg)
            print("❌ No code found for analysis")
            return "NO_CODE_PROVIDED"
        
        # Analyze the code
        analysis_result = self.code_analysis_agent.run(code_analysis_request)
        
        # Speak the analysis
        self.tts_agent.run(analysis_result)
        
        # Show analysis type and language detected
        analysis_type = code_analysis_request.get("analysis_type", "explain")
        language = code_analysis_request.get("language", "auto")
        print(f"✅ Code analysis completed (type: {analysis_type}, language: {language})")
        
        return "CODE_ANALYSIS_COMPLETED"
    
    def _handle_coding(self, user_request: str, intent_result: dict) -> str:
        """Handle coding mode with confirmation workflow."""
        print(f"\n💻 Coding Mode: {intent_result['message']}")
        
        # Voice Confirmation
        print("\n🔄 Confirming coding request...")
        confirmation_msg = self.tts_agent.confirm_request(user_request)
        
        is_confirmed = self.tts_agent.get_user_confirmation(
            stt_agent=self.stt_agent,
            use_voice=True,
            auto_detect=True
        )
        if not is_confirmed:
            self.tts_agent.run("No problem. What else would you like me to help you with?")
            return ""
        
        # Generate To-do List
        print("\n📋 Creating your coding plan...")
        todo_list = self.todo_agent.run(user_request)
        
        # Present to-do list via voice and get approval
        todo_speech = self.todo_agent.format_todo_list_for_speech(todo_list)
        self.tts_agent.run(todo_speech)
        
        todo_approved = self.todo_agent.get_user_approval(
            todo_list,
            stt_agent=self.stt_agent,
            use_voice=True,
            auto_detect=True
        )
        if not todo_approved:
            self.tts_agent.run("Alright, let me know what you'd like to code instead.")
            return ""
        
        # Generate Python Code
        print("\n⚡ Generating your code...")
        code_file_path = self.programming_agent.run(todo_list)
        
        if code_file_path and self.programming_agent.validate_code(code_file_path):
            completion_msg = f"Perfect! I've generated your code and saved it to {os.path.basename(code_file_path)}. The code is ready to run!"
            self.tts_agent.run(completion_msg)
            
            # Preview the code
            self.programming_agent.preview_code(code_file_path)
            
            print(f"✅ Code generated: {code_file_path}")
            return code_file_path
        else:
            self.tts_agent.run("I had trouble generating the code. Let me know if you'd like to try a different approach.")
            return ""
    
    def start_voice_session(self):
        """Start a continuous intelligent voice interaction session."""
        print("\n🎤 Starting Intelligent Voice Session")
        print("🗣️  Ask questions, request code, manage files, or analyze code")
        print("🔄 Say 'thank you Pair Programming' to end")
        print("💡 Examples:")
        print("   'What is recursion?' (Discussion)")
        print("   'Create a sorting function' (Coding)")
        print("   'Open main.py' (File Operations)")
        print("   'Explain this code' (Code Analysis - copy code first!)")
        print("-" * 60)
        
        while True:
            try:
                print("\n🎧 Listening for your next request...")
                
                # Get voice input
                user_request = self.stt_agent.auto_record_speech(max_duration=30)
                
                if not user_request:
                    print("❌ No voice detected. Please try again or say 'thank you Pair Programming' to exit.")
                    continue
                
                # Process the request (exit handled within workflow)
                result = self.run_workflow(user_request)
                
                # Check if user requested to exit
                if result == "EXIT_SESSION":
                    print("👋 Voice session ended.")
                    break
                
                # Handle different result types
                if result and result.endswith('.py'):
                    # Code generation result
                    print(f"\n✅ Code generated: {result}")
                elif result:
                    # Other successful operations
                    print(f"\n✅ Operation completed: {result}")
                
                print("\n" + "-" * 60)
                
            except KeyboardInterrupt:
                self.tts_agent.run("Goodbye!")
                print("\n\n👋 Voice session ended.")
                break


def main():
    """Main entry point - Intelligent Voice Mode."""
    print("🤖 AI Pair Programming Framework - INTELLIGENT VOICE")
    print("🧠 Smart Assistant with Dynamic Intent Detection")
    print("=" * 60)
    
    # Initialize intelligent orchestrator
    orchestrator = PairProgrammingOrchestrator()
    
    # Welcome message
    welcome_msg = """Welcome to the intelligent AI Pair Programming Framework! 

I can help you in four ways:
- Ask me questions and I'll discuss programming concepts with you
- Tell me to create code and I'll write it for you
- Ask me to open files and I'll help you manage them
- Copy code to your clipboard and ask me to explain, review, or debug it

Just speak naturally and I'll understand what you want to do. 
Say 'thank you Pair Programming' when you're done!"""
    
    orchestrator.tts_agent.run(welcome_msg)
    
    # Start the intelligent voice session
    orchestrator.start_voice_session()


if __name__ == "__main__":
    main()
