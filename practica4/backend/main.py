"""Backend FastAPI — Práctica 4: Copilotos especializados con Ollama."""
import time
import requests
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

OLLAMA_URL = "http://localhost:11434/api/chat"

PROFILES = {
    "generico": {
        "label": "Asistente genérico",
        "system_prompt": "Eres un asistente de propósito general. Responde de forma clara y breve.",
    },
    "docente": {
        "label": "Copiloto docente",
        "system_prompt": (
            "Eres un copiloto docente universitario. Rol: explicar conceptos con rigor académico "
            "y ejemplos pedagógicos. Tarea: responder dudas de estudiantes de ingeniería. "
            "Formato: explicación conceptual + ejemplo aplicado. Límites: no inventes referencias "
            "bibliográficas; si falta información, dilo explícitamente antes de asumir."
        ),
    },
    "robotica": {
        "label": "Copiloto de robótica móvil",
        "system_prompt": (
            "Eres un copiloto especializado en robótica móvil y mecatrónica. Rol: ingeniero "
            "experto en sistemas embebidos, sensores y control. Tarea: explicar conceptos técnicos "
            "con ecuaciones cuando aplique. Formato: explicación conceptual, ecuaciones básicas, "
            "ejemplo para estudiantes de ingeniería, y una limitación práctica. Límites: no inventes "
            "datasheets ni especificaciones de hardware; señala advertencias de seguridad cuando "
            "se mencione actuar sobre hardware real."
        ),
    },
    "programacion": {
        "label": "Copiloto de programación",
        "system_prompt": (
            "Eres un copiloto de programación. Rol: ingeniero de software senior. Tarea: ayudar a "
            "escribir, depurar y explicar código. Formato: código en bloques con comentarios mínimos "
            "+ breve explicación. Límites: no inventes funciones o librerías que no existan; si no "
            "estás seguro de una API, dilo."
        ),
    },
    "investigacion": {
        "label": "Copiloto de investigación académica",
        "system_prompt": (
            "Eres un copiloto de investigación académica. Rol: asistente metodológico. Tarea: ayudar "
            "a estructurar ideas, marcos teóricos y metodología, NUNCA citar papers o autores que no "
            "puedas verificar. Formato: respuesta estructurada con secciones. Límites: declara "
            "explícitamente que no debes usarse como única fuente académica y que toda referencia "
            "debe ser verificada por el usuario."
        ),
    },
}


class ChatRequest(BaseModel):
    message: str
    model: str = "gemma3:4b"
    copilot_profile: str = "generico"
    system_prompt: str | None = Field(default=None, max_length=6000)
    temperature: float = 0.7
    top_p: float = 0.9
    num_predict: int = 400
    num_ctx: int = 4096
    repeat_penalty: float = 1.1


app = FastAPI(title="Práctica 4 — Copilotos con Ollama")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"status": "ok", "service": "copilotos-ollama"}


@app.get("/health")
def health():
    try:
        r = requests.get("http://localhost:11434/api/tags", timeout=3)
        return {"ollama": "up" if r.status_code == 200 else "down"}
    except requests.RequestException:
        return {"ollama": "down"}


@app.get("/profiles")
def get_profiles():
    return PROFILES


@app.post("/chat")
def chat(req: ChatRequest):
    system_prompt = req.system_prompt or PROFILES.get(
        req.copilot_profile, PROFILES["generico"]
    )["system_prompt"]

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
            "num_predict": req.num_predict,
            "num_ctx": req.num_ctx,
            "repeat_penalty": req.repeat_penalty,
        },
    }

    t0 = time.time()
    try:
        resp = requests.post(OLLAMA_URL, json=payload, timeout=120)
        resp.raise_for_status()
    except requests.RequestException as e:
        return {"error": str(e)}
    wall_time = time.time() - t0

    data = resp.json()
    prompt_tokens = data.get("prompt_eval_count", 0)
    completion_tokens = data.get("eval_count", 0)
    eval_duration_s = data.get("eval_duration", 0) / 1e9
    tps = completion_tokens / eval_duration_s if eval_duration_s > 0 else 0

    return {
        "model": req.model,
        "copilot_profile": req.copilot_profile,
        "copilot_label": PROFILES.get(req.copilot_profile, PROFILES["generico"])["label"],
        "system_prompt_used": system_prompt,
        "reply": data.get("message", {}).get("content", ""),
        "metrics": {
            "wall_time_s": round(wall_time, 2),
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "tokens_per_second": round(tps, 2),
        },
    }
