import json
import requests

API = "http://localhost:8000/chat"
MODEL = "gemma3:4b"

PROMPTS = {
    "generico": [
        "¿Qué es la inteligencia artificial?",
        "Dame consejos para estudiar mejor.",
        "Explica qué es una API en términos simples.",
    ],
    "docente": [
        "Explícame qué es la transformada de Fourier para un estudiante de ingeniería.",
        "¿Cómo le explicarías el concepto de entropía a un alumno de primer semestre?",
        "Da un ejemplo pedagógico para enseñar recursividad en programación.",
    ],
    "robotica": [
        "Explícame qué es la odometría diferencial y dame un ejemplo para estudiantes de primer semestre",
        "¿Qué es un PID y cómo se aplica al control de un robot móvil?",
        "Explica la diferencia entre un sensor ultrasónico y un LIDAR en robótica móvil.",
    ],
    "programacion": [
        "Escribe una función en Python que invierta una lista sin usar reversed().",
        "¿Cuál es la diferencia entre una lista y una tupla en Python?",
        "Corrige este código: def suma(a,b) return a+b",
    ],
}

results = []
for profile, prompts in PROMPTS.items():
    for prompt in prompts:
        resp = requests.post(API, json={
            "message": prompt,
            "model": MODEL,
            "copilot_profile": profile,
        }, timeout=180)
        data = resp.json()
        results.append({
            "profile": profile,
            "prompt": prompt,
            "reply": data.get("reply", ""),
            "metrics": data.get("metrics", {}),
        })
        print(f"[{profile}] {prompt[:50]}... -> {data.get('metrics')}")

with open("test_results.json", "w") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

# Comparación genérico vs robótica con el mismo prompt
compare_prompt = "Explícame qué es la odometría diferencial y dame un ejemplo para estudiantes de primer semestre"
comparison = {}
for profile in ["generico", "robotica"]:
    resp = requests.post(API, json={
        "message": compare_prompt,
        "model": MODEL,
        "copilot_profile": profile,
    }, timeout=180)
    comparison[profile] = resp.json()

with open("comparison.json", "w") as f:
    json.dump(comparison, f, ensure_ascii=False, indent=2)

print("\nListo. Resultados en test_results.json y comparison.json")
