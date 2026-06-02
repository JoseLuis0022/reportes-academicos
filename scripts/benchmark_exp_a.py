"""
Experimento A — Comparación de modelos LLM
3 modelos × 100 ciclos = 300 llamadas a la API local de Ollama.
Salida: data/exp_a_results.csv

Ejecutar con:
    python3 scripts/benchmark_exp_a.py
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from benchmark_utils import ollama_call, extract_metrics, open_csv_writer, write_row
from tqdm import tqdm

MODELS = [
    "gemma3:4b",
    "phi4-mini:latest",
    "llama3.2:3b",
]

PROMPT = (
    "Explica en menos de 100 palabras la diferencia entre "
    "Inteligencia Artificial, Machine Learning e IA Generativa."
)

PARAMS = {
    "options": {
        "temperature": 0.7,
        "top_p": 0.9,
        "top_k": 40,
        "num_predict": 200,
    }
}

CYCLES = 100
OUTPUT = os.path.join(os.path.dirname(__file__), "..", "data", "exp_a_results.csv")


def main():
    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
    f, writer = open_csv_writer(OUTPUT)
    total = len(MODELS) * CYCLES

    print("\n" + "═" * 60)
    print("  EXPERIMENTO A — Comparación de modelos")
    print(f"  {len(MODELS)} modelos × {CYCLES} ciclos = {total} llamadas")
    print("═" * 60 + "\n")

    global_bar = tqdm(
        total=total,
        desc="  Total",
        unit="ciclo",
        position=0,
        colour="yellow",
        bar_format="{l_bar}{bar:30}{r_bar}",
        leave=True,
    )

    try:
        for model in MODELS:
            short = model.split(":")[0]
            model_bar = tqdm(
                total=CYCLES,
                desc=f"  {short:<18}",
                unit="ciclo",
                position=1,
                colour="cyan",
                bar_format="{l_bar}{bar:30}{r_bar}",
                leave=False,
            )

            errors = 0
            for cycle in range(1, CYCLES + 1):
                try:
                    resp = ollama_call(model, PROMPT, PARAMS)
                    row  = extract_metrics(resp, "exp_a", model, cycle, PROMPT, PARAMS)
                    write_row(writer, row)
                    f.flush()

                    tps  = row["tokens_per_second"]
                    ms   = row["total_duration_ms"]
                    qual = row["quality_score"]

                    model_bar.set_postfix(
                        tps=f"{tps:.1f}",
                        ms=f"{ms:.0f}",
                        cal=f"{qual:.1f}",
                        err=errors,
                        refresh=True,
                    )
                    model_bar.update(1)
                    global_bar.update(1)

                except Exception as e:
                    errors += 1
                    model_bar.set_postfix(err=errors, refresh=True)
                    model_bar.update(1)
                    global_bar.update(1)
                    tqdm.write(f"  ⚠  ERROR {model} ciclo {cycle}: {e}")

            model_bar.close()
            tqdm.write(f"  ✓  {model} completado ({errors} errores)")

    finally:
        global_bar.close()
        f.close()

    print("\n" + "═" * 60)
    print(f"  ✅  Resultados guardados en: {OUTPUT}")
    print("═" * 60 + "\n")


if __name__ == "__main__":
    main()
