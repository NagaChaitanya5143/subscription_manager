"""
Benchmark the fastest models on NVIDIA NIM API.
Tests small/fast models with a simple tool-calling prompt and measures latency.
"""

import os
import time

import requests

API_KEY = os.getenv("NVIDIA_API_KEY") or os.getenv("OPENAI_API_KEY") or ""
BASE_URL = os.getenv("LLM_BASE_URL", "https://integrate.api.nvidia.com/v1/chat/completions")
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

if not API_KEY:
    raise RuntimeError("Set NVIDIA_API_KEY or OPENAI_API_KEY before running the benchmark.")

# Candidates: small/fast models (avoid 70B+ for speed)
MODELS = [
    "meta/llama-3.1-8b-instruct",
    "meta/llama-3.2-1b-instruct",
    "meta/llama-3.2-3b-instruct",
    "google/gemma-3-4b-it",
    "google/gemma-3-12b-it",
    "mistralai/mistral-7b-instruct-v0.3",
    "nv-mistralai/mistral-nemo-12b-instruct",
    "nvidia/llama-3.1-nemotron-nano-8b-v1",
    "nvidia/nemotron-mini-4b-instruct",
    "ibm/granite-3.0-3b-a800m-instruct",
    "ibm/granite-3.0-8b-instruct",
    "stepfun-ai/step-3.7-flash",
    "deepseek-ai/deepseek-v4-flash-0731",
    "openai/gpt-oss-20b",
]

PROMPT = [{"role": "user", "content": "Say 'hello' in exactly 3 words."}]

results = []
for model in MODELS:
    payload = {
        "model": model,
        "messages": PROMPT,
        "max_tokens": 20,
        "temperature": 0.0
    }
    try:
        start = time.time()
        r = requests.post(BASE_URL, headers=HEADERS, json=payload, timeout=12)
        elapsed = round(time.time() - start, 2)
        if r.status_code == 200:
            reply = r.json()["choices"][0]["message"]["content"].strip()
            results.append((elapsed, model, "OK", reply))
        else:
            results.append((elapsed, model, f"HTTP {r.status_code}", ""))
    except Exception as e:
        results.append((99.0, model, f"ERROR: {str(e)[:50]}", ""))

# Sort by speed
results.sort(key=lambda x: x[0])

print(f"\n{'Rank':<5} {'Time(s)':<10} {'Model':<55} {'Status'}")
print("-" * 100)
for i, (t, model, status, reply) in enumerate(results, 1):
    print(f"{i:<5} {t:<10} {model:<55} {status}")
