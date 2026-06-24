# CLAUDE.md — Memoria del Proyecto

> Archivo de contexto para Claude Code. Leer al iniciar cualquier sesión.

---

## Identidad del proyecto

| | |
|---|---|
| **Nombre** | Reportes Académicos – IA Generativa |
| **Curso** | IA Generativa — IBERO |
| **Profesor** | Huber Girón |
| **Repositorio** | https://github.com/JoseLuis0022/reportes-academicos |
| **Sitio publicado** | https://joseluis0022.github.io/reportes-academicos/ |
| **Usuario GitHub** | JoseLuis0022 (`joseluismacedo.lego@gmail.com`) |
| **Ruta local** | `/Users/joseluismacedo/Desktop/Practica IA` |

---

## Setup de sesión (leer primero)

```bash
cd "/Users/joseluismacedo/Desktop/Practica IA"
git status   # confirmar que el repo está limpio
```

Si la carpeta no tiene `.git` (sesión en otro equipo):
```bash
git clone https://github.com/JoseLuis0022/reportes-academicos.git "/Users/joseluismacedo/Desktop/Practica IA"
cd "/Users/joseluismacedo/Desktop/Practica IA"
git config user.email "joseluismacedo.lego@gmail.com"
git config user.name "JoseLuis0022"
```

---

## Estructura de carpetas (definitiva)

```
/Users/joseluismacedo/Desktop/Practica IA/
│
│  ── Archivos raíz del sitio ──────────────────────────────
├── CLAUDE.md                    ← este archivo (memoria del proyecto)
├── _config.yml                  ← configuración Jekyll + Just the Docs
├── index.md                     ← portada del sitio (nav_order: 1)
├── practica1.md                 ← Práctica 1 (nav_order: 2)
├── practica2.md                 ← Práctica 2 (nav_order: 3)
├── practica3.md                 ← Práctica 3 (nav_order: 4)
├── practica4.md                 ← Práctica 4 (nav_order: 5)
├── practica5.md                 ← Práctica 5 (nav_order: 6)
├── practica6.md                 ← Práctica 6 (nav_order: 7)
├── uso-ia.md                    ← transparencia IA (nav_exclude: true)
├── .gitignore                   ← incluye .env / *.env (API keys nunca a git)
│
│  ── Código de prácticas 4-6 (backend/frontend funcionales) ──
├── practica4/                   ← Copilotos: backend FastAPI + frontend + scripts de prueba
│   ├── backend/main.py · requirements.txt
│   ├── frontend/index.html · app.js · styles.css
│   └── run_tests.py · test_results.json · comparison.json · injection_test.json
├── practica5/                   ← Ollama vs OpenRouter
│   ├── backend/main.py · requirements.txt · .env (NO en git) · .env.example
│   ├── frontend/index.html · app.js · styles.css
│   └── run_tests.py · comparison_results.json
├── practica6/                   ← LED agent + MQTT
│   ├── backend/main.py · requirements.txt
│   └── run_tests.py · generate_report.py
│
│  ── Plantillas Jekyll ─────────────────────────────────────
├── _includes/
│   ├── head_custom.html         ← skip link + favicon JS
│   └── footer_custom.html       ← footer con foto de perfil
│
│  ── Recursos estáticos ────────────────────────────────────
├── assets/
│   ├── css/
│   │   └── custom.css           ← sistema de diseño dorado/oscuro (563 líneas)
│   ├── files/                   ← PDFs u otros adjuntos (vacío por ahora)
│   └── img/
│       ├── perfil.jpeg          ← foto de perfil 800×800px
│       ├── practica2/           ← gráficas PNG del benchmark
│       │   ├── exp_a_boxplot.png
│       │   ├── exp_a_latencia.png
│       │   ├── exp_a_tokens_per_second.png
│       │   ├── exp_b_temperature.png
│       │   ├── exp_b_top_k.png
│       │   └── exp_b_top_p.png
│       ├── practica6/           ← gráficas del agente LED (matriz confusión, latencia, etc.)
│       └── (practicaN/)         ← carpeta por práctica para sus imágenes
│
│  ── Datos de experimentos ─────────────────────────────────
├── data/
│   ├── exp_a_results.csv        ← 300 filas — Exp B Práctica 2
│   ├── exp_b_results.csv        ← 900 filas — Exp C Práctica 2
│   ├── resultados_llm_led_raw.csv, resumen_metricas.csv, classification_report.csv,
│   │   errores.csv, instrumento_supervision_llm_led.xlsx  ← Práctica 6 (120 pruebas)
│
│  ── Scripts Python ────────────────────────────────────────
└── scripts/
    ├── benchmark_utils.py       ← funciones compartidas (API, métricas, CSV)
    ├── benchmark_exp_a.py       ← Exp B: comparación de modelos
    ├── benchmark_exp_b.py       ← Exp C: variación de parámetros
    └── generate_plots.py        ← genera 6 gráficas matplotlib

── Carpeta local (NO en git) ────────────────────────────────
_local/                          ← archivos de trabajo, ignorado por .gitignore
├── Guia de diseño.html          ← referencia del sistema de diseño
├── HANDOFF.md                   ← historial de sesiones anteriores
└── plan_practica2.md            ← plan de la Práctica 2
```

