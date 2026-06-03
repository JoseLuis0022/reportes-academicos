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

La ruta definitiva del repo es `/Users/joseluismacedo/Desktop/Practica IA`.

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

## Cómo hacer commit y push

```bash
cd "/Users/joseluismacedo/Desktop/Practica IA"
git add <archivos específicos>        # NUNCA git add -A sin revisar
git commit -m "Descripción del cambio"
git push
```

Verificar que el deploy de GitHub Pages arrancó:
```bash
gh run list --repo JoseLuis0022/reportes-academicos --limit 3
```

El deploy tarda ~2-3 minutos en reflejarse en el sitio.

---

## Cómo funciona el deploy

- **Plataforma:** GitHub Pages
- **Rama:** `main`, directorio raíz `/`
- **Motor:** Jekyll con `remote_theme: just-the-docs/just-the-docs`
- **Trigger:** automático al hacer `git push` a `main`
- **CLI autenticada:** `gh` como JoseLuis0022 con scope `repo` y `workflow`

---

## Estructura del repositorio

```
/Users/joseluismacedo/Desktop/Practica IA/   ← raíz del repo
├── CLAUDE.md                          ← este archivo
├── _config.yml                        ← Jekyll: título, baseurl, tema, CSS
├── index.md                           ← Portada del sitio (nav_order: 1)
├── practica1.md                       ← Práctica 1 (nav_order: 2)
├── practica2.md                       ← Práctica 2 (nav_order: 3)
├── uso-ia.md                          ← Transparencia IA (nav_exclude: true)
├── .gitignore
├── _includes/
│   ├── head_custom.html               ← Skip link + favicon JS
│   └── footer_custom.html             ← Footer con foto de perfil
├── assets/
│   ├── css/custom.css                 ← Sistema de diseño completo (563 líneas)
│   └── img/
│       ├── perfil.jpeg                ← Foto de perfil 800×800px
│       └── practica2/                 ← 6 gráficas PNG del benchmark
├── data/
│   ├── exp_a_results.csv              ← 300 filas — Exp B Práctica 2
│   └── exp_b_results.csv              ← 900 filas — Exp C Práctica 2
└── scripts/
    ├── benchmark_utils.py
    ├── benchmark_exp_a.py
    ├── benchmark_exp_b.py
    └── generate_plots.py
```

Archivos locales que NO están en git (solo en el disco):
- `HANDOFF.md`, `plan_practica2.md`, `Guion.md`, `Contenido.txt`
- `practica1-llm-ollama.md`, `Guia de diseño.html`
- `foto de perfil.jpeg`, `reel_audio.mp3`, `reel_audio.txt`

---

## Cómo modificar el índice (index.md)

Agregar la nueva práctica en la **tabla de prácticas** y en la sección **Navegación**:

```markdown
## Prácticas
| # | Práctica | Tema |
|---|----------|------|
| 1 | [LLM locales con Ollama](practica1/) | ... |
| 2 | [Benchmark de LLM](practica2/) | ... |
| 3 | [Nueva práctica](practica3/) | Tema |   ← agregar aquí

## Navegación
- [Práctica 3 – Título](practica3/)           ← agregar aquí
```

---

## Cómo crear una nueva práctica

1. Crear `practicaN.md` con este front matter:
   ```yaml
   ---
   layout: default
   title: "Práctica N – Título"
   nav_order: N+1
   ---
   ```
2. Seguir la estructura de `practica2.md`:
   - Tabla de metadatos (modalidad, fecha, curso, profesor, herramientas)
   - Secciones numeradas `## N. Título`
   - Separadores `---` entre secciones principales
   - Blockquotes `>` para citas o respuestas de modelos
3. Actualizar `index.md` (ver sección anterior)
4. Si tiene imágenes: guardar en `assets/img/practicaN/`
5. Commit y push

---

## Cómo modificar un archivo existente

```bash
# Editar el archivo con Claude (Edit tool) o directamente
# Luego:
cd "/Users/joseluismacedo/Desktop/Practica IA"
git add practica1.md       # o el archivo que se modificó
git commit -m "Actualiza práctica 1: descripción del cambio"
git push
```

---

## Sistema de diseño — NO modificar sin razón

Tokens principales en `assets/css/custom.css`:

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

Principios aplicados: mobile-first (375/768/1024px), `clamp()` en tipografía,
touch targets ≥44px, `prefers-reduced-motion`, `focus-visible`.

---

## Ollama — verificar modelos antes de cualquier experimento

```bash
ollama list
```

Modelos confirmados instalados (junio 2026):

| Modelo | Parámetros | Uso recomendado |
|--------|-----------|-----------------|
| `tinyllama:1.1b-chat-v1-q8_0` | 1.1B | Pruebas rápidas |
| `phi4-mini:latest` | 3.8B | Mejor calidad/tamaño ⭐ |
| `llama3.2:3b` | 3.21B | Más rápido (61 TPS) ⚡ |
| `gemma3:4b` | 4B | Buena calidad general |
| `qwen2.5:7b` | 7.61B | Alta calidad |
| `mistral:7b` | 7B | Alta calidad |
| `qwen3:8b` | 8.2B | Máxima calidad + modo thinking |
| `gemma4:latest` | — | Disponible |
| `qwen2.5-coder:14b` | 14B | Especializado en código |
| `nomic-embed-text:latest` | — | Solo embeddings (no generativo) |

**Regla:** usar solo modelos ya instalados. Hacer `ollama pull <modelo>` únicamente
si la práctica exige uno específico no disponible.

---

## Scripts de benchmark (Práctica 2)

```bash
cd "/Users/joseluismacedo/Desktop/Practica IA"

# Experimento B: comparación de modelos (300 ciclos, ~40 min)
python3 scripts/benchmark_exp_a.py

# Experimento C: variación de parámetros (900 ciclos, ~45 min)
python3 scripts/benchmark_exp_b.py

# Generar 6 gráficas PNG en assets/img/practica2/
python3 scripts/generate_plots.py
```

Dependencias Python (instalar si faltan):
```bash
pip3 install pandas matplotlib tqdm --break-system-packages
```

API local de Ollama: `http://localhost:11434/api/generate`

---

## Estado actual del portafolio

| # | Práctica | Tema | Estado |
|---|----------|------|--------|
| 1 | Práctica 1 | Instalación y comparación de 7 modelos LLM con Ollama | ✅ Completa |
| 2 | Práctica 2 | Benchmark: matriz de decisión + comparación + variación de parámetros | ✅ Completa |

---

## Hallazgos clave ya documentados

**Práctica 1:**
- `gemma3:4b` — mejor desempeño general
- `qwen3:8b` — único con modo thinking visible
- `tinyllama` — peor desempeño (confundió "LLM" con "LL.M." Licenciatura en Leyes)

**Práctica 2:**
- `llama3.2:3b` — más rápido (61.76 TPS, 2,802 ms promedio)
- `phi4-mini:latest` — mejor calidad (8.25/10) ⭐ elegido para Experimento C
- Configuración óptima recomendada: `temperature=0.5`, `top_p=0.75`, `top_k=40`
- TPS no varía con parámetros de muestreo (cuello de botella en multiplicación matricial)
- Plataforma elegida para proyecto final: APIs en nube (OpenAI + Anthropic + OpenRouter)
