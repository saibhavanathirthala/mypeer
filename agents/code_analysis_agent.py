"""
Code Analysis Agent using GPT-4.
Explains, analyzes, and provides insights about selected code snippets.
"""

import os
import subprocess
import platform
from typing import Dict, Any
from openai import OpenAI
from .base_agent import BaseAgent
from prompts import (CODE_EXPLANATION_PROMPT, CODE_REVIEW_PROMPT, 
                     CODE_OPTIMIZATION_PROMPT, CODE_DEBUG_PROMPT, 
                     get_prompt_by_analysis_type, format_code_prompt)


class CodeAnalysisAgent(BaseAgent):
    """Agent that analyzes and explains code through voice."""
    
    def __init__(self, config: dict = None):
        super().__init__("CodeAnalysisAgent", config)
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    def run(self, input_data: Dict[str, Any]) -> str:
        """
        Analyze and explain code.
        
        Args:
            input_data: Dictionary containing code and analysis type
            
        Returns:
            Code explanation and analysis
        """
        try:
            code = input_data.get("code", "")
            analysis_type = input_data.get("analysis_type", "explain")
            language = input_data.get("language", "auto")
            
            if not code.strip():
                return "I don't see any code to analyze. Please make sure you've copied the code to your clipboard or provided it in another way."
            
            self.log(f"Analyzing {len(code)} characters of code ({analysis_type})")
            
            if analysis_type == "explain":
                return self._explain_code(code, language)
            elif analysis_type == "review":
                return self._review_code(code, language)
            elif analysis_type == "optimize":
                return self._suggest_optimizations(code, language)
            elif analysis_type == "debug":
                return self._debug_analysis(code, language)
            else:
                return self._explain_code(code, language)
                
        except Exception as e:
            self.log(f"Error in code analysis: {str(e)}")
            return "I encountered an issue while analyzing the code. Could you try again?"
    
    def _explain_code(self, code: str, language: str = "auto") -> str:
        """Explain what the code does in simple terms."""
        
        prompt = format_code_prompt(CODE_EXPLANATION_PROMPT, code, language)

        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert code analyst providing voice-friendly explanations."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            explanation = response.choices[0].message.content.strip()
            return explanation
            
        except Exception as e:
            self.log(f"Error generating code explanation: {str(e)}")
            return "I had trouble analyzing this code. Could you try selecting a smaller code snippet?"
    
    def _review_code(self, code: str, language: str = "auto") -> str:
        """Provide a code review with suggestions."""
        
        prompt = format_code_prompt(CODE_REVIEW_PROMPT, code, language)

        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a senior developer conducting a friendly code review."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.6,
                max_tokens=400
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            self.log(f"Error in code review: {str(e)}")
            return "I couldn't complete the code review. Please try again with the code snippet."
    
    def _suggest_optimizations(self, code: str, language: str = "auto") -> str:
        """Suggest performance and code optimizations."""
        
        prompt = format_code_prompt(CODE_OPTIMIZATION_PROMPT, code, language)

        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a performance optimization specialist providing voice-friendly advice."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.6,
                max_tokens=400
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            self.log(f"Error suggesting optimizations: {str(e)}")
            return "I couldn't analyze the code for optimizations. Please try again."
    
    def _debug_analysis(self, code: str, language: str = "auto") -> str:
        """Analyze code for potential bugs and issues."""
        
        prompt = format_code_prompt(CODE_DEBUG_PROMPT, code, language)

        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a debugging expert providing voice-friendly analysis."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                max_tokens=400
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            self.log(f"Error in debug analysis: {str(e)}")
            return "I couldn't complete the debugging analysis. Please try again."
    
    def get_clipboard_content(self) -> str:
        """Get code content from system clipboard."""
        try:
            if platform.system() == "Darwin":  # macOS
                result = subprocess.run(['pbpaste'], capture_output=True, text=True)
                return result.stdout
            elif platform.system() == "Windows":
                result = subprocess.run(['powershell', '-command', 'Get-Clipboard'], 
                                      capture_output=True, text=True)
                return result.stdout
            elif platform.system() == "Linux":
                try:
                    result = subprocess.run(['xclip', '-selection', 'clipboard', '-o'], 
                                          capture_output=True, text=True)
                    return result.stdout
                except FileNotFoundError:
                    # Try xsel if xclip not available
                    result = subprocess.run(['xsel', '--clipboard'], 
                                          capture_output=True, text=True)
                    return result.stdout
            else:
                return ""
                
        except Exception as e:
            self.log(f"Error reading clipboard: {str(e)}")
            return ""
    
    def detect_language(self, code: str) -> str:
        """Detect programming language from code snippet."""
        code_lower = code.lower().strip()
        
        # Simple language detection based on common patterns
        if 'def ' in code and 'import ' in code:
            return "python"
        elif 'function ' in code and ('{' in code or '=>' in code):
            return "javascript"
        elif 'public class ' in code or 'private ' in code:
            return "java"
        elif '#include' in code or 'int main(' in code:
            return "cpp"
        elif 'func ' in code and 'package ' in code:
            return "go"
        elif 'fn ' in code and 'let ' in code:
            return "rust"
        elif 'const ' in code and 'interface ' in code:
            return "typescript"
        elif 'SELECT ' in code_lower and 'FROM ' in code_lower:
            return "sql"
        else:
            return "auto"
    
    def extract_code_analysis_request(self, user_request: str) -> Dict[str, Any]:
        """Extract analysis details from user request."""
        request_lower = user_request.lower()
        
        # Determine analysis type
        if any(word in request_lower for word in ["review", "check", "critique"]):
            analysis_type = "review"
        elif any(word in request_lower for word in ["optimize", "improve", "better", "performance"]):
            analysis_type = "optimize"
        elif any(word in request_lower for word in ["debug", "bug", "error", "issue", "problem"]):
            analysis_type = "debug"
        else:
            analysis_type = "explain"  # Default
        
        # Get code from clipboard
        code = self.get_clipboard_content()
        language = self.detect_language(code) if code else "auto"
        
        return {
            "code": code,
            "analysis_type": analysis_type,
            "language": language,
            "original_request": user_request
        }
