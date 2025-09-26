"""
To-do List Agent using GPT-4.
Converts user requests into structured to-do lists of coding tasks.
"""

import os
import json
from typing import List
from openai import OpenAI
from .base_agent import BaseAgent
from prompts import TODO_SYSTEM_PROMPT, TODO_CREATION_PROMPT


class TodoAgent(BaseAgent):
    """Agent that converts requests into structured to-do lists."""
    
    def __init__(self, config: dict = None):
        super().__init__("TodoAgent", config)
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    def run(self, input_data: str) -> List[str]:
        """
        Convert a user request into a structured to-do list.
        
        Args:
            input_data: User's coding request
            
        Returns:
            List of actionable coding tasks
        """
        try:
            self.log(f"Converting request to to-do list: '{input_data}'")
            
            prompt = self._create_todo_prompt(input_data)
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": self._get_system_prompt()},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=1000
            )
            
            todo_response = response.choices[0].message.content.strip()
            
            # Parse the response to extract the todo list
            todo_list = self._parse_todo_response(todo_response)
            
            self.log(f"Generated {len(todo_list)} tasks:")
            for i, task in enumerate(todo_list, 1):
                self.log(f"  {i}. {task}")
            
            return todo_list
            
        except Exception as e:
            self.log(f"Error generating to-do list: {str(e)}")
            # Fallback to a simple breakdown
            return [f"Implement: {input_data}"]
    
    def _get_system_prompt(self) -> str:
        """Get the system prompt for the to-do generation."""
        return TODO_SYSTEM_PROMPT
    
    def _create_todo_prompt(self, request: str) -> str:
        """Create the prompt for to-do generation."""
        return TODO_CREATION_PROMPT.format(request=request)
    
    def _parse_todo_response(self, response: str) -> List[str]:
        """Parse the GPT response to extract to-do items."""
        lines = response.strip().split('\n')
        todo_items = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Remove numbering (1., 2., etc.) and clean up
            import re
            # Match patterns like "1.", "1)", "- ", "• ", etc.
            cleaned_line = re.sub(r'^[\d\-\•\*\+]+[\.\)]\s*', '', line)
            cleaned_line = re.sub(r'^[\-\•\*\+]\s*', '', cleaned_line)
            
            if cleaned_line:
                todo_items.append(cleaned_line)
        
        return todo_items
    
    def format_todo_list_for_speech(self, todo_list: List[str]) -> str:
        """Format the to-do list for TTS presentation."""
        if not todo_list:
            return "I couldn't generate a to-do list for this request."
        
        formatted = "Here's the to-do list I've created:\n"
        for i, task in enumerate(todo_list, 1):
            formatted += f"{i}. {task}\n"
        
        formatted += "\nShould I proceed with implementing these tasks?"
        return formatted
    
    def get_user_approval(self, todo_list: List[str], stt_agent, use_voice=True, auto_detect=True) -> bool:
        """
        Present the to-do list and get voice approval only (no typing allowed).
        
        Args:
            todo_list: The generated to-do list
            stt_agent: STT agent for voice input (required)
            use_voice: Whether to use voice input (always True)
            auto_detect: Whether to use automatic voice detection (always True)
            
        Returns:
            True if user approves, False otherwise
        """
        self.log("Presenting to-do list for voice approval...")
        
        print("\n" + "="*50)
        print("GENERATED TO-DO LIST:")
        print("="*50)
        for i, task in enumerate(todo_list, 1):
            print(f"{i}. {task}")
        print("="*50)
        
        # Always use automatic voice detection in voice-only mode
        approved = stt_agent.get_voice_confirmation_auto(
            "Do you approve this to-do list?"
        )
        
        if approved:
            self.log("To-do list approved via voice")
        else:
            self.log("To-do list rejected via voice")
        
        return approved