---

## Cómo hacer commit y push

```bash
cd "/Users/joseluismacedo/Desktop/Practica IA"
git add <archivos específicos>        # NUNCA git add -A sin revisar
git commit -m "Descripción del cambio"
git push
```

Verificar deploy de GitHub Pages:
```bash
gh run list --repo JoseLuis0022/reportes-academicos --limit 3
```

El deploy tarda ~2-3 minutos en reflejarse en el sitio.

---

## Cómo funciona el deploy

- **Plataforma:** GitHub Pages — rama `main`, directorio raíz `/`
- **Motor:** Jekyll con `remote_theme: just-the-docs/just-the-docs`
- **Trigger:** automático al hacer `git push` a `main`
- **CLI autenticada:** `gh` como JoseLuis0022 con scope `repo` y `workflow`

---

## Cómo modificar el índice (index.md)

Agregar la nueva práctica en la **tabla** y en **Navegación**:

```markdown
| 3 | [Nombre práctica](practica3/) | Tema breve |

- [Práctica 3 – Título](practica3/)
```

---

## Cómo crear una nueva práctica

1. Crear `practicaN.md` en la raíz con front matter:
   ```yaml
   ---
   layout: default
   title: "Práctica N – Título"
   nav_order: N+1
   ---
   ```
2. Estructura a seguir (igual que `practica2.md`):
   - Tabla de metadatos (modalidad, fecha, curso, profesor, herramientas)
   - Secciones `## N. Título` con separadores `---`
   - Blockquotes `>` para citas o respuestas de modelos
3. Actualizar `index.md`
4. Si tiene imágenes: guardar en `assets/img/practicaN/`
5. Commit y push

---

## Cómo modificar un archivo existente

```bash
# Editar con Claude (Edit tool) o directamente, luego:
git add practica1.md
git commit -m "Actualiza práctica 1: descripción"
git push
```

---

## Sistema de diseño — NO modificar sin razón

Tokens en `assets/css/custom.css`:

| Token | Valor | Uso |
|-------|-------|-----|
| `--gold` | `#C9962A` | Color de marca |
| `--gold-l` | `#F0C84A` | Hover, highlights |
| `--gold-d` | `#8C6518` | Dark accent |
| `--bg` | `#FAF6EE` | Fondo crema del contenido |
| `--sb-bg` | `#0D0D0D` | Sidebar oscuro |
| `--g-dark` | `148deg, #1A1210 → #0C0806` | Header, thead tablas |
| `--g-footer` | `155deg, #C9962A → #5A3D08` | Footer |
| `--txt-1` | `#1A1208` | Headings |
| `--txt-2` | `#4A3820` | Body text |

Principios: mobile-first (375/768/1024px), `clamp()` en tipografía,
touch targets ≥44px, `prefers-reduced-motion`, `focus-visible`.

---

## Ollama — verificar modelos antes de cualquier experimento

```bash
ollama list
```

Modelos confirmados instalados (verificado 24 de junio de 2026 — **reemplaza la lista de
junio 2026 usada en Prácticas 1-3**: `tinyllama`, `phi4-mini`, `llama3.2:3b`, `mistral:7b` y
`qwen2.5-coder:14b` ya NO están instalados en este equipo):

| Modelo | Parámetros | Uso recomendado |
|--------|-----------|-----------------|
| `gemma3:4b` | 4B | Modelo principal usado en Prácticas 4-6 ⭐ |
| `qwen2.5:7b` | 7.61B | Alta calidad, usado en Práctica 5 |
| `qwen3:8b` | 8.2B | Máxima calidad + modo thinking |
| `qwen3-toolcalling:latest` | — | Especializado en tool/function calling |

