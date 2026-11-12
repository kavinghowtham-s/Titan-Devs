#!/usr/bin/env python3
"""CLI utility to verify Ollama Cloud API key and test available model responses."""

import os
import sys
import time
import httpx
from dotenv import load_dotenv

# Load environment
load_dotenv("backend/.env")
load_dotenv(".env")

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "https://ollama.com").rstrip("/")
OLLAMA_API_KEY = os.getenv("OLLAMA_API_KEY", "")

def check_connection():
    print(f"Checking Ollama Cloud endpoint: {OLLAMA_BASE_URL}")
    if not OLLAMA_API_KEY:
        print("[FAIL] OLLAMA_API_KEY is not set in .env")
        sys.exit(1)

    masked_key = f"...{OLLAMA_API_KEY[-4:]}" if len(OLLAMA_API_KEY) >= 4 else "***"
    print(f"API Key present: {masked_key}")

    headers = {
        "Authorization": f"Bearer {OLLAMA_API_KEY}",
        "Content-Type": "application/json"
    }

    # 1. Test /api/tags
    try:
        t0 = time.time()
        res = httpx.get(f"{OLLAMA_BASE_URL}/api/tags", headers=headers, timeout=10.0)
        dt = (time.time() - t0) * 1000
        if res.status_code == 200:
            models_data = res.json().get("models", [])
            model_names = [m["name"] for m in models_data]
            print(f"[OK] Authentication successful ({dt:.0f}ms). Found {len(model_names)} available models:")
            for m in model_names:
                print(f"  - {m}")
        else:
            print(f"[FAIL] /api/tags returned HTTP {res.status_code}: {res.text}")
            sys.exit(1)
    except Exception as e:
        print(f"[FAIL] Network error reaching {OLLAMA_BASE_URL}: {e}")
        sys.exit(1)

    # 2. Test chat with primary model
    test_model = os.getenv("MODEL_INTAKE", "deepseek-v4.1-flash")
    if test_model not in model_names and model_names:
        test_model = model_names[0]

    print(f"\nTesting live chat completion on model '{test_model}'...")
    payload = {
        "model": test_model,
        "messages": [{"role": "user", "content": "Respond with the word OK."}],
        "stream": False
    }
    try:
        t0 = time.time()
        res = httpx.post(f"{OLLAMA_BASE_URL}/api/chat", json=payload, headers=headers, timeout=15.0)
        dt = (time.time() - t0) * 1000
        if res.status_code == 200:
            reply = res.json().get("message", {}).get("content", "").strip()
            print(f"[OK] Response received in {dt:.0f}ms: \"{reply[:100]}\"")
            print("\n[SUCCESS] Your Ollama Cloud setup is fully operational!")
        else:
            print(f"[WARN] Chat endpoint returned HTTP {res.status_code}: {res.text}")
    except Exception as e:
        print(f"[WARN] Chat test failed: {e}")

if __name__ == "__main__":
    check_connection()
