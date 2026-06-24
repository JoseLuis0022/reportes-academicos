"""Backend FastAPI — Práctica 5: APIs LLM externas (OpenRouter) vs Ollama local."""
import os
import time
import requests
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

OLLAMA_URL = "http://localhost:11434/api/chat"
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")

PROFILES = {
    "generico": "Eres un asistente de propósito general. Responde de forma clara y breve.",
    "robotica": (
        "Eres un copiloto especializado en robótica móvil y mecatrónica. Rol: ingeniero "
        "experto en sistemas embebidos, sensores y control. Tarea: explicar conceptos técnicos "
        "con ecuaciones cuando aplique. Formato: explicación conceptual, ecuaciones básicas, "
        "ejemplo para estudiantes de ingeniería, y una limitación práctica."
    ),
}


class ChatRequest(BaseModel):
    message: str
    provider: str = "ollama"  # "ollama" | "openrouter"
    model: str = "gemma3:4b"
    copilot_profile: str = "generico"
    temperature: float = 0.7
    top_p: float = 0.9
    max_tokens: int = 300


app = FastAPI(title="Práctica 5 — Ollama vs APIs externas")
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)


@app.get("/health")
def health():
    ollama_up = False
    try:
        ollama_up = requests.get("http://localhost:11434/api/tags", timeout=3).status_code == 200
    except requests.RequestException:
        pass
    return {"ollama": "up" if ollama_up else "down", "openrouter_key_set": bool(OPENROUTER_API_KEY)}


def call_ollama(req: ChatRequest, system_prompt: str):
    payload = {
        "model": req.model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": req.message},
        ],
        "stream": False,
        "options": {
            "temperature": req.temperature,
            "top_p": req.top_p,
            "num_predict": req.max_tokens,
        },
    }
    t0 = time.time()
    resp = requests.post(OLLAMA_URL, json=payload, timeout=120)
    resp.raise_for_status()
    wall = time.time() - t0
    data = resp.json()
    eval_duration_s = data.get("eval_duration", 0) / 1e9
    completion_tokens = data.get("eval_count", 0)
    return {
        "reply": data.get("message", {}).get("content", ""),
        "metrics": {
            "wall_time_s": round(wall, 2),
            "prompt_tokens": data.get("prompt_eval_count", 0),
            "completion_tokens": completion_tokens,
            "total_tokens": data.get("prompt_eval_count", 0) + completion_tokens,
            "tokens_per_second": round(completion_tokens / eval_duration_s, 2) if eval_duration_s > 0 else 0,
        },
    }


def call_openrouter(req: ChatRequest, system_prompt: str):
    headers = {"Authorization": f"Bearer {OPENROUTER_API_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": req.model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": req.message},
        ],
        "temperature": req.temperature,
        "top_p": req.top_p,
        "max_tokens": req.max_tokens,
    }
    t0 = time.time()
    resp = requests.post(OPENROUTER_URL, headers=headers, json=payload, timeout=120)
    resp.raise_for_status()
    wall = time.time() - t0
    data = resp.json()
    usage = data.get("usage", {})
    completion_tokens = usage.get("completion_tokens", 0)
    return {
        "reply": data["choices"][0]["message"]["content"],
        "metrics": {
            "wall_time_s": round(wall, 2),
            "prompt_tokens": usage.get("prompt_tokens", 0),
            "completion_tokens": completion_tokens,
            "total_tokens": usage.get("total_tokens", 0),
            "tokens_per_second": round(completion_tokens / wall, 2) if wall > 0 else 0,
        },
    }


@app.post("/chat")
def chat(req: ChatRequest):
    system_prompt = PROFILES.get(req.copilot_profile, PROFILES["generico"])
    try:
        if req.provider == "openrouter":
            if not OPENROUTER_API_KEY:
                return {"error": "OPENROUTER_API_KEY no configurada"}
            result = call_openrouter(req, system_prompt)
        else:
            result = call_ollama(req, system_prompt)
    except requests.RequestException as e:
        return {"error": str(e)}
    result["provider"] = req.provider
    result["model"] = req.model
    return result
