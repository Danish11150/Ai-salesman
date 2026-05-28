def safe_extract_reply(data):
    """
    Safely extract AI reply from DeepSeek JSON response.
    Prevents crashes if JSON format changes or reply is missing.
    """
    try:
        reply = (
            data.get("choices", [{}])[0]
            .get("message", {})
            .get("content", "")
            .strip()
        )
        if not reply:
            return "Mujhe samajh nahi aaya, dobara likho please."
        return reply

    except Exception:
        return "Response samajh nahi aaya, dobara try karein."


def safe_http_error(status_code):
    """
    Handle HTTP errors from DeepSeek API.
    """

    if status_code == 400:
        return "Request galat hai. Kripya sahi format me bhejein."

    if status_code == 401:
        return "API key invalid hai. Kripya sahi key add karein."

    if status_code == 403:
        return "Access denied. API key ko permission nahi hai."

    if status_code == 404:
        return "DeepSeek server nahi mila. Thori der baad try karein."

    if status_code == 408:
        return "Request timeout ho gaya. Dobara try karein."

    if status_code == 429:
        return "Zyada requests ho gayi hain. Thori der baad dobara try karein."

    if status_code >= 500:
        return "Server busy hai. Thori der baad try karein."

    return "Kuch error aa gaya hai. Dobara try karein."


def safe_exception():
    """
    Handle unexpected Python exceptions.
    """
    return "Kuch technical issue aa gaya hai, thori der baad try karein."