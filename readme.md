Here's a comprehensive README.md for your project:

```markdown
# ⚡ Thoughtful Lightning - Dual-Engine AI Assistant

A sophisticated AI assistant combining DeepSeek's reasoning capabilities with Groq's ultra-fast inference, packaged in an intuitive Gradio interface.

## 🌟 Features

- **Dual-Engine Architecture**
  - First-stage reasoning with DeepSeek R1
  - Second-stage response generation with Groq's Llama-3 70B
- **Enterprise-Grade Security**
  - Environment variable support (.env file)
  - Encrypted password fields for API keys
  - Automatic validation of credentials
- **Advanced UI Features**
  - Streaming responses with partial output rendering
  - Collapsible settings panel
  - Reasoning step visualization
  - Pre-built example queries
- **Error Resilience**
  - Graceful API error handling
  - Missing key detection
  - Automatic .env file creation
- **Modern Tooling**
  - PEP 723 inline dependencies
  - Compatible with `uv run`
  - Python 3.12+ optimized

## 📦 Installation

1. **Prerequisites**
   - Python 3.12+
   - [uv](https://github.com/astral-sh/uv) package manager

2. **Quick Start**
```bash
# Clone repository (if applicable)
git clone https://github.com/martinbowling/thoughtful-lightning.git
cd thoughtful-lightning

# Run with uv
uv run thoughtful-lightning.py
```

## 🔧 Configuration

### API Keys Setup
1. **Environment Variables (Recommended)**
   ```bash
   # Create .env file
   touch .env
   ```
   Add your credentials:
   ```env
   DEEPSEEK_API_KEY=your_key_here
   GROQ_API_KEY=your_key_here
   ```

2. **UI Configuration**
   - Click the ⚙️ Settings button
   - Enter keys in the password fields
   - Click Close when done

### Dependency Management
The script uses PEP 723 inline requirements:
```python
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "gradio>=4.25.0",
#     "requests>=2.32.2",
#     "groq>=0.5.0",
#     "python-dotenv>=1.0.0",
# ]
# ///
```

## 🚀 Usage

1. **Launch Interface**
   ```bash
   uv run thoughful-lightning.py
   ```
   The app will launch at `http://localhost:7860`

2. **Basic Workflow**
   - Enter query in chat input
   - System processes through DeepSeek (reasoning stage)
   - Groq generates final response (execution stage)
   - Click 🧐 Show Reasoning to view thought process

3. **Example Queries**
   - "Explain quantum entanglement using cooking analogies"
   - "How to optimize Python code for machine learning?"
   - "Compare blockchain and traditional databases"

## 🧠 Technical Details

### Reasoning Pipeline
1. **DeepSeek Processing**
   - API: `deepseek-reasoner` model
   - Stream: Enabled
   - Max Tokens: 1 (forces reasoning content extraction)
   - Output: Aggregated `reasoning_content` chunks

2. **Groq Execution**
   - Model: `llama-3.3-70b-specdec`
   - Temperature: 0.7 (balanced creativity/accuracy)
   - Max Tokens: 1024
   - Prompt Structure:
     ```xml
     <user_query>{original query}</user_query>
     <reasoning>{extracted steps}</reasoning>
     ```

### Error Handling
- **Missing Keys Detection**
  - Checks both environment and UI inputs
  - Provides clear error messages
- **API Failure Modes**
  - DeepSeek errors: Preserved in chat history
  - Groq errors: Displayed with traceback
  - Network issues: Automatic retries

## 🛠 Troubleshooting

**Common Issues**
```bash
# Missing .env file
ERROR: No API keys found in environment variables

# Solution
touch .env && echo "DEEPSEEK_API_KEY=\nGROQ_API_KEY=" > .env
```

```bash
# Dependency conflicts
ERROR: Cannot install package versions

# Solution
uv venv && uv pip install --reinstall -r requirements.txt
```

**Performance Tips**
- Use Groq's `specdec` model for fastest inference
- Keep DeepSeek's `max_tokens=1` for pure reasoning
- Enable streaming for real-time interaction

## 📄 License

MIT License - See [LICENSE](LICENSE) for details


This README provides:
1. Comprehensive feature breakdown
2. Clear installation/configuration instructions
3. Detailed technical specifications
4. Troubleshooting guide
5. Security best practices
6. Performance optimization tips

Would you like me to add any specific sections or modify existing content?