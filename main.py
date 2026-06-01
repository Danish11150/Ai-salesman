import os
import json
import requests
from flask import Flask, request, jsonify
from website import website
from supabase import create_client


from lan.language import LANGUAGE_SYSTEM_PROMPT
from assets.personality import AI_PERSONALITY_PROMPT
from utils.error_handle import safe_extract_reply, safe_http_error, safe_exception
from utils.rate_limit import respect_rate_limit

app = Flask(__name__,
           static_url_path="/static",
    static_folder="website/static"
           )
app.register_blueprint(website, url_prefix="/")
app.secret_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJ5dm1xYmNzdHJsZ2dlemlrc291Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc4MDMwNTIyNiwiZXhwIjoyMDk1ODgxMjI2fQ.iJwrdLmZ38mK1c1QFTXLvKiAsj4dCzpfEGrkfXH9lqo"

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_URL = "https://api.deepseek.com/chat/completions"
DEEPSEEK_MODEL = "deepseek-chat"


def ai_agent_reply(user_message: str) -> str:
    user_message = str(user_message).strip() or "Hello"

    respect_rate_limit()

    payload = {
        "model": DEEPSEEK_MODEL,
        "messages": [
            {
                "role": "system",
                "content": LANGUAGE_SYSTEM_PROMPT + "\n\n" + AI_PERSONALITY_PROMPT
            },
            {
                "role": "user",
                "content": user_message
            }
        ],
        "temperature": 0.7,
        "max_tokens": 300,
    }

    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json",
    }

    try:
        resp = requests.post(DEEPSEEK_URL, headers=headers, data=json.dumps(payload))

        if resp.status_code != 200:
            return safe_http_error(resp.status_code)

        data = resp.json()
        return safe_extract_reply(data)

    except Exception:
        return safe_exception()



@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")
    reply = ai_agent_reply(user_message)
    return jsonify({"reply": reply})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
