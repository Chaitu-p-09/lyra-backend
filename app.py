from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

GROQ_API_KEY = os.environ.get("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")

@app.route("/lyra", methods=["POST"])
def lyra():
    try:
        data = request.json
        user_text = data.get("message", "")

        system_prompt = """
You are LYRA, a female Indian AI assistant.
Owner: Chaitu.
Speak short, natural, voice-friendly replies.
Hindi/English mix allowed.
"""

        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "llama3-8b-8192",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_text}
                ]
            }
        )

        result = response.json()

        # Debug fallback
        if "choices" not in result:
            return jsonify({"reply": "Groq API error: " + str(result)})

        reply = result["choices"][0]["message"]["content"]

        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"reply": "Server error: " + str(e)})


if __name__ == "__main__":
    app.run()
