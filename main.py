import os
import requests
import json

# 🔹 Import all modules
from lan.language import LANGUAGE_SYSTEM_PROMPT
from assets.personality import AI_PERSONALITY_PROMPT
from utils.error_handle import safe_extract_reply, safe_http_error, safe_exception
from utils.rate_limit import respect_rate_limit

# 🔹 DeepSeek configuration
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_URL = "https://api.deepseek.com/chat/completions"
DEEPSEEK_MODEL = "deepseek-chat"


def ai_agent_reply(user_message: str) -> str:
    """
    DeepSeek AI Agent — Phase 1 Final Version
    Features:
    - Multi-language detection
    - AI personality rules
    - Error-proof response handling
    - Rate-limit safe design
    """

    # 🧠 Step 1: Clean user message
    user_message = str(user_message).strip() or "Hello"

    # 🧠 Step 2: Respect rate limit before API call
    respect_rate_limit()

    # 🧠 Step 3: Prepare payload with system + user messages
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
        # 🧠 Step 4: DeepSeek API call
        resp = requests.post(DEEPSEEK_URL, headers=headers, data=json.dumps(payload))

        # 🧠 Step 5: HTTP error handling
        if resp.status_code != 200:
            return safe_http_error(resp.status_code)

        # 🧠 Step 6: Extract reply safely
        data = resp.json()
        reply = safe_extract_reply(data)
        return reply

    except Exception:
        # 🧠 Step 7: Handle unexpected errors
        return safe_exception()