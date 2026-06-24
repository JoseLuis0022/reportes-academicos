"""Ejecuta el dataset de pruebas contra /led-agent, exporta CSV y calcula métricas."""
import csv
import time
import requests

API = "http://localhost:8002/led-agent"

# Dataset balanceado: instrucciones etiquetadas manualmente (ground truth)
DATASET = [
    ("enciende el led", "on"),
    ("prende la luz por favor", "on"),
    ("activa el led ahora", "on"),
    ("quiero que el led esté encendido", "on"),
    ("turn on the light", "on"),
    ("ilumina el cuarto", "on"),
    ("pon el led en encendido", "on"),
    ("necesito luz, enciéndela", "on"),
    ("activa la salida del LED", "on"),
    ("favor de encender el indicador luminoso", "on"),
    ("apaga el led", "off"),
    ("quita la luz", "off"),
    ("desactiva el led ahora", "off"),
    ("quiero que el led esté apagado", "off"),
    ("turn off the light", "off"),
    ("oscurece el cuarto", "off"),
    ("pon el led en apagado", "off"),
    ("ya no necesito luz, apágala", "off"),
    ("desactiva la salida del LED", "off"),
    ("favor de apagar el indicador luminoso", "off"),
    ("¿qué hora es?", "none"),
    ("cuéntame un chiste", "none"),
    ("¿cómo está el clima hoy?", "none"),
    ("explícame qué es un transistor", "none"),
    ("hola, ¿cómo estás?", "none"),
    ("dame la receta de un pastel", "none"),
    ("¿cuál es la capital de Francia?", "none"),
    ("ayúdame con mi tarea de matemáticas", "none"),
    ("el led parpadea muy rápido", "none"),
    ("no sé qué hacer con el robot", "none"),
]

# Repetir el dataset ~3.3x para llegar a >=100 ciclos (30 instrucciones x 4 = 120)
FULL_DATASET = DATASET * 4

rows = []
for i, (instruction, label) in enumerate(FULL_DATASET):
    t0 = time.time()
    try:
        resp = requests.post(API, json={"instruction": instruction}, timeout=60)
        data = resp.json()
    except requests.RequestException as e:
        data = {"error": str(e)}
    wall = time.time() - t0

    parsed = data.get("parsed", {})
    row = {
        "cycle": i,
        "instruction": instruction,
        "true_label": label,
        "predicted_action": parsed.get("action", "error"),
        "confidence": parsed.get("confidence", 0),
        "schema_valid": data.get("schema_valid", False),
        "mqtt_published": data.get("mqtt_published", False),
        "architecture_success": data.get("architecture_success", False),
        "wall_time_s": data.get("metrics", {}).get("wall_time_s", wall),
        "prompt_tokens": data.get("metrics", {}).get("prompt_tokens", 0),
        "completion_tokens": data.get("metrics", {}).get("completion_tokens", 0),
        "tokens_per_second": data.get("metrics", {}).get("tokens_per_second", 0),
    }
    rows.append(row)
    print(f"[{i+1}/{len(FULL_DATASET)}] {instruction[:40]:40} true={label:5} pred={row['predicted_action']:5} ok={row['architecture_success']}")

with open("resultados_llm_led_raw.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)

print(f"\nListo: {len(rows)} pruebas guardadas en resultados_llm_led_raw.csv")
