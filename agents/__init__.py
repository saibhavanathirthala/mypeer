"""
AI Pair Programming Multi-Agent Framework
Agents package containing all agent implementations.
"""

from .base_agent import BaseAgent
from .stt_agent import STTAgent
from .tts_agent import TTSPromptAgent
from .python_agent import ProgrammingAgent as PythonAgent
from .discussion_agent import DiscussionAgent
from .code_analysis_agent import CodeAnalysisAgent
from .coderabbit_agent import CodeRabbitAgent

__all__ = [
    'BaseAgent',
    'STTAgent',
    'TTSPromptAgent',
    'PythonAgent',
    'DiscussionAgent',
    'CodeAnalysisAgent',
    'CodeRabbitAgent'
]
