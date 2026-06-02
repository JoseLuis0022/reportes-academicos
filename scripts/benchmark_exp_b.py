"""
Experimento B — Variación de parámetros de generación
1 modelo × 9 configuraciones × 100 ciclos = 900 llamadas.
Salida: data/exp_b_results.csv

El modelo se lee de data/exp_a_results.csv (ganador por quality_score promedio).
Si el CSV no existe, usa phi4-mini:latest por defecto.

Ejecutar con:
    python3 scripts/benchmark_exp_b.py
"""
import sys
import os
import csv

sys.path.insert(0, os.path.dirname(__file__))
from benchmark_utils import ollama_call, extract_metrics, open_csv_writer, write_row
from tqdm import tqdm

DATA_DIR      = os.path.join(os.path.dirname(__file__), "..", "data")
EXP_A_CSV     = os.path.join(DATA_DIR, "exp_a_results.csv")
OUTPUT        = os.path.join(DATA_DIR, "exp_b_results.csv")
DEFAULT_MODEL = "phi4-mini:latest"

PROMPT = (
    "Explica en menos de 100 palabras la diferencia entre "
    "Inteligencia Artificial, Machine Learning e IA Generativa."
)

CYCLES = 100

# 3 parámetros × 3 valores = 9 configuraciones
# Un parámetro varía a la vez; los otros se fijan en su valor medio
EXPERIMENTS = [
    {"param": "temperature", "temperature": 0.1, "top_p": 0.75, "top_k": 40},
    {"param": "temperature", "temperature": 0.5, "top_p": 0.75, "top_k": 40},
    {"param": "temperature", "temperature": 0.9, "top_p": 0.75, "top_k": 40},
    {"param": "top_p",       "temperature": 0.5, "top_p": 0.50, "top_k": 40},
    {"param": "top_p",       "temperature": 0.5, "top_p": 0.75, "top_k": 40},
    {"param": "top_p",       "temperature": 0.5, "top_p": 0.95, "top_k": 40},
    {"param": "top_k",       "temperature": 0.5, "top_p": 0.75, "top_k": 10},
    {"param": "top_k",       "temperature": 0.5, "top_p": 0.75, "top_k": 40},
    {"param": "top_k",       "temperature": 0.5, "top_p": 0.75, "top_k": 80},
]


def best_model_from_exp_a():
    if not os.path.exists(EXP_A_CSV):
        print(f"  No se encontró {EXP_A_CSV}. Usando {DEFAULT_MODEL}.")
        return DEFAULT_MODEL
    scores, counts = {}, {}
    with open(EXP_A_CSV, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            m = row["model"]
            scores[m] = scores.get(m, 0) + float(row.get("quality_score", 0))
            counts[m] = counts.get(m, 0) + 1
    avgs   = {m: scores[m] / counts[m] for m in scores}
    winner = max(avgs, key=avgs.get)
    print(f"  Modelo ganador de Exp A: {winner}  (calidad promedio {avgs[winner]:.2f})")
    return winner


def main():
    print("\n" + "═" * 60)
    print("  EXPERIMENTO B — Variación de parámetros")
    print(f"  9 configuraciones × {CYCLES} ciclos = {9 * CYCLES} llamadas")
    print("═" * 60)

    model = best_model_from_exp_a()
    print(f"  Modelo seleccionado: {model}")
    print("═" * 60 + "\n")

    os.makedirs(DATA_DIR, exist_ok=True)
    f, writer = open_csv_writer(OUTPUT)
    total = len(EXPERIMENTS) * CYCLES

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
        for exp in EXPERIMENTS:
            param = exp["param"]
            temp  = exp["temperature"]
            tp    = exp["top_p"]
            tk    = exp["top_k"]

            # Etiqueta del valor que está variando
            val_label = {
                "temperature": f"temp={temp}",
                "top_p":       f"top_p={tp}",
                "top_k":       f"top_k={tk}",
            }[param]
            exp_id = f"exp_b_{param}_{val_label}"

            params = {"options": {
                "temperature": temp,
                "top_p": tp,
                "top_k": tk,
                "num_predict": 200,
            }}

            config_bar = tqdm(
                total=CYCLES,
                desc=f"  {val_label:<20}",
                unit="ciclo",
                position=1,
                colour="cyan",
                bar_format="{l_bar}{bar:30}{r_bar}",
                leave=False,
            )

            errors = 0
            for cycle in range(1, CYCLES + 1):
                try:
                    resp = ollama_call(model, PROMPT, params)
                    row  = extract_metrics(resp, exp_id, model, cycle, PROMPT, params)
                    write_row(writer, row)
                    f.flush()

                    config_bar.set_postfix(
                        tps=f"{row['tokens_per_second']:.1f}",
                        ms=f"{row['total_duration_ms']:.0f}",
                        cal=f"{row['quality_score']:.1f}",
                        err=errors,
                        refresh=True,
                    )
                except Exception as e:
                    errors += 1
                    tqdm.write(f"  ⚠  ERROR {val_label} ciclo {cycle}: {e}")

                config_bar.update(1)
                global_bar.update(1)

            config_bar.close()
            tqdm.write(f"  ✓  {val_label} completado ({errors} errores)")

    finally:
        global_bar.close()
        f.close()

    print("\n" + "═" * 60)
    print(f"  ✅  Resultados guardados en: {OUTPUT}")
    print("═" * 60 + "\n")


if __name__ == "__main__":
    main()
