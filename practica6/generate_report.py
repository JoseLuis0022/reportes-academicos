"""Calcula métricas de clasificación, genera gráficas y el instrumento Excel de supervisión."""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report, confusion_matrix

df = pd.read_csv("resultados_llm_led_raw.csv")
LABELS = ["on", "off", "none"]

# --- Métricas de clasificación ---
report = classification_report(
    df["true_label"], df["predicted_action"], labels=LABELS, output_dict=True, zero_division=0
)
report_df = pd.DataFrame(report).transpose()
report_df.to_csv("classification_report.csv")

cm = confusion_matrix(df["true_label"], df["predicted_action"], labels=LABELS)

# --- Matriz de confusión (gráfica) ---
fig, ax = plt.subplots(figsize=(5, 4))
im = ax.imshow(cm, cmap="Blues")
ax.set_xticks(range(len(LABELS))); ax.set_xticklabels(LABELS)
ax.set_yticks(range(len(LABELS))); ax.set_yticklabels(LABELS)
ax.set_xlabel("Predicho"); ax.set_ylabel("Real")
ax.set_title("Matriz de confusión — clasificador LED")
for i in range(len(LABELS)):
    for j in range(len(LABELS)):
        ax.text(j, i, cm[i, j], ha="center", va="center",
                color="white" if cm[i, j] > cm.max() / 2 else "black")
fig.colorbar(im)
fig.tight_layout()
fig.savefig("confusion_matrix.png", dpi=150)
plt.close(fig)

# --- Latencia por ciclo ---
fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(df["cycle"], df["wall_time_s"], marker=".", linewidth=0.8)
ax.set_xlabel("Ciclo"); ax.set_ylabel("Latencia (s)")
ax.set_title("Latencia por prueba")
fig.tight_layout()
fig.savefig("latency_by_trial.png", dpi=150)
plt.close(fig)

# --- Boxplot de latencia ---
fig, ax = plt.subplots(figsize=(4, 4))
ax.boxplot(df["wall_time_s"], vert=True)
ax.set_ylabel("Latencia (s)")
ax.set_title("Distribución de latencia")
fig.tight_layout()
fig.savefig("latency_boxplot.png", dpi=150)
plt.close(fig)

# --- Tokens vs latencia ---
fig, ax = plt.subplots(figsize=(5, 4))
ax.scatter(df["completion_tokens"], df["wall_time_s"], alpha=0.6)
ax.set_xlabel("Tokens de salida"); ax.set_ylabel("Latencia (s)")
ax.set_title("Tokens de salida vs. latencia")
fig.tight_layout()
fig.savefig("tokens_vs_latency.png", dpi=150)
plt.close(fig)

# --- Tasas de éxito ---
rates = {
    "schema_valid_rate": df["schema_valid"].mean(),
    "mqtt_publish_rate": df["mqtt_published"].mean(),
    "architecture_success_rate": df["architecture_success"].mean(),
    "accuracy": (df["true_label"] == df["predicted_action"]).mean(),
}
fig, ax = plt.subplots(figsize=(6, 4))
ax.bar(rates.keys(), rates.values(), color=["#C9962A", "#8C6518", "#1A1208", "#4A3820"])
ax.set_ylim(0, 1.05)
ax.set_title("Tasas de éxito de la arquitectura")
plt.xticks(rotation=20, ha="right")
fig.tight_layout()
fig.savefig("success_rates.png", dpi=150)
plt.close(fig)

# --- Resumen de métricas ---
summary = {
    "model": "gemma3:4b",
    "num_trials": len(df),
    "accuracy": round(rates["accuracy"], 4),
    "macro_f1": round(report["macro avg"]["f1-score"], 4),
    "schema_valid_rate": round(rates["schema_valid_rate"], 4),
    "mqtt_publish_rate": round(rates["mqtt_publish_rate"], 4),
    "architecture_success_rate": round(rates["architecture_success_rate"], 4),
    "latency_mean_s": round(df["wall_time_s"].mean(), 3),
    "latency_p50_s": round(df["wall_time_s"].quantile(0.50), 3),
    "latency_p95_s": round(df["wall_time_s"].quantile(0.95), 3),
    "latency_p99_s": round(df["wall_time_s"].quantile(0.99), 3),
    "avg_prompt_tokens": round(df["prompt_tokens"].mean(), 1),
    "avg_completion_tokens": round(df["completion_tokens"].mean(), 1),
}
pd.DataFrame([summary]).to_csv("resumen_metricas.csv", index=False)

# --- Errores ---
errors = df[df["true_label"] != df["predicted_action"]]
errors.to_csv("errores.csv", index=False)

# --- Instrumento de supervisión Excel ---
with pd.ExcelWriter("instrumento_supervision_llm_led.xlsx", engine="openpyxl") as writer:
    df.to_excel(writer, sheet_name="Resultados_raw", index=False)
    report_df.to_excel(writer, sheet_name="Classification_report")
    pd.DataFrame([summary]).to_excel(writer, sheet_name="Resumen", index=False)
    errors.to_excel(writer, sheet_name="Errores", index=False)
    pd.DataFrame(cm, index=LABELS, columns=LABELS).to_excel(writer, sheet_name="Matriz_confusion")

print("Resumen:", summary)
print(f"\nErrores ({len(errors)}):")
print(errors[["instruction", "true_label", "predicted_action"]].to_string(index=False))