**Regla:** correr `ollama list` al inicio de cada práctica nueva — la lista de modelos
instalados cambia entre sesiones. `ollama pull <modelo>` solo si la práctica exige uno
específico que no esté disponible.

---

## Scripts de benchmark (Práctica 2)

```bash
cd "/Users/joseluismacedo/Desktop/Practica IA"

python3 scripts/benchmark_exp_a.py   # Exp B: 3 modelos × 100 ciclos (~40 min)
python3 scripts/benchmark_exp_b.py   # Exp C: 9 configs × 100 ciclos (~45 min)
python3 scripts/generate_plots.py    # genera PNGs en assets/img/practica2/
```

Dependencias:
```bash
pip3 install pandas matplotlib tqdm --break-system-packages
```

API Ollama local: `http://localhost:11434/api/generate`

---

## Estado del portafolio

| # | Práctica | Tema | Estado |
|---|----------|------|--------|
| 1 | Práctica 1 | 7 modelos LLM con Ollama — instalación, comparación y reflexión | ✅ Completa |
| 2 | Práctica 2 | Benchmark: matriz de decisión + comparación de modelos + variación de parámetros | ✅ Completa |
| 3 | Práctica 3 | Chatbot con LLM Local (Ollama + FastAPI, comparación con Page Assist) | ✅ Completa |
| 4 | Práctica 4 | Copilotos especializados con Ollama: perfiles, comparación genérico vs especializado, prompt injection | ✅ Completa |
| 5 | Práctica 5 | APIs LLM externas (OpenRouter) vs Ollama local: costo, latencia, calidad | ✅ Completa |
| 6 | Práctica 6 | Evaluación de arquitecturas LLM + MQTT: agente clasificador LED con métricas de clasificación | ✅ Completa |

---

## Hallazgos clave ya documentados

**Práctica 1:**
- `gemma3:4b` — mejor desempeño general
- `qwen3:8b` — único con modo thinking visible
- `tinyllama` — peor desempeño (confundió LLM con LL.M.)

**Práctica 2:**
- `llama3.2:3b` — más rápido (61.76 TPS, 2,802 ms)
- `phi4-mini:latest` — mejor calidad (8.25/10) ⭐
- Configuración óptima: `temperature=0.5`, `top_p=0.75`, `top_k=40`
- TPS estable con cualquier parámetro de muestreo (cuello de botella en capas del transformer)
- Plataforma elegida para proyecto final: APIs en nube (OpenAI + Anthropic + OpenRouter)

**Práctica 4:**
- Hallazgo principal: el perfil `generico` alucinó el mecanismo de la odometría diferencial (lo describió como visión por cámaras/LiDAR en vez de encoders de rueda); el perfil `robotica` lo identificó correctamente.
- `gemma3:4b` filtró su `system_prompt` completo ante un ataque simple de prompt injection (sin guardrails nativos).
- Modelos instalados cambiaron respecto a versiones anteriores: `llama3.2:3b`/`mistral:7b`/`tinyllama`/`phi4-mini` ya no están en `ollama list`; modelos vigentes: `gemma3:4b`, `qwen2.5:7b`, `qwen3:8b`, `qwen3-toolcalling`. Verificar siempre con `ollama list` antes de cada práctica nueva.

**Práctica 5:**
- Comparación Ollama (`gemma3:4b`) vs OpenRouter (`gpt-4o-mini`, `llama-3.1-8b-instruct`) con el mismo prompt técnico de robótica.
- Solo `gpt-4o-mini` reprodujo correctamente las ecuaciones canónicas de cinemática diferencial; los otros dos cometieron errores físicos/no estándar.
- OpenRouter fue 3–5x más rápido que Ollama local en CPU (sin GPU dedicada).
- API key de OpenRouter del usuario almacenada en `practica5/backend/.env` (excluido de git vía `.gitignore`); cuenta con límite de $4 USD.

**Práctica 6:**
- Arquitectura LLM → FastAPI → MQTT con `gemma3:4b`: 93.33% accuracy, 100% validez de esquema JSON y 100% publicación MQTT en 120 pruebas.
- Errores 100% concentrados en instrucciones metafóricas ("ilumina/oscurece el cuarto") que no mencionan literalmente el LED.
- Se usó un broker **Mosquitto local** en vez del broker público `mqtt.mecatronica-ibero.mx` de la guía oficial, por decisión explícita del usuario (evitar tráfico de prueba a infraestructura universitaria compartida). Mismo tópico (`public/llm-led/cmd`) y esquema de mensaje.
