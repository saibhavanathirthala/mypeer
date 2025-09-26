"""
Intent Classification Agent using GPT-4.
Determines user intent to route to appropriate agents and modes.
"""

import os
import json
from typing import Dict, Any
from openai import OpenAI
from .base_agent import BaseAgent
from prompts import INTENT_CLASSIFICATION_PROMPT, format_user_request_prompt


class IntentAgent(BaseAgent):
    """Agent that classifies user intent to route to appropriate handlers."""
    
    def __init__(self, config: dict = None):
        super().__init__("IntentAgent", config)
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    def run(self, input_data: str) -> Dict[str, Any]:
        """
        Classify user intent from their request.
        
        Args:
            input_data: User's voice/text request
            
        Returns:
            Dictionary with intent classification and extracted parameters
        """
        try:
            self.log(f"Classifying intent for: '{input_data}'")
            
            # Check for specific exit phrases first
            if self._is_exit_intent(input_data):
                return {
                    "intent": "exit",
                    "confidence": 1.0,
                    "action": "end_session",
                    "message": "Goodbye session detected"
                }
            
            # Use GPT-4 for intent classification
            classification = self._classify_with_gpt4(input_data)
            
            self.log(f"Classified intent: {classification['intent']} (confidence: {classification['confidence']})")
            
            return classification
            
        except Exception as e:
            self.log(f"Error in intent classification: {str(e)}")
            # Default to discussion mode on error
            return {
                "intent": "discussion",
                "confidence": 0.5,
                "action": "discuss",
                "message": "Defaulting to discussion mode due to classification error"
            }
    
    def _is_exit_intent(self, text: str) -> bool:
        """Check for specific exit phrases."""
        exit_phrases = [
            "thank you pair programming",
            "thanks pair programming", 
            "thank you pair programmer",
            "goodbye pair programming",
            "exit pair programming",
            "stop pair programming"
        ]
        
        text_lower = text.lower().strip()
        return any(phrase in text_lower for phrase in exit_phrases)
    
    def _classify_with_gpt4(self, user_request: str) -> Dict[str, Any]:
        """Use GPT-4 to classify the user's intent."""
        
        prompt = format_user_request_prompt(INTENT_CLASSIFICATION_PROMPT, user_request)

        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an intent classification expert. Always respond with valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                max_tokens=300
            )
            
            result_text = response.choices[0].message.content.strip()
            
            # Parse JSON response
            classification = json.loads(result_text)
            
            # Validate required fields
            required_fields = ["intent", "confidence", "action", "message"]
            for field in required_fields:
                if field not in classification:
                    raise ValueError(f"Missing required field: {field}")
            
            # Add extracted_info if missing
            if "extracted_info" not in classification:
                classification["extracted_info"] = {}
            
            return classification
            
        except Exception as e:
            self.log(f"Error in GPT-4 classification: {str(e)}")
            # Return default classification
            return {
                "intent": "discussion",
                "confidence": 0.3,
                "action": "discuss",
                "extracted_info": {},
                "message": "Fallback classification due to parsing error"
            }
    
    def get_intent_description(self, intent: str) -> str:
        """Get a human-readable description of the intent."""
        descriptions = {
            "coding": "Writing or generating code",
            "discussion": "Answering questions or having a conversation", 
            "file_operations": "Opening or managing files",
            "exit": "Ending the session"
        }
        return descriptions.get(intent, "Unknown intent")
