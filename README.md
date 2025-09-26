# MyPeer - AI Pair Programming Framework

# Move over BlackBerry, BlueBerry is the new tech fruit!"

A LangGraph-powered multi-agent system for voice-controlled pair programming with universal code generation and AI code review capabilities.

<div align="center">
  <img src="https://avatars.githubusercontent.com/u/132028505?s=280&v=4" alt="CodeRabbit AI" width="200" height="100">
  <p><em>Powered by CodeRabbit AI for intelligent code review</em></p>
</div>

## Key Features

- **Voice-Controlled Interface**: Complete hands-free operation with wake-up word detection
- **Universal Code Generation**: Supports 20+ programming languages including Python, JavaScript, Java, C++, Go, Rust, and more
- **AI Code Review**: Integrated CodeRabbit AI for automated code analysis and feedback
- **Intent Classification**: Smart routing between coding, discussion, file operations, and code analysis
- **Continuous Sessions**: Persistent voice sessions with session management
- **Multi-Modal Workflow**: Seamless integration of speech-to-text, text-to-speech, and code generation

## Architecture

### Core Components

**LangGraph Pipeline**: Orchestrates the complete voice-to-code workflow using state management and agent coordination.

**Voice Interface**: 
- Wake-up word detection ("Blueberry") for session initiation
- Continuous voice input capture with silence detection
- Speech-to-text conversion using OpenAI Whisper
- Text-to-speech responses for natural interaction

**Agent System**:
- **Intent Agent**: Classifies user requests (coding, discussion, file operations, code analysis)
- **Discussion Agent**: Handles programming questions and explanations
- **Code Analysis Agent**: Reviews and explains existing code
- **File Agent**: Manages file operations and workspace navigation
- **Python Agent**: Generates Python code with best practices
- **CodeRabbit Agent**: Provides AI-powered code review and feedback

**Universal Code Generation**: Supports 20+ programming languages with automatic file extension detection and language-specific optimizations.

## Quick Start

### Prerequisites
- Python 3.8+
- OpenAI API key
- Porcupine API key (optional, for wake-up word detection)

### Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd mypeer
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   ```bash
   # Create .env file with:
   OPENAI_API_KEY=your_openai_api_key
   PORCUPINE_ACCESS_KEY=your_porcupine_key  # Optional
   ```

### Usage

```bash
python main_langgraph.py
```

The system will:
1. Initialize the LangGraph voice pipeline
2. Wait for wake-up word "Blueberry" to start a session
3. Capture voice input and convert to text
4. Classify intent and route to appropriate agent
5. Generate code or provide responses
6. Continue listening for additional requests

## Setup Guide

### 1. Environment Setup

Create a `.env` file in the project root:
```bash
# Required
OPENAI_API_KEY=your_openai_api_key_here

# Optional (for wake-up word detection)
PORCUPINE_ACCESS_KEY=your_porcupine_key_here
```

### 2. Install Dependencies

```bash
# Install Python dependencies
pip install -r requirements.txt

# For macOS users (if you encounter audio issues)
brew install portaudio

# For Linux users (if you encounter audio issues)
sudo apt-get install libasound2-dev
```

### 3. Test Audio Setup

```bash
# Test microphone access
python -c "import sounddevice; print('Microphone detected:', sounddevice.query_devices())"

# Test audio playback
python -c "import pygame; pygame.mixer.init(); print('Audio system ready')"
```

## How to Use

### Starting a Session

1. **Run the application:**
   ```bash
   python main_langgraph.py
   ```

2. **Wait for wake-up word:** Say "Blueberry" to activate the system

3. **Speak your request:** The system will capture your voice automatically

4. **Confirm understanding:** The system will repeat what it heard and ask for confirmation

5. **Get results:** Receive code generation, explanations, or file operations

### Voice Commands

| **Intent** | **Example Commands** | **Expected Output** |
|------------|---------------------|-------------------|
| **Code Generation** | "Create a binary search function" | Generated code file with documentation |
| **Code Review** | "Review my code" | CodeRabbit AI analysis with suggestions |
| **Discussion** | "What is recursion?" | Detailed explanation with examples |
| **File Operations** | "Open main.py" | File opened in default editor |
| **Code Analysis** | "Explain this function" | Code explanation and documentation |

### Session Management

- **Continue Session:** Say "yes" when asked for more help
- **End Session:** Say "I don't want any help" to end current session
- **New Session:** Say "Blueberry" to start a new session

## Expected Outputs

### Code Generation Output

When you request code generation, the system will:

1. **Confirm the request** via voice
2. **Generate the code** with proper documentation
3. **Save to file** (e.g., `pair_program.py`)
4. **Announce completion** via voice
5. **Ask for additional help**

