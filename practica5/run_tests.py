import json
import requests

API = "http://localhost:8001/chat"
PROMPT = (
    "Explica qué es la odometría diferencial en un robot móvil de dos ruedas. Incluye: "
    "1) explicación conceptual; 2) ecuaciones básicas; 3) ejemplo para estudiantes de "
    "ingeniería; 4) una limitación práctica. Responde en máximo 250 palabras."
)

CONFIGS = [
    {"provider": "ollama", "model": "gemma3:4b"},
    {"provider": "openrouter", "model": "openai/gpt-4o-mini"},
    {"provider": "openrouter", "model": "meta-llama/llama-3.1-8b-instruct"},
]

results = {}
for cfg in CONFIGS:
    payload = {
        "message": PROMPT,
        "provider": cfg["provider"],
        "model": cfg["model"],
        "copilot_profile": "robotica",
        "temperature": 0.7,
        "top_p": 0.9,
        "max_tokens": 300,
    }
    resp = requests.post(API, json=payload, timeout=120)
    data = resp.json()
    key = f"{cfg['provider']}::{cfg['model']}"
    results[key] = data
    print(key, "->", data.get("metrics", data.get("error")))

with open("comparison_results.json", "w") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
print("\nGuardado en comparison_results.json")
