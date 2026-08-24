import os
from flask import Flask, request, render_template, jsonify, session
import requests
from dotenv import load_dotenv
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "supersecretkey")  # Use env var for security
CORS(app)

# OpenRouter / OpenAI-Compatible API Configuration
DEFAULT_API_URL = "https://openrouter.ai/api/v1/chat/completions"

def ask_doctor(prompt, conv_id):
    """Send user input to AI completion API and return formatted response"""
    api_key = (
        os.getenv("OPENROUTER_API_KEY") or 
        os.getenv("OPENAI_API_KEY") or 
        os.getenv("GROQ_API_KEY") or 
        os.getenv("GEMINI_API_KEY") or 
        os.getenv("AI_API_KEY")
    )
    if not api_key or api_key == "your_openrouter_api_key_here":
        return "Configuration Error: API key is not set. Please set OPENROUTER_API_KEY (or GROQ_API_KEY / OPENAI_API_KEY) in your .env file or environment variables."

    api_url = os.getenv("API_URL", DEFAULT_API_URL)
    model = os.getenv("MODEL", "openai/gpt-4o-mini")

    # Initialize session conversations
    if "conversations" not in session:
        session["conversations"] = []

    while len(session["conversations"]) <= conv_id:
        session["conversations"].append([])

    messages = session["conversations"][conv_id]

    # Append user message with instruction for medical context
    messages.append({
        "role": "user",
        "content": f"{prompt}\nRespond ONLY in medical context in this format:\n"
                   f"Symptoms:\nPossible Causes:\nRecommended Tests:\nAdvice:"
    })

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": model,
        "messages": messages,
        "max_tokens": 1000
    }

    try:
        response = requests.post(api_url, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 401:
            return "API Error (401 Unauthorized): Invalid or missing API key. Please check your API key."
        elif response.status_code == 402:
            return "API Error (402 Payment Required): Insufficient API credits/quota. Please add credits to your account."
        elif response.status_code == 429:
            return "API Error (429 Rate Limit/Quota Exceeded): Too many requests or quota limit reached."
        
        response.raise_for_status()  # Raise error for other bad status codes
        data = response.json()

        if "choices" in data and len(data["choices"]) > 0:
            answer = data["choices"][0]["message"]["content"]
        else:
            answer = "No response from AI. Please try again."

        # Append AI response
        messages.append({"role": "assistant", "content": answer})
        session["conversations"][conv_id] = messages
        return answer

    except requests.exceptions.RequestException as e:
        return f"API Error: {str(e)}"

@app.route("/")
def index():
    if "conversations" not in session:
        session["conversations"] = []
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    conv_id = data.get("conv_id", 0)
    user_input = data.get("message", "").strip()

    if not user_input:
        return jsonify({"answer": " Hello! I'm your AI Doctor."}), 400

    answer = ask_doctor(user_input, conv_id)
    return jsonify({"answer": answer})

if __name__ == "__main__":
    app.run(debug=True)
