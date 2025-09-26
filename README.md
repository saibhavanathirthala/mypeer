# AI Pair Programming Multi-Agent Framework

> **🚀 Enhanced Intelligent Version** - Now with smart intent detection, discussion mode, and file operations!

An intelligent Python-based multi-agent system that provides AI pair programming capabilities using OpenAI's APIs. The framework features **smart intent detection** and **dynamic agent routing** to handle discussion, coding, and file operations through **100% voice interaction** with zero typing required.

## 🌟 Key Features

- **🧠 Smart Intent Detection**: Automatically understands whether you want to discuss, code, or manage files
- **🎤 100% Voice Controlled**: Complete hands-free operation with automatic speech detection
- **💬 Discussion Mode**: Ask programming questions and get detailed explanations
- **💻 Coding Mode**: Generate code with intelligent planning and confirmations  
- **📁 File Operations**: Open, read, and manage files through voice commands
- **🔍 Code Analysis Mode**: Select any code and get explanations, reviews, optimizations, or debugging help
- **🔄 Continuous Operation**: Keeps listening until you say "thank you Pair Programming"
- **⚡ Dynamic Routing**: Intelligently routes requests to specialized agents

## 🧠 Intelligent Agents

### Core Agents

#### 1. Speech-to-Text Agent (STTAgent)
- Uses OpenAI Whisper API with **automatic voice activity detection**
- **Zero typing required** - starts recording when you speak, stops when you're silent
- Handles continuous listening for hands-free operation

#### 2. Text-to-Speech Agent (TTSPromptAgent)  
- Uses OpenAI TTS API for natural voice feedback
- Provides confirmations and responses through speech
- Supports continuous voice conversations

#### 3. Intent Classification Agent (IntentAgent) ⭐ **NEW**
- Uses GPT-4 to **intelligently understand** your voice commands
- Automatically detects whether you want to:
  - **Ask questions** (Discussion Mode)
  - **Write code** (Coding Mode) 
  - **Manage files** (File Operations Mode)
- Routes requests to appropriate specialized agents

### Specialized Agents

#### 4. Discussion Agent (DiscussionAgent) ⭐ **NEW**
- Handles programming questions and explanations
- Provides conversational responses optimized for voice
- Explains concepts, algorithms, and best practices

#### 5. File Operations Agent (FileAgent) ⭐ **NEW**
- Opens files in your default editor by voice command
- Reads and presents file contents through speech
- Lists directory contents and manages workspace files

#### 6. Code Analysis Agent (CodeAnalysisAgent) ⭐ **NEW**
- Explains what any code does in plain English
- Reviews code and suggests improvements
- Provides optimization recommendations
- Analyzes code for potential bugs and issues
- Supports multiple programming languages with auto-detection

#### 7. To-do List Agent (TodoAgent)
- Converts coding requests into structured action plans
- Used specifically in Coding Mode for complex projects
- Breaks down tasks into implementable steps

#### 8. Python Code Agent (PythonAgent)
- Generates clean, documented Python code
- Includes validation, error handling, and type hints
- Saves code to `pair_program.py` with timestamp

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- OpenAI API key

### Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd hacakthon-multi-agent
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your OpenAI API key:**
   ```bash
   cp .env.template .env
   # Edit .env and add your OpenAI API key
   ```

### Usage

#### Simple One-Command Start
```bash
python main.py
```

That's it! The system will:
1. 🗣️ **Welcome you** with voice instructions
2. 🎧 **Listen continuously** for your voice commands  
3. 🧠 **Automatically detect** your intent
4. 🔄 **Route to the appropriate mode**:
   - **Discussion**: Answer questions and explain concepts
   - **Coding**: Generate code with confirmations
   - **File Operations**: Open and manage files
   - **Code Analysis**: Explain, review, or debug existing code

#### Voice Commands Examples

| **What You Say** | **Mode Activated** | **What Happens** |
|-----------------|------------------|------------------|
| *"What is recursion?"* | 💬 Discussion | Explains programming concepts |
| *"How does bubble sort work?"* | 💬 Discussion | Discusses algorithms |
| *"Create a sorting function"* | 💻 Coding | Generates code with confirmations |
| *"Build me a REST API"* | 💻 Coding | Creates structured code project |
| *"Open main.py"* | 📁 File Ops | Opens file in your editor |
| *"Show me config.py"* | 📁 File Ops | Reads file contents aloud |
| *"Explain this code"* | 🔍 Code Analysis | Explains copied code in detail |
| *"Review my function"* | 🔍 Code Analysis | Provides code review and suggestions |
| *"Debug this code"* | 🔍 Code Analysis | Analyzes for bugs and issues |
| *"Thank you Pair Programming"* | 👋 Exit | Ends the session gracefully |