Example generated code:
```python
"""
Generated by MyPeer AI Pair Programming Framework
File: pair_program.py
Generated at: 2024-01-15 10:30:00
"""

def binary_search(arr, target):
    """
    Perform binary search on a sorted array.
    
    Args:
        arr: Sorted list of integers
        target: Value to search for
        
    Returns:
        Index of target if found, -1 otherwise
    """
    left, right = 0, len(arr) - 1
    
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1

if __name__ == "__main__":
    # Example usage
    numbers = [1, 3, 5, 7, 9, 11, 13]
    result = binary_search(numbers, 7)
    print(f"Found at index: {result}")
```

### CodeRabbit AI Review Output

When you request code review:

1. **Voice confirmation:** "I'll review your code using CodeRabbit AI"
2. **Analysis processing:** CodeRabbit analyzes the code
3. **Voice feedback:** Spoken summary of findings
4. **Detailed report:** Written analysis with suggestions

Example review output:
```
CodeRabbit AI Review Summary:
- Code Quality: Good (8.5/10)
- Issues Found: 2 minor suggestions
- Performance: Optimal for the use case
- Documentation: Well documented
- Security: No security concerns

Suggestions:
1. Consider adding type hints for better code clarity
2. Add input validation for edge cases
```

### Discussion Mode Output

For programming questions:

1. **Voice response:** Detailed explanation
2. **Examples:** Code examples when relevant
3. **Best practices:** Additional insights
4. **Follow-up:** Opportunity to ask related questions

### File Operations Output

For file operations:

1. **Confirmation:** "Opening main.py in your default editor"
2. **Action performed:** File opened/read/listed
3. **Status update:** Success/failure notification
4. **Content display:** File contents read aloud (if requested)

## Supported Languages

**Programming Languages**: Python, JavaScript, Java, C++, C#, Go, Rust, PHP, Ruby, Swift, Kotlin, TypeScript

**Web Technologies**: HTML, CSS, SQL

**Scripting & Configuration**: Bash, PowerShell, YAML, JSON, XML

## Voice Commands

| **Command** | **Action** |
|-------------|------------|
| "Create a sorting function" | Generates code in detected language |
| "What is recursion?" | Provides programming explanations |
| "Open main.py" | File operations and navigation |
| "Review my code" | CodeRabbit AI code review |
| "Explain this function" | Code analysis and explanation |
| "I don't want any help" | End current session |

## Workflow

1. **Wake-up Detection**: System waits for "Blueberry" wake-up word
2. **Voice Input**: Captures speech with automatic silence detection
3. **Speech-to-Text**: Converts voice to text using OpenAI Whisper
4. **Intent Classification**: Determines user intent (coding, discussion, file ops, analysis)
5. **Agent Routing**: Routes to appropriate specialized agent
6. **Response Generation**: Generates code, explanations, or performs operations
7. **Voice Feedback**: Provides spoken responses via text-to-speech
8. **Session Continuation**: Asks for additional help or ends session

## Project Structure

```
mypeer/
├── agents/
│   ├── base_agent.py          # Abstract base class for all agents
│   ├── stt_agent.py           # Speech-to-text with voice detection
│   ├── tts_agent.py           # Text-to-speech responses
│   ├── intent_agent.py        # Intent classification and routing
│   ├── discussion_agent.py    # Programming Q&A and explanations
│   ├── file_agent.py          # File operations and workspace management
│   ├── code_analysis_agent.py # Code review and analysis
│   ├── coderabbit_agent.py    # AI code review integration
│   ├── python_agent.py        # Python code generation
│   └── todo_agent.py          # Task planning and organization
├── langgraph_pipeline.py      # Main LangGraph orchestration
├── main_langgraph.py          # Entry point for the application
├── prompts.py                 # Centralized prompt templates
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## Key Technologies

- **LangGraph**: State management and agent orchestration
- **OpenAI APIs**: GPT-4, Whisper (STT), TTS for natural language processing
- **Porcupine**: Wake-up word detection for hands-free activation
- **WebRTC VAD**: Voice activity detection for automatic recording
- **CodeRabbit AI**: Integrated code review and analysis

## Configuration

### Environment Variables
- `OPENAI_API_KEY`: Required for OpenAI API access
- `PORCUPINE_ACCESS_KEY`: Optional for wake-up word detection

### Dependencies
- OpenAI API for language models and speech processing
- LangGraph for workflow orchestration
- Porcupine for wake-up word detection
- WebRTC VAD for voice activity detection

## Collaborators

<div align="center">
  <img src="https://avatars.githubusercontent.com/u/132028505?s=280&v=4" alt="CodeRabbit AI" width="150" height="75">
</div>

**CodeRabbit AI** - Integrated AI code review and analysis system that provides automated code quality assessment, bug detection, and improvement suggestions within the pipeline workflow.

**Contributors** - Bhavana, Venkatachalam
## License

This project is open source and available under the MIT License.
