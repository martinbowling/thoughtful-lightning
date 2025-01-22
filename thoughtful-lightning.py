# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "gradio>=4.25.0",
#     "requests>=2.32.2",
#     "groq>=0.5.0",
#     "python-dotenv>=1.0.0",
# ]
# ///

import gradio as gr
import requests
import json
import os
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize global variables
reasoning_history = []
ENV_DEEPSEEK_KEY = os.getenv("DEEPSEEK_API_KEY", "")
ENV_GROQ_KEY = os.getenv("GROQ_API_KEY", "")

def validate_keys(deepseek_key, groq_key):
    """Validate API keys and return appropriate message"""
    if not deepseek_key or not groq_key:
        missing = []
        if not deepseek_key:
            missing.append("DeepSeek")
        if not groq_key:
            missing.append("Groq")
        return False, f"Missing API key(s) for: {', '.join(missing)}. Please configure keys."
    return True, "Keys configured successfully!"

def process_deepseek(message, api_key):
    if not api_key:
        raise ValueError("DeepSeek API key not configured")
        
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "deepseek-reasoner",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": message}
        ],
        "stream": True,
        "max_tokens": 1
    }
    
    response = requests.post(
        "https://api.deepseek.com/chat/completions",
        headers=headers,
        json=data,
        stream=True
    )
    
    reasoning = []
    for line in response.iter_lines():
        if line:
            try:
                cleaned_line = line.decode('utf-8').replace('data: ', '').strip()
                if cleaned_line == '[DONE]':
                    continue
                chunk = json.loads(cleaned_line)
                if chunk.get('choices'):
                    content = chunk['choices'][0]['delta'].get('reasoning_content', '')
                    if content:
                        reasoning.append(content)
            except Exception as e:
                continue
    
    return ' '.join(reasoning)

def chat_fn(message, history, deepseek_key, groq_key):
    # Use environment variables if available, otherwise use UI inputs
    active_deepseek_key = ENV_DEEPSEEK_KEY or deepseek_key
    active_groq_key = ENV_GROQ_KEY or groq_key
    
    # Validate keys before processing
    is_valid, validation_message = validate_keys(active_deepseek_key, active_groq_key)
    if not is_valid:
        yield {"role": "assistant", "content": validation_message}
        return
    
    try:
        reasoning = process_deepseek(message, active_deepseek_key)
    except Exception as e:
        yield {"role": "assistant", "content": f"DeepSeek API Error: {str(e)}"}
        return
    
    reasoning_history.append(reasoning)
    
    groq_prompt = f"""You will be given a query and reasoning steps. 
    Review the reasoning, thinking through each of the steps and provide a concise answer to the user.
    
    <user_query>{message}</user_query>
    <reasoning>{reasoning}</reasoning>"""
    
    try:
        client = Groq(api_key=active_groq_key)
        groq_response = client.chat.completions.create(
            model="llama-3.3-70b-specdec",
            messages=[{"role": "user", "content": groq_prompt}],
            temperature=0.7,
            max_tokens=1024,
            top_p=1,
            stream=True,
        )
        
        accumulated_response = ""
        for chunk in groq_response:
            part = chunk.choices[0].delta.content or ""
            accumulated_response += part
            yield {"role": "assistant", "content": accumulated_response}
            
    except Exception as e:
        yield {"role": "assistant", "content": f"Groq API Error: {str(e)}"}

def show_reasoning():
    return reasoning_history[-1] if reasoning_history else "No reasoning available"

def toggle_reasoning_visibility(visible):
    return gr.update(visible=visible)

def show_settings():
    return gr.update(visible=True)

def hide_settings():
    return gr.update(visible=False)

# Create the Gradio interface
with gr.Blocks(theme=gr.themes.Soft(), title="Thoughtful Lightning") as demo:
    # Initialize error banner
    error_banner = gr.Markdown(visible=False)
    
    # Main Interface
    gr.Markdown("## ⚡ Thoughtful Lightning")
    gr.Markdown("*Powered by DeepSeek R1 reasoning and Groq's lightning-fast inference*")
    
    # Settings Group (Initially Hidden)
    with gr.Group(visible=False) as settings_group:
        gr.Markdown("### ⚙️ Settings")
        gr.Markdown("*Note: Environment variables will be used if available*")
        with gr.Row():
            with gr.Column(scale=1):
                deepseek_key = gr.Textbox(
                    label="DeepSeek API Key",
                    type="password",
                    value="",
                    placeholder="Enter DeepSeek API key" if not ENV_DEEPSEEK_KEY else "Using key from environment",
                    info="DeepSeek R1 API key for reasoning"
                )
                groq_key = gr.Textbox(
                    label="Groq API Key",
                    type="password",
                    value="",
                    placeholder="Enter Groq API key" if not ENV_GROQ_KEY else "Using key from environment",
                    info="Groq API key for fast inference"
                )
        with gr.Row():
            close_btn = gr.Button("Close")
            settings_status = gr.Markdown()
    
    with gr.Row():
        with gr.Column(scale=1):
            settings_btn = gr.Button("⚙️ Settings")
            reasoning_btn = gr.Button("🧐 Show Reasoning")
    
    with gr.Row():
        chat_interface = gr.ChatInterface(
            chat_fn,
            additional_inputs=[deepseek_key, groq_key],
            examples=[
                ["How many r's are in strawberry"],
                ["Which is greater 9.11 or 9.9"],
                ["Best way to learn Rust in 2024?"]
            ]
        )
    
    reasoning_output = gr.Textbox(
        label="Reasoning Steps",
        interactive=False,
        visible=False,
        lines=8,
        max_lines=12
    )
    
    # Event handlers
    settings_btn.click(
        fn=show_settings,
        outputs=[settings_group]
    )
    
    close_btn.click(
        fn=hide_settings,
        outputs=[settings_group]
    )
    
    reasoning_btn.click(
        fn=show_reasoning,
        outputs=reasoning_output
    ).then(
        fn=toggle_reasoning_visibility,
        inputs=[gr.State(True)],
        outputs=[reasoning_output]
    )

if __name__ == "__main__":
    # Create .env file if it doesn't exist
    if not os.path.exists(".env"):
        with open(".env", "w") as f:
            f.write("DEEPSEEK_API_KEY=\nGROQ_API_KEY=\n")
            
    # Show error if no keys are configured
    if not (ENV_DEEPSEEK_KEY or ENV_GROQ_KEY):
        print("\n⚠️  No API keys found in environment variables.")
        print("You can either:")
        print("1. Add them to your .env file")
        print("2. Configure them in the UI settings\n")
    
    demo.queue().launch()