## 🔄 Intelligent Workflow

The framework uses **smart intent detection** and **dynamic routing**:

### Universal Flow
1. **🎧 Voice Input** → STT Agent captures your speech automatically
2. **🧠 Intent Detection** → Intent Agent analyzes and classifies your request  
3. **🎯 Smart Routing** → System routes to the appropriate mode

### Mode-Specific Workflows

#### 💬 Discussion Mode
- **Discussion Agent** → Generates informative response
- **TTS Agent** → Speaks answer back to you
- **🔄 Continue** → Ready for next request

#### 💻 Coding Mode  
- **TTS Agent** → Confirms coding request
- **Todo Agent** → Creates structured plan (if complex)
- **Python Agent** → Generates and validates code
- **TTS Agent** → Announces completion
- **🔄 Continue** → Ready for next request

#### 📁 File Operations Mode
- **File Agent** → Executes file operation (open/read/list)
- **TTS Agent** → Reports results
- **🔄 Continue** → Ready for next request

### Key Features
- **🎤 Zero Typing**: Everything is voice-controlled
- **🧠 Context Aware**: Understands natural language
- **🔄 Continuous**: Keeps listening until you say "thank you Pair Programming"
- **⚡ Fast**: Direct routing to appropriate agents

## 📁 Project Structure

```
hacakthon-multi-agent/
├── agents/
│   ├── __init__.py
│   ├── base_agent.py          # Abstract base class
│   ├── stt_agent.py           # Speech-to-Text with voice detection
│   ├── tts_agent.py           # Text-to-Speech responses
│   ├── intent_agent.py        # ⭐ Intent classification & routing
│   ├── discussion_agent.py    # ⭐ Question answering & explanations  
│   ├── file_agent.py          # ⭐ File operations & management
│   ├── todo_agent.py          # To-do list generation (coding mode)
│   └── python_agent.py        # Python code generation
├── main.py                    # Intelligent orchestrator with dynamic routing
├── requirements.txt           # Dependencies (includes voice detection libs)
├── .env.template             # Environment variables template
├── pair_program.py           # Generated code output
└── README.md                 # This file
```

## 🎯 Example Sessions

### 💬 Discussion Mode Example
```
🤖 AI Pair Programming Framework - INTELLIGENT VOICE
🎧 Listening for your next request...
📝 Understood: 'What is the difference between recursion and iteration?'

🧠 Analyzing your request...
🎯 Detected intent: discussion (confidence: 0.95)
💬 Discussion Mode: User wants explanation

[TTS] Recursion and iteration are both ways to repeat operations, but they work differently. 
      Recursion calls itself with smaller problems, while iteration uses loops. 
      Recursion is elegant for tree-like problems, but iteration is usually more memory efficient...

✅ Discussion completed
------------------------------------------------------------
```

### 💻 Coding Mode Example  
```
🎧 Listening for your next request...
📝 Understood: 'Create a binary search function'

🧠 Analyzing your request...
🎯 Detected intent: coding (confidence: 0.92)
💻 Coding Mode: User wants code generation

🔄 Confirming coding request...
[TTS] So you are asking me to Create a binary search function, am I correct?
🎧 Say 'yes' or 'no' when ready...
📝 Transcribed: 'Yes, that's correct'

📋 Creating your coding plan...
⚡ Generating your code...
[TTS] Perfect! I've generated your code and saved it to pair_program.py. The code is ready to run!

✅ Code generated: /path/to/pair_program.py
------------------------------------------------------------
```

### 📁 File Operations Example
```
🎧 Listening for your next request...
📝 Understood: 'Open the main.py file'

🧠 Analyzing your request...
🎯 Detected intent: file_operations (confidence: 0.88)
📁 File Operations Mode: User wants file management

[TTS] Successfully opened main.py in your default editor.

✅ File operation completed
------------------------------------------------------------
```

## 🔧 Configuration

### Environment Variables
- `OPENAI_API_KEY`: Your OpenAI API key (required)

### Agent Configuration
Each agent can be configured via the config dictionary:

```python
# Example: Custom output file for Python agent
python_agent = PythonAgent(config={'output_file': 'my_code.py'})
```

## 🎨 Extensibility

The framework is designed for easy extension. To add new agents:

1. **Inherit from BaseAgent:**
   ```python
   from agents.base_agent import BaseAgent
   
   class DebugAgent(BaseAgent):
       def run(self, input_data):
           # Your implementation
           pass
   ```

2. **Add to orchestrator workflow**
3. **Update `agents/__init__.py`**

