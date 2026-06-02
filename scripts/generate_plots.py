"""
Genera 6 gráficas PNG en assets/img/practica2/ a partir de los CSVs.
Requiere: pandas, matplotlib
"""
import os
import sys
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
IMG_DIR  = os.path.join(os.path.dirname(__file__), "..", "assets", "img", "practica2")

# Paleta cálida del sitio
GOLD    = "#C9962A"
DARK    = "#1A1210"
BROWN   = "#4A3820"
CREAM   = "#FAF6EE"
COLORS  = ["#C9962A", "#4A3820", "#8C6518"]
PARAM_COLORS = {"temperature": "#C9962A", "top_p": "#4A3820", "top_k": "#8C6518"}

plt.rcParams.update({
    "figure.facecolor": CREAM,
    "axes.facecolor":   CREAM,
    "axes.edgecolor":   BROWN,
    "axes.labelcolor":  DARK,
    "xtick.color":      DARK,
    "ytick.color":      DARK,
    "text.color":       DARK,
    "font.family":      "sans-serif",
    "axes.spines.top":  False,
    "axes.spines.right": False,
})


def save(fig, name):
    os.makedirs(IMG_DIR, exist_ok=True)
    path = os.path.join(IMG_DIR, name)
    fig.savefig(path, dpi=150, bbox_inches="tight", facecolor=CREAM)
    plt.close(fig)
    print(f"  Guardado: {path}")


def plot_exp_a(df):
    models = df["model"].unique()

    # 1. Latencia por ciclo (línea)
    fig, ax = plt.subplots(figsize=(9, 4))
    for i, model in enumerate(models):
        sub = df[df["model"] == model].sort_values("cycle")
        ax.plot(sub["cycle"], sub["total_duration_ms"],
                color=COLORS[i % len(COLORS)], alpha=0.8,
                linewidth=1.2, label=model)
    ax.set_title("Experimento A — Latencia total por ciclo", fontweight="bold")
    ax.set_xlabel("Ciclo")
    ax.set_ylabel("Latencia (ms)")
    ax.legend(fontsize=8)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))
    save(fig, "exp_a_latencia.png")

    # 2. TPS media por modelo (barras con error bars)
    fig, ax = plt.subplots(figsize=(6, 4))
    means  = [df[df["model"] == m]["tokens_per_second"].mean() for m in models]
    stds   = [df[df["model"] == m]["tokens_per_second"].std()  for m in models]
    bars = ax.bar(models, means, color=COLORS[:len(models)],
                  yerr=stds, capsize=5, error_kw={"ecolor": DARK, "linewidth": 1.2})
    ax.set_title("Experimento A — Tokens por segundo (media ± σ)", fontweight="bold")
    ax.set_ylabel("Tokens/segundo")
    ax.set_xticks(range(len(models)))
    ax.set_xticklabels([m.split(":")[0] for m in models], fontsize=9)
    for bar, mean in zip(bars, means):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + max(stds) * 0.05,
                f"{mean:.1f}", ha="center", va="bottom", fontsize=8, color=DARK)
    save(fig, "exp_a_tokens_per_second.png")

    # 3. Boxplot de latencia
    fig, ax = plt.subplots(figsize=(7, 4))
    data_bp = [df[df["model"] == m]["total_duration_ms"].values for m in models]
    bp = ax.boxplot(data_bp, patch_artist=True, medianprops={"color": DARK, "linewidth": 2})
    for patch, color in zip(bp["boxes"], COLORS):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)
    ax.set_xticklabels([m.split(":")[0] for m in models], fontsize=9)
    ax.set_title("Experimento A — Distribución de latencia", fontweight="bold")
    ax.set_ylabel("Latencia (ms)")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))
    save(fig, "exp_a_boxplot.png")


def plot_exp_b(df):
    for param in ["temperature", "top_p", "top_k"]:
        subset = df[df["experiment_id"].str.contains(f"exp_b_{param}")]
        if subset.empty:
            print(f"  Sin datos para parámetro: {param}")
            continue

        col_map = {"temperature": "temperature", "top_p": "top_p", "top_k": "top_k"}
        col = col_map[param]

        grouped = subset.groupby(col).agg(
            tps_mean=("tokens_per_second", "mean"),
            tps_std=("tokens_per_second", "std"),
            lat_mean=("total_duration_ms", "mean"),
        ).reset_index()

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
        color = PARAM_COLORS[param]

        ax1.errorbar(grouped[col], grouped["tps_mean"], yerr=grouped["tps_std"],
                     marker="o", color=color, linewidth=2, capsize=5)
        ax1.set_title(f"TPS vs {param}", fontweight="bold")
        ax1.set_xlabel(param)
        ax1.set_ylabel("Tokens/segundo")

        ax2.plot(grouped[col], grouped["lat_mean"], marker="s",
                 color=BROWN, linewidth=2)
        ax2.set_title(f"Latencia vs {param}", fontweight="bold")
        ax2.set_xlabel(param)
        ax2.set_ylabel("Latencia media (ms)")
        ax2.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))

        fig.suptitle(f"Experimento B — Efecto de {param}", fontweight="bold", y=1.02)
        fig.tight_layout()
        save(fig, f"exp_b_{param}.png")


def main():
    exp_a_path = os.path.join(DATA_DIR, "exp_a_results.csv")
    exp_b_path = os.path.join(DATA_DIR, "exp_b_results.csv")

    if os.path.exists(exp_a_path):
        print("Generando gráficas Exp A...")
        df_a = pd.read_csv(exp_a_path)
        plot_exp_a(df_a)
    else:
        print(f"No encontrado: {exp_a_path}")

    if os.path.exists(exp_b_path):
        print("Generando gráficas Exp B...")
        df_b = pd.read_csv(exp_b_path)
        plot_exp_b(df_b)
    else:
        print(f"No encontrado: {exp_b_path}")

    print("\nListo.")


if __name__ == "__main__":
    main()
