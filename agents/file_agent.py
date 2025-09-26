"""
File Operations Agent for opening and managing files.
Handles file-related voice commands like opening, reading, and editing files.
"""

import os
import subprocess
import platform
from pathlib import Path
from typing import Dict, Any, List
from .base_agent import BaseAgent


class FileAgent(BaseAgent):
    """Agent that handles file operations through voice commands."""
    
    def __init__(self, config: dict = None):
        super().__init__("FileAgent", config)
        self.workspace_path = Path.cwd()
    
    def run(self, input_data: Dict[str, Any]) -> str:
        """
        Handle file operation requests.
        
        Args:
            input_data: Dictionary with file operation details
            
        Returns:
            Status message about the file operation
        """
        try:
            action = input_data.get("action", "unknown")
            file_info = input_data.get("extracted_info", {})
            
            self.log(f"Processing file operation: {action}")
            
            if action == "open_file":
                return self._open_file(file_info)
            elif action == "read_file":
                return self._read_file(file_info)
            elif action == "list_files":
                return self._list_files(file_info)
            elif action == "show_file":
                return self._show_file_contents(file_info)
            else:
                return f"I'm not sure how to handle the file operation: {action}. Try asking me to 'open a file' or 'show me file contents'."
                
        except Exception as e:
            self.log(f"Error in file operation: {str(e)}")
            return "I had trouble with that file operation. Could you please try again?"
    
    def _extract_filename(self, text: str) -> str:
        """Extract filename from user request."""
        # Common file extensions to look for
        extensions = ['.py', '.js', '.html', '.css', '.txt', '.md', '.json', '.yml', '.yaml', '.xml']
        
        words = text.split()
        
        # Look for files with extensions
        for word in words:
            if any(word.lower().endswith(ext) for ext in extensions):
                return word
        
        # Look for common filenames
        common_files = ['main', 'index', 'app', 'config', 'requirements', 'readme']
        for word in words:
            if word.lower() in common_files:
                return word
        
        # Return the last word if nothing else found
        return words[-1] if words else ""
    
    def _find_file(self, filename: str) -> Path:
        """Find a file in the current workspace."""
        if not filename:
            return None
        
        # Try exact match first
        file_path = self.workspace_path / filename
        if file_path.exists():
            return file_path
        
        # Try with common extensions
        extensions = ['.py', '.js', '.html', '.css', '.txt', '.md', '.json']
        for ext in extensions:
            if not filename.endswith(ext):
                test_path = self.workspace_path / (filename + ext)
                if test_path.exists():
                    return test_path
        
        # Search recursively in workspace
        for file_path in self.workspace_path.rglob(f"*{filename}*"):
            if file_path.is_file():
                return file_path
        
        return None
    
    def _open_file(self, file_info: Dict[str, Any]) -> str:
        """Open a file in the default editor."""
        filename = file_info.get("filename", "")
        if not filename:
            # Try to extract from the original request
            filename = self._extract_filename(file_info.get("original_request", ""))
        
        if not filename:
            return "I need a filename to open. Please tell me which file you'd like to open."
        
        file_path = self._find_file(filename)
        
        if not file_path:
            return f"I couldn't find the file '{filename}' in the current workspace. Could you check the filename?"
        
        try:
            # Open file with default system editor
            if platform.system() == "Darwin":  # macOS
                subprocess.run(["open", str(file_path)], check=True)
            elif platform.system() == "Windows":
                subprocess.run(["start", str(file_path)], shell=True, check=True)
            else:  # Linux
                subprocess.run(["xdg-open", str(file_path)], check=True)
            
            self.log(f"Opened file: {file_path}")
            return f"Successfully opened {file_path.name} in your default editor."
            
        except subprocess.CalledProcessError as e:
            self.log(f"Error opening file: {e}")
            return f"I had trouble opening {file_path.name}. Please check if you have a default editor set up."
    
    def _read_file(self, file_info: Dict[str, Any]) -> str:
        """Read and return file contents."""
        filename = file_info.get("filename", "")
        if not filename:
            filename = self._extract_filename(file_info.get("original_request", ""))
        
        if not filename:
            return "Please tell me which file you'd like me to read."
        
        file_path = self._find_file(filename)
        
        if not file_path:
            return f"I couldn't find the file '{filename}'. Could you check the filename?"
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Limit content length for voice output
            if len(content) > 500:
                content = content[:500] + "... The file continues. Would you like me to open it for you instead?"
            
            self.log(f"Read file: {file_path}")
            return f"Here are the contents of {file_path.name}: {content}"
            
        except Exception as e:
            self.log(f"Error reading file: {e}")
            return f"I had trouble reading {file_path.name}. Please make sure it's a text file."
    
    def _show_file_contents(self, file_info: Dict[str, Any]) -> str:
        """Show file contents (same as read_file)."""
        return self._read_file(file_info)
    
    def _list_files(self, file_info: Dict[str, Any]) -> str:
        """List files in the current directory."""
        try:
            files = []
            for item in self.workspace_path.iterdir():
                if item.is_file() and not item.name.startswith('.'):
                    files.append(item.name)
            
            if not files:
                return "There are no files in the current directory."
            
            # Limit to first 10 files for voice output
            if len(files) > 10:
                file_list = ", ".join(files[:10])
                return f"Here are the first 10 files: {file_list}. There are {len(files)} files total."
            else:
                file_list = ", ".join(files)
                return f"Here are the files in the current directory: {file_list}."
                
        except Exception as e:
            self.log(f"Error listing files: {e}")
            return "I had trouble listing the files in the current directory."
    
    def extract_file_operation(self, user_request: str) -> Dict[str, Any]:
        """Extract file operation details from user request."""
        request_lower = user_request.lower()
        
        # Determine action
        if any(word in request_lower for word in ["open", "launch", "start"]):
            action = "open_file"
        elif any(word in request_lower for word in ["read", "show", "display", "contents"]):
            action = "show_file"
        elif any(word in request_lower for word in ["list", "files", "directory"]):
            action = "list_files"
        else:
            action = "open_file"  # Default
        
        # Extract filename
        filename = self._extract_filename(user_request)
        
        return {
            "action": action,
            "extracted_info": {
                "filename": filename,
                "original_request": user_request
            }
        }
