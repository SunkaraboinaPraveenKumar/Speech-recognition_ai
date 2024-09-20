from flask import Flask, request, render_template, jsonify
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

# Ensure that the correct API key is loaded
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize the model
model = genai.GenerativeModel("models/gemini-1.5-pro")

conversation_history = []

def voice_assistant(user_input):
    global conversation_history
    prompt = f"""
    You are an AI assistant in an engaging conversation with a user. The user just asked the following question:
    '{user_input}'
    Provide a direct and informative answer, focusing on the exact details the user is asking for. Avoid unnecessary elaboration or asking follow-up
    questions.
    """

    # Generate a response using the model
    response = model.generate_content(prompt).text
    conversation_history.append({
        'user': user_input,
        'ai': response
    })
    return response

app = Flask(__name__)

# Endpoints
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/process_voice", methods=['POST'])
def process_voice():
    user_input = request.json.get('user_input')
    response = voice_assistant(user_input)
    return jsonify({"response": response, 'conversation_history': conversation_history})

if __name__ == "__main__":
    app.run(debug=True)
