#!/usr/bin/env python3
"""
CodeRabbit Agent for Code Review
Integrates CodeRabbit CLI for AI-powered code reviews
"""

import os
import subprocess
import tempfile
from typing import Dict, List, Optional
from .base_agent import BaseAgent
from prompts import (
    CODERABBIT_SUMMARIZATION_PROMPT,
    CODERABBIT_RATE_LIMIT_MESSAGE,
    CODERABBIT_TIMEOUT_MESSAGE
)


class CodeRabbitAgent(BaseAgent):
    """CodeRabbit Agent for AI-powered code reviews using CodeRabbit CLI"""
    
    def __init__(self, config: dict = None):
        super().__init__("CodeRabbitAgent", config)
        self.coderabbit_path = self._find_coderabbit_path()
        
    def _find_coderabbit_path(self) -> str:
        """Find CodeRabbit CLI path"""
        try:
            # Try to find coderabbit in PATH
            result = subprocess.run(['which', 'coderabbit'], 
                                 capture_output=True, text=True, check=True)
            return result.stdout.strip()
        except subprocess.CalledProcessError:
            # Fallback to common installation paths
            possible_paths = [
                os.path.expanduser("~/.local/bin/coderabbit"),
                "/usr/local/bin/coderabbit",
                "/opt/homebrew/bin/coderabbit"
            ]
            
            for path in possible_paths:
                if os.path.exists(path):
                    return path
            
            # If not found, return 'coderabbit' and let subprocess handle it
            return "coderabbit"
    
    def run(self, input_data: str) -> str:
        """
        Run CodeRabbit review on the provided code or file path.
        
        Args:
            input_data: File path to review or code content
            
        Returns:
            CodeRabbit review results
        """
        try:
            self.log(f"Running CodeRabbit review on: {input_data}")
            
            # Check if input is a file path or code content
            if os.path.exists(input_data):
                # It's a file path
                return self._review_file(input_data)
            else:
                # It's code content, save to temp file and review
                return self._review_code_content(input_data)
                
        except Exception as e:
            self.log(f"Error in CodeRabbit review: {str(e)}")
            return f"CodeRabbit review failed: {str(e)}"
    
    def _review_file(self, file_path: str) -> str:
        """Review a specific file using CodeRabbit CLI"""
        try:
            # Change to the directory containing the file
            file_dir = os.path.dirname(os.path.abspath(file_path))
            
            # Check if it's a git repository, if not initialize one
            if not os.path.exists(os.path.join(file_dir, '.git')):
                self.log("Initializing git repository for CodeRabbit...")
                subprocess.run(['git', 'init'], cwd=file_dir, capture_output=True)
                subprocess.run(['git', 'add', '.'], cwd=file_dir, capture_output=True)
                subprocess.run(['git', 'commit', '-m', 'Initial commit for CodeRabbit review'], 
                             cwd=file_dir, capture_output=True)
            
            # Run CodeRabbit review with shorter timeout
            cmd = [self.coderabbit_path, "review", "--plain"]
            
            result = subprocess.run(
                cmd,
                cwd=file_dir,
                capture_output=True,
                text=True,
                timeout=300
            )
            
            if result.returncode == 0:
                self.log("CodeRabbit review completed successfully")
                return result.stdout
            else:
                self.log(f"CodeRabbit review failed: {result.stderr}")
                return f"CodeRabbit review failed: {result.stderr}"
                
        except subprocess.TimeoutExpired:
            self.log("CodeRabbit review timed out")
            return "CodeRabbit review timed out. Please try again."
        except Exception as e:
            self.log(f"Error running CodeRabbit review: {str(e)}")
            return f"Error running CodeRabbit review: {str(e)}"
    
    def _review_code_content(self, code_content: str) -> str:
        """Review code content by saving to temp file"""
        try:
            # Create a temporary file with the code content
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as temp_file:
                temp_file.write(code_content)
                temp_path = temp_file.name
            
            # Review the temporary file
            result = self._review_file(temp_path)
            
            # Clean up temporary file
            os.unlink(temp_path)
            
            return result
            
        except Exception as e:
            self.log(f"Error reviewing code content: {str(e)}")
            return f"Error reviewing code content: {str(e)}"
    
    def review_generated_code(self, code_file_path: str) -> Dict[str, str]:
        """
        Review generated code and return structured results.
        
        Args:
            code_file_path: Path to the generated code file
            
        Returns:
            Dictionary with review results
        """
        try:
            self.log(f"Reviewing generated code: {code_file_path}")
            
            # Run CodeRabbit review
            review_output = self.run(code_file_path)
            
            # Parse the review output
            review_summary = self._parse_review_output(review_output)
            
            return {
                "review_output": review_output,
                "summary": review_summary,
                "file_path": code_file_path,
                "status": "completed"
            }
            
        except Exception as e:
            self.log(f"Error in code review: {str(e)}")
            return {
                "review_output": f"Code review failed: {str(e)}",
                "summary": "Code review could not be completed",
                "file_path": code_file_path,
                "status": "error"
            }
    
    def review_current_directory(self) -> Dict[str, str]:
        """
        Review all code in current directory using CodeRabbit CLI.
        
        Returns:
            Dictionary with review results
        """
        try:
            self.log("Reviewing current directory with CodeRabbit...")
            print(f" Running CodeRabbit CLI command: {self.coderabbit_path} review --plain")
            
            # Run CodeRabbit review on current directory
            result = subprocess.run(
                [self.coderabbit_path, "review", "--plain"],
                capture_output=True,
                text=True,
                timeout=120  # 2 minute timeout
            )
            
            print(f" CodeRabbit CLI completed with return code: {result.returncode}")
            if result.stdout:
                print(f" CodeRabbit stdout: {result.stdout[:200]}...")
            if result.stderr:
                print(f" CodeRabbit stderr: {result.stderr[:200]}...")
            
            if result.returncode == 0:
                self.log("CodeRabbit review completed successfully")
                review_output = result.stdout
                
                # Use GPT-4 to summarize the review
                summary = self._summarize_with_gpt4(review_output)
                
                return {
                    "review_output": review_output,
                    "summary": summary,
                    "status": "completed"
                }
            else:
                # Check for rate limit error
                if "Rate limit exceeded" in result.stderr:
                    self.log("CodeRabbit rate limit exceeded")
                    return {
                        "review_output": "Rate limit exceeded error",
                        "summary": "Rate limit exceeded error",
                        "status": "rate_limited"
                    }
                else:
                    self.log(f"CodeRabbit review failed: {result.stderr}")
                    return {
                        "review_output": result.stderr,
                        "summary": "CodeRabbit review failed",
                        "status": "error"
                    }
                
        except subprocess.TimeoutExpired:
            self.log("CodeRabbit review timed out")
            return {
                "review_output": "Rate limit exceeded error",
                "summary": "Rate limit exceeded error",
                "status": "timeout"
            }
        except Exception as e:
            self.log(f"Error in directory review: {str(e)}")
            return {
                "review_output": "Rate limit exceeded error",
                "summary": "Rate limit exceeded error",
                "status": "error"
            }
    
    def _summarize_with_gpt4(self, review_output: str) -> str:
        """Use GPT-4 to summarize CodeRabbit review output"""
        try:
            from langchain_openai import ChatOpenAI
            
            # Use prompt from prompts.py
            prompt = CODERABBIT_SUMMARIZATION_PROMPT.format(review_output=review_output)
            
            # Use GPT-4 for summarization
            llm = ChatOpenAI(model="gpt-4", temperature=0.3)
            result = llm.invoke(prompt)
            
            return result.content.strip()
            
        except Exception as e:
            self.log(f"Error in GPT-4 summarization: {str(e)}")
            # Fallback to simple summarization
            return self._simple_summarize(review_output)
    
    def _simple_summarize(self, review_output: str) -> str:
        """Simple fallback summarization"""
        lines = review_output.split('\n')
        critical_issues = []
        
        for line in lines:
            if 'Type: potential_issue' in line or 'Type: bug' in line:
                # Extract the comment from the next few lines
                for i, next_line in enumerate(lines[lines.index(line):lines.index(line)+10]):
                    if 'Comment:' in next_line:
                        comment = next_line.replace('Comment:', '').strip()
                        if comment and len(comment) > 10:
                            critical_issues.append(comment[:100] + "..." if len(comment) > 100 else comment)
                        break
        
        if critical_issues:
            return f"Um, I found {len(critical_issues)} critical issues. Hmm, the main ones are: {critical_issues[0]}"
        else:
            return "Um, the code review looks good overall, no critical issues found."
    
    def _parse_review_output(self, review_output: str) -> str:
        """Parse CodeRabbit review output to extract key insights"""
        try:
            # Extract key sections from the review
            lines = review_output.split('\n')
            summary_lines = []
            
            # Look for key sections
            in_summary = False
            for line in lines:
                if any(keyword in line.lower() for keyword in ['summary', 'overview', 'key findings']):
                    in_summary = True
                elif in_summary and line.strip():
                    if line.startswith('#'):  # End of summary section
                        break
                    summary_lines.append(line.strip())
            
            if summary_lines:
                return '\n'.join(summary_lines[:5])  # First 5 lines of summary
            else:
                # Fallback: return first few lines of the review
                return '\n'.join([line.strip() for line in lines[:10] if line.strip()])
                
        except Exception as e:
            self.log(f"Error parsing review output: {str(e)}")
            return "Review completed but summary could not be extracted."
    
    def get_review_suggestions(self, code_file_path: str) -> List[str]:
        """
        Get specific suggestions from CodeRabbit review.
        
        Args:
            code_file_path: Path to the code file
            
        Returns:
            List of improvement suggestions
        """
        try:
            review_output = self.run(code_file_path)
            
            # Extract suggestions from the review
            suggestions = []
            lines = review_output.split('\n')
            
            for line in lines:
                if any(keyword in line.lower() for keyword in ['suggest', 'recommend', 'consider', 'improve']):
                    suggestions.append(line.strip())
            
            return suggestions[:10]  # Return up to 10 suggestions
            
        except Exception as e:
            self.log(f"Error getting review suggestions: {str(e)}")
            return [f"Could not extract suggestions: {str(e)}"]
    
    def is_authenticated(self) -> bool:
        """Check if CodeRabbit is authenticated"""
        try:
            result = subprocess.run(
                [self.coderabbit_path, "auth", "status"],
                capture_output=True,
                text=True,
                timeout=10
            )
            return result.returncode == 0
        except:
            return False
    
    def authenticate(self) -> bool:
        """Authenticate with CodeRabbit"""
        try:
            self.log("Authenticating with CodeRabbit...")
            result = subprocess.run(
                [self.coderabbit_path, "auth", "login"],
                capture_output=True,
                text=True,
                timeout=30
            )
            return result.returncode == 0
        except Exception as e:
            self.log(f"Authentication failed: {str(e)}")
            return False
