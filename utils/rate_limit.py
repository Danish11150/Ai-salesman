import time

# Simple in-memory rate limit tracker (per process)
_last_request_time = 0
MIN_GAP_SECONDS = 1.0  # 1 second gap between requests (safe default)


def respect_rate_limit():
    """
    Ensures a minimum gap between DeepSeek API calls.
    Prevents hitting rate limits too fast.
    """
    global _last_request_time
    now = time.time()
    diff = now - _last_request_time

    if diff < MIN_GAP_SECONDS:
        sleep_time = MIN_GAP_SECONDS - diff
        time.sleep(sleep_time)

    _last_request_time = time.time()


def handle_rate_limit_error():
    """
    Message to show when DeepSeek returns 429 (Too Many Requests).
    """
    return "Zyada requests ho gayi hain. Thori der baad dobara try karein."