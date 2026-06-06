from supabase import create_client
import os

# Render environment variables
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Fallback (local development)
if not SUPABASE_URL:
    SUPABASE_URL = "https://ryvmqbcstrlggeziksou.supabase.co"

if not SUPABASE_KEY:
    SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

# Create client
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
