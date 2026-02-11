from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

HF_API_KEY = os.environ.get("HF_API_KEY")
MODEL = "mistralai/Mistral-7B-Instruct-v0.2"

@app.route("/lyra", methods=["POST"])
def lyra():
    data = request.json
    user_text = data.get("message", "")

    system_prompt = f"""
You are LYRA, a female Indian AI assistant.
Owner: Chaitu
Speak short, natural, voice-friendly replies.
Hindi/English mix allowed.
"""

    payload = {
        "inputs": system_prompt + "\nUser: " + user_text + "\nLYRA:",
        "parameters": {"max_new_tokens": 120}
    }

    headers = {
        "Authorization": f"Bearer {HF_API_KEY}"
    }

    response = requests.post(
        f"https://api-inference.huggingface.co/models/{MODEL}",
        headers=headers,
        json=payload
    )

    result = response.json()

    if isinstance(result, dict) and result.get("error"):
        return jsonify({"reply": "Model is loading. Try again."})

    reply = result[0]["generated_text"].split("LYRA:")[-1].strip()

    return jsonify({"reply": reply})


if __name__ == "__main__":
    app.run()
