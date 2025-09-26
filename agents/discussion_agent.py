"""
Discussion Agent using GPT-4.
Handles questions, explanations, and general conversation.
"""

import os
from openai import OpenAI
from .base_agent import BaseAgent
from prompts import DISCUSSION_SYSTEM_PROMPT, DISCUSSION_PROGRAMMING_PROMPT


class DiscussionAgent(BaseAgent):
    """Agent that handles questions and discussion through voice."""
    
    def __init__(self, config: dict = None):
        super().__init__("DiscussionAgent", config)
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    def run(self, input_data: str) -> str:
        """
        Handle discussion/question requests.
        
        Args:
            input_data: User's question or discussion topic
            
        Returns:
            Response text to be spoken back to user
        """
        try:
            self.log(f"Processing discussion request: '{input_data}'")
            
            # Generate response using GPT-4
            response = self._generate_discussion_response(input_data)
            
            self.log(f"Generated response ({len(response)} characters)")
            
            return response
            
        except Exception as e:
            self.log(f"Error in discussion: {str(e)}")
            return "I'm sorry, I had trouble processing your question. Could you please try asking it differently?"
    
    def _generate_discussion_response(self, question: str) -> str:
        """Generate a conversational response using GPT-4."""
        
        system_prompt = DISCUSSION_SYSTEM_PROMPT

        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": question}
                ],
                temperature=0.7,
                max_tokens=250  # Keep responses concise for voice
            )
            
            answer = response.choices[0].message.content.strip()
            
            # Ensure response isn't too long for comfortable listening
            if len(answer) > 500:
                # Truncate and add continuation offer
                answer = answer[:400] + "... Would you like me to explain more about any specific part?"
            
            return answer
            
        except Exception as e:
            self.log(f"Error generating discussion response: {str(e)}")
            return "I encountered an issue while thinking about your question. Could you please try asking it again?"
    
    def handle_programming_question(self, question: str) -> str:
        """Handle specific programming-related questions."""
        
        programming_prompt = DISCUSSION_PROGRAMMING_PROMPT.format(question=question)

        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a helpful programming mentor speaking to a student. Be clear and encouraging."},
                    {"role": "user", "content": programming_prompt}
                ],
                temperature=0.6,
                max_tokens=200
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            self.log(f"Error in programming question: {str(e)}")
            return "That's a great programming question! Let me think... Could you ask it one more time? I want to make sure I give you the best answer."