### Suggested Extensions
- **DebugAgent**: Automated debugging assistance
- **TestingAgent**: Generate unit tests
- **DocumentationAgent**: Create code documentation
- **RefactorAgent**: Code refactoring suggestions

## 🛠️ Technical Details

### Dependencies
- `openai>=1.0.0`: OpenAI API client (Whisper, GPT-4, TTS)
- `pygame>=2.5.0`: Audio playback for TTS
- `sounddevice>=0.5.0`: Microphone recording for voice input
- `scipy>=1.10.0`: Audio processing for voice detection
- `webrtcvad>=2.0.10`: Voice activity detection for automatic recording
- `numpy>=1.20.0`: Numerical processing for audio data
- `python-dotenv>=1.0.0`: Environment variable management

### API Usage
- **Whisper API**: Real-time speech-to-text transcription with voice activity detection
- **GPT-4**: 
  - Intent classification and request routing
  - Programming question answers and explanations
  - To-do list generation for coding projects
  - Python code generation with best practices
- **TTS API**: Natural voice synthesis for responses and confirmations

### Voice Features
- **Automatic Voice Detection**: Starts recording when you speak
- **Silence Detection**: Stops recording after 1.5 seconds of silence  
- **Continuous Listening**: No need to press buttons or type
- **Natural Language**: Understands conversational requests
- **Multi-Modal**: Seamlessly switches between discussion, coding, and file operations

## ⭐ What Makes This Special

### 🧠 Intelligent Intent Detection
Unlike simple voice assistants, this framework **understands context** and automatically routes your requests to the right specialized agent. No need to specify modes or commands - just speak naturally.

### 🎤 True Zero-Typing Experience  
Complete hands-free operation with:
- **Automatic speech detection** (no button pressing)
- **Voice confirmations** (speak "yes" or "no")
- **Spoken responses** (hear answers, not just text)
- **Smart exit phrase** ("thank you Pair Programming")

### 🔄 Three Integrated Modes
1. **💬 Discussion**: Ask programming questions, get explanations
2. **💻 Coding**: Generate code with intelligent planning
3. **📁 File Operations**: Manage your workspace by voice

### 🚀 Production Ready
- **Robust error handling** with graceful fallbacks
- **Code validation** ensures generated code runs
- **Modular architecture** for easy extension
- **Professional documentation** and type hints

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add your improvements
4. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 🐛 Troubleshooting

### Common Issues

**"OPENAI_API_KEY not found"**
- Ensure you've created a `.env` file with your API key
- Verify the key is valid and has sufficient credits
- Alternative: Set environment variable: `export OPENAI_API_KEY="your_key"`

**Audio/Voice Issues**
- **No microphone detected**: Check system permissions for microphone access
- **Audio playback problems**: Install pygame: `pip install pygame`
- **Voice detection not working**: Install voice dependencies: `pip install sounddevice webrtcvad scipy`
- **On macOS**: You may need: `brew install portaudio` for sounddevice
- **On Linux**: Install ALSA development headers: `sudo apt-get install libasound2-dev`

**Import/Installation Errors**
- **ModuleNotFoundError**: Ensure all requirements installed: `pip install -r requirements.txt`
- **Permission errors**: Try with user install: `pip install --user -r requirements.txt`
- **Version conflicts**: Use virtual environment: `python -m venv venv && source venv/bin/activate`

**Voice Recognition Issues**
- **Low confidence detection**: Speak clearly and closer to microphone
- **Background noise**: Use in quiet environment for better voice detection
- **Wrong intent detected**: Try rephrasing your request more explicitly
- **Not responding to voice**: Check if `webrtcvad` installed correctly

**Performance Issues**
- **Slow responses**: Ensure stable internet connection for OpenAI API calls
- **Memory usage**: Voice detection libraries may use more RAM than expected
- **API timeouts**: Check OpenAI API status and rate limits

## 🎉 Demo Output

The framework generates clean, documented Python code. Example output for factorial:

```python
"""
Generated by AI Pair Programming Multi-Agent Framework
File: pair_program.py
Generated at: 2025-09-26 10:30:00
"""

def factorial(n: int) -> int:
    """
    Calculate the factorial of a number using recursion.
    
    Args:
        n: Non-negative integer to calculate factorial for
        
    Returns:
        The factorial of n
        
    Raises:
        ValueError: If n is negative
        TypeError: If n is not an integer
    """
    if not isinstance(n, int):
        raise TypeError("Input must be an integer")
    
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    
    # Base case
    if n <= 1:
        return 1
    
    # Recursive case  
    return n * factorial(n - 1)


if __name__ == "__main__":
    # Example usage
    print(f"factorial(5) = {factorial(5)}")  # Output: 120
    print(f"factorial(0) = {factorial(0)}")  # Output: 1
```
