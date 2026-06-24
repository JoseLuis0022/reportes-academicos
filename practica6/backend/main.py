"""Backend FastAPI — Práctica 6: clasificación de instrucciones LED vía LLM + publicación MQTT."""
import json
import re
import time
import requests
import paho.mqtt.client as mqtt
from fastapi import FastAPI
from pydantic import BaseModel

OLLAMA_URL = "http://localhost:11434/api/chat"
MQTT_BROKER = "mqtt.mecatronica-ibero.mx"
MQTT_PORT = 1883
MQTT_TOPIC = "public/llm-led/cmd"

SYSTEM_PROMPT = (
    "Eres un agente que clasifica instrucciones de un usuario para controlar un LED. "
    "Debes responder ÚNICAMENTE con un JSON válido, sin texto adicional, con este esquema exacto: "
    '{"action": "on|off|none", "confidence": 0.0-1.0, "reason": "breve justificación"}. '
    "action=on si el usuario pide encender el LED, action=off si pide apagarlo, "
    "action=none si la instrucción es ambigua o no relacionada con el LED."
)

mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)


class LedRequest(BaseModel):
    instruction: str
    model: str = "gemma3:4b"
    temperature: float = 0.0


app = FastAPI(title="Práctica 6 — LED Agent (LLM + MQTT)")


def extract_json(text: str) -> dict:
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        return {"action": "none", "confidence": 0.0, "reason": "json_parse_error"}
    try:
        return json.loads(match.group(0))
    except json.JSONDecodeError:
        return {"action": "none", "confidence": 0.0, "reason": "json_parse_error"}


@app.get("/health")
def health():
    try:
        ollama_up = requests.get("http://localhost:11434/api/tags", timeout=3).status_code == 200
    except requests.RequestException:
        ollama_up = False
    return {"ollama": "up" if ollama_up else "down"}


@app.post("/led-agent")
def led_agent(req: LedRequest):
    t0 = time.time()
    payload = {
        "model": req.model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": req.instruction},
        ],
        "stream": False,
        "format": "json",
        "options": {"temperature": req.temperature, "num_predict": 100},
    }
    try:
        resp = requests.post(OLLAMA_URL, json=payload, timeout=60)
        resp.raise_for_status()
    except requests.RequestException as e:
        return {"error": str(e)}
    wall_time = time.time() - t0

    data = resp.json()
    raw_content = data.get("message", {}).get("content", "")
    parsed = extract_json(raw_content)
    schema_valid = (
        isinstance(parsed, dict)
        and parsed.get("action") in ("on", "off", "none")
        and isinstance(parsed.get("confidence"), (int, float))
    )

    mqtt_published = False
    if schema_valid:
        try:
            mqtt_client.connect(MQTT_BROKER, MQTT_PORT, keepalive=10)
            mqtt_client.publish(MQTT_TOPIC, json.dumps(parsed))
            mqtt_client.disconnect()
            mqtt_published = True
        except Exception:
            mqtt_published = False

    eval_duration_s = data.get("eval_duration", 0) / 1e9
    completion_tokens = data.get("eval_count", 0)

    return {
        "instruction": req.instruction,
        "raw_content": raw_content,
        "parsed": parsed,
        "schema_valid": schema_valid,
        "mqtt_published": mqtt_published,
        "architecture_success": schema_valid and mqtt_published,
        "metrics": {
            "wall_time_s": round(wall_time, 3),
            "prompt_tokens": data.get("prompt_eval_count", 0),
            "completion_tokens": completion_tokens,
            "tokens_per_second": round(completion_tokens / eval_duration_s, 2) if eval_duration_s > 0 else 0,
        },
    }
