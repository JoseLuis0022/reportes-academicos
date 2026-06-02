import requests
import csv
import datetime

OLLAMA_URL = "http://localhost:11434/api/generate"

CSV_FIELDS = [
    "timestamp", "experiment_id", "model", "cycle", "prompt",
    "temperature", "top_p", "top_k", "response",
    "total_duration_ms", "load_duration_ms", "eval_duration_ms",
    "prompt_eval_count", "eval_count", "tokens_per_second",
    "response_chars", "quality_score", "notes",
]

KEYWORDS = ["modelo", "lenguaje", "token", "ia", "aprendizaje", "generativa",
            "machine learning", "inteligencia", "artificial", "neural"]


def ollama_call(model, prompt, params, timeout=180):
    payload = {"model": model, "prompt": prompt, "stream": False, **params}
    r = requests.post(OLLAMA_URL, json=payload, timeout=timeout)
    r.raise_for_status()
    return r.json()


def extract_metrics(resp, experiment_id, model, cycle, prompt, params):
    ns = 1_000_000_000
    total_ms  = resp.get("total_duration", 0) / 1_000_000
    load_ms   = resp.get("load_duration", 0) / 1_000_000
    eval_dur  = resp.get("eval_duration", 0)
    eval_count = resp.get("eval_count", 0)
    tps = eval_count / (eval_dur / ns) if eval_dur > 0 else 0
    response = resp.get("response", "")
    opts = params.get("options", {})
    return {
        "timestamp":         datetime.datetime.now().isoformat(),
        "experiment_id":     experiment_id,
        "model":             model,
        "cycle":             cycle,
        "prompt":            prompt[:80],
        "temperature":       opts.get("temperature", ""),
        "top_p":             opts.get("top_p", ""),
        "top_k":             opts.get("top_k", ""),
        "response":          response[:300],
        "total_duration_ms": round(total_ms, 2),
        "load_duration_ms":  round(load_ms, 2),
        "eval_duration_ms":  round(eval_dur / 1_000_000, 2),
        "prompt_eval_count": resp.get("prompt_eval_count", 0),
        "eval_count":        eval_count,
        "tokens_per_second": round(tps, 2),
        "response_chars":    len(response),
        "quality_score":     quality_score(response),
        "notes":             "",
    }


def quality_score(text):
    if not text or len(text) < 20:
        return 0.0
    words = text.lower().split()
    if not words:
        return 0.0
    unique_ratio = len(set(words)) / len(words)
    length_score = min(len(text) / 500, 1.0)
    kw_score = sum(1 for k in KEYWORDS if k in text.lower()) / len(KEYWORDS)
    return round(length_score * 4 + unique_ratio * 3 + kw_score * 3, 2)


def open_csv_writer(path):
    f = open(path, "w", newline="", encoding="utf-8")
    writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
    writer.writeheader()
    return f, writer


def write_row(writer, row):
    writer.writerow({f: row.get(f, "") for f in CSV_FIELDS})
