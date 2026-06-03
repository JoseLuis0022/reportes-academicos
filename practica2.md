---
layout: default
title: "Práctica 2 – Benchmark de LLM"
nav_order: 3
---

# Práctica 2 – Benchmark de LLM

| | |
|---|---|
| **Modalidad** | Individual |
| **Fecha** | Junio 2026 |
| **Curso** | IA Generativa — IBERO |
| **Profesor** | Huber Girón |
| **Herramientas** | Python 3.14 · Ollama 0.24 · pandas · matplotlib |

---

## 1. Objetivo

Diseñar y ejecutar un benchmark técnico de modelos LLM ejecutados localmente con Ollama, midiendo latencia, throughput (tokens por segundo) y calidad de respuesta. La práctica se divide en tres partes:

- **Experimento A** — matriz de decisión de plataformas para el proyecto final.
- **Experimento B** — comparar el rendimiento de tres modelos distintos bajo condiciones idénticas.
- **Experimento C** — analizar el impacto de los parámetros de generación (`temperature`, `top_p`, `top_k`) sobre el rendimiento del mejor modelo.

---

## 2. Conceptos técnicos clave

### 2.1 RAM, VRAM y precisión numérica

Los modelos LLM requieren cargar todos sus pesos en memoria durante la inferencia. La cantidad depende del número de parámetros y la precisión usada:

| Precisión | Bits/parámetro | Modelo 4B | Modelo 7B |
|-----------|---------------|-----------|-----------|
| FP32 | 32 | ~16 GB | ~28 GB |
| FP16 | 16 | ~8 GB | ~14 GB |
| INT8 | 8 | ~4 GB | ~7 GB |
| INT4 (Q4) | 4 | ~2 GB | ~3.5 GB |

En CPU (sin GPU dedicada), los modelos usan RAM del sistema. La cuantización INT4 o INT8 permite correr modelos de 7B en equipos con 8–16 GB de RAM, a cambio de una ligera reducción en calidad.

### 2.2 Tokens, latencia y sus componentes

Un **token** es la unidad mínima de procesamiento (aprox. 0.75 palabras en español). La latencia total de una respuesta se descompone en:

1. **Load duration** — tiempo para cargar el modelo en memoria (solo el primer ciclo o si se descargó).
2. **Prompt eval duration** — tiempo para procesar el prompt de entrada.
3. **Eval duration** — tiempo para generar la respuesta token a token.

La métrica clave de rendimiento es **tokens por segundo (TPS)**: `eval_count / (eval_duration_ns / 1e9)`.

### 2.3 Parámetros de generación evaluados

| Parámetro | Descripción | Rango usado |
|-----------|-------------|-------------|
| `temperature` | Controla aleatoriedad: valores bajos → respuestas más deterministas | 0.1 · 0.5 · 0.9 |
| `top_p` | Nucleus sampling: considera solo los tokens cuya probabilidad acumulada ≤ p | 0.50 · 0.75 · 0.95 |
| `top_k` | Considera solo los k tokens más probables en cada paso | 10 · 40 · 80 |

---

## 3. Entorno y metodología

### 3.1 Hardware

- **Equipo:** MacBook Pro (Apple Silicon)
- **RAM:** sistema (CPU inference)
- **Ollama:** v0.24.0

### 3.2 Llamada a la API de Ollama

Los scripts usan la API REST local de Ollama (`http://localhost:11434/api/generate`) con `stream: false` para obtener todas las métricas en una sola respuesta:

```python
def ollama_call(model, prompt, params, timeout=180):
    payload = {"model": model, "prompt": prompt, "stream": False, **params}
    r = requests.post("http://localhost:11434/api/generate",
                      json=payload, timeout=timeout)
    r.raise_for_status()
    return r.json()
```

### 3.3 Prompt utilizado

El mismo prompt en todos los experimentos, para garantizar comparabilidad:

> *"Explica en menos de 100 palabras la diferencia entre Inteligencia Artificial, Machine Learning e IA Generativa."*

### 3.4 Métrica de calidad heurística

Se implementó una función automática de calidad (escala 0–10) basada en tres criterios:

```python
def quality_score(text):
    length_score  = min(len(text) / 500, 1.0)          # hasta 4 puntos
    unique_ratio  = len(set(words)) / len(words)        # hasta 3 puntos
    kw_score      = keywords_found / total_keywords     # hasta 3 puntos
    return length_score * 4 + unique_ratio * 3 + kw_score * 3
```

> ⚠️ Esta métrica es orientativa. Las respuestas fueron revisadas manualmente para validar coherencia y precisión académica.

---

## 4. Experimento A — Matriz de decisión para proyecto final

Para el proyecto final se evaluaron distintas plataformas de implementación de modelos de lenguaje (LLM), considerando factores como costo, latencia, privacidad, facilidad de implementación, escalabilidad y compatibilidad con la arquitectura del sistema propuesto.

El proyecto propuesto implementará una arquitectura basada completamente en servicios de nube mediante APIs, permitiendo escalabilidad, modularidad y reducción del costo inicial de infraestructura.

| Plataforma | Costo inicial | Costo operativo | Latencia | Privacidad | Implementación | Modelo | Escalabilidad | Notas |
|---|---|---|---|---|---|---|---|---|
| APIs en nube (OpenAI + Anthropic + OpenRouter) | **Bajo.** No requiere compra de hardware ni servidores dedicados. | **Variable.** Se paga por uso según tokens procesados y llamadas API. | **Baja–Media.** Las respuestas suelen generarse en pocos segundos dependiendo del modelo y complejidad. | **Media–Alta.** Los datos se procesan en servidores externos con medidas de seguridad del proveedor. | **Media.** Requiere integración de APIs, autenticación y automatización de flujos. | **Whisper, GPT-4.1 mini, GPT-5.1, Claude Haiku 4.5 y Claude Sonnet 4.6.** Cada modelo se usa según el tipo de tarea. | **Alta.** Puede aumentar usuarios y consultas sin necesidad de ampliar infraestructura propia. | Arquitectura completamente en nube. Se emplea routing inteligente: tareas simples usan modelos económicos y tareas complejas usan modelos avanzados para optimizar costos y rendimiento. |

---

## 5. Experimento B — Comparación de modelos

### 5.1 Configuración

| Parámetro | Valor |
|-----------|-------|
| Modelos | `gemma3:4b`, `phi4-mini:latest`, `llama3.2:3b` |
| Ciclos por modelo | 100 |
| Total de llamadas | 300 |
| temperature | 0.7 |
| top_p | 0.9 |
| top_k | 40 |
| num_predict | 200 |

### 5.2 Resultados

Promedios sobre 100 ciclos por modelo:

| Modelo | Fabricante | TPS media | Latencia media (ms) | Load time (ms) | Calidad media |
|--------|-----------|-----------|---------------------|----------------|---------------|
| `llama3.2:3b` | Meta | **61.76** ⚡ | **2,802** | 98.8 | 7.98 |
| `phi4-mini:latest` | Microsoft | 48.69 | 3,371 | 111.1 | **8.25** ⭐ |
| `gemma3:4b` | Google | 43.81 | 3,614 | 216.3 | 7.57 |

### 5.3 Gráficas

**Latencia total por ciclo (100 iteraciones por modelo):**

![Latencia por ciclo]({{ site.baseurl }}/assets/img/practica2/exp_a_latencia.png)

**Tokens por segundo — media y desviación estándar:**

![Tokens por segundo]({{ site.baseurl }}/assets/img/practica2/exp_a_tokens_per_second.png)

**Distribución de latencia (boxplot):**

![Boxplot latencia]({{ site.baseurl }}/assets/img/practica2/exp_a_boxplot.png)

### 5.4 Análisis

- **`llama3.2:3b`** fue el más rápido (61.76 TPS, 2,802 ms), gracias a su menor número de parámetros (3.21B). Es la opción ideal cuando la velocidad es prioritaria.
- **`phi4-mini:latest`** obtuvo la mejor calidad (8.25/10) pese a ser el segundo más pequeño (3.8B), confirmando la eficiencia de su arquitectura Microsoft. Fue seleccionado para el Experimento C.
- **`gemma3:4b`** tuvo el mayor tiempo de carga (216 ms vs ~100 ms de los otros), posiblemente por diferencias en cuantización. Su calidad fue la más baja del grupo.
- La desviación estándar de `phi4-mini` en latencia fue alta (σ = 902 ms), indicando mayor variabilidad según la complejidad interna de cada respuesta.

---

## 6. Experimento C — Variación de parámetros

**Modelo:** `phi4-mini:latest` (ganador de calidad en Exp B)

### 6.1 Configuración

| Dimensión | Valores probados | Parámetros fijos |
|-----------|-----------------|-----------------|
| `temperature` | 0.1 · 0.5 · 0.9 | top_p=0.75, top_k=40 |
| `top_p` | 0.50 · 0.75 · 0.95 | temperature=0.5, top_k=40 |
| `top_k` | 10 · 40 · 80 | temperature=0.5, top_p=0.75 |
| **Ciclos por config** | **100** | **Total: 900 llamadas** |

### 6.2 Temperatura (`temperature`)

| temperature | TPS media | Latencia media (ms) | Calidad media |
|-------------|-----------|---------------------|---------------|
| 0.1 | 48.71 | **2,866** | 8.23 |
| 0.5 | **48.99** | 3,056 | **8.26** |
| 0.9 | 48.54 | 3,236 | 8.17 |

**Observación:** temperatura alta (0.9) aumenta la latencia ~370 ms respecto a temperatura baja (0.1), ya que el modelo explora más tokens alternativos. La calidad es ligeramente mejor en valores medios (0.5).

### 6.3 Nucleus sampling (`top_p`)

| top_p | TPS media | Latencia media (ms) | Calidad media |
|-------|-----------|---------------------|---------------|
| 0.50 | 48.76 | 3,021 | **8.30** ⭐ |
| 0.75 | 48.61 | 3,163 | 8.16 |
| 0.95 | 48.73 | **3,076** | 8.27 |

**Observación:** `top_p=0.50` (vocabulario más restringido) produjo la mejor calidad (8.30) y una latencia moderada. Un `top_p` alto amplía el espacio de búsqueda sin mejorar necesariamente la calidad.

### 6.4 Top-K sampling (`top_k`)

| top_k | TPS media | Latencia media (ms) | Calidad media |
|-------|-----------|---------------------|---------------|
| 10 | 48.80 | 3,204 | 8.19 |
| 40 | **48.83** | **3,048** | 8.22 |
| 80 | 48.80 | 3,122 | **8.24** |

**Observación:** el impacto de `top_k` es mínimo en TPS, con diferencias menores a 0.1 token/seg. La latencia más baja se obtuvo con `top_k=40` (valor medio). `top_k=80` ofrece la mayor calidad marginalmente.

### 6.5 Gráficas

**Efecto de temperature en TPS y latencia:**

![Temperatura]({{ site.baseurl }}/assets/img/practica2/exp_b_temperature.png)

**Efecto de top_p en TPS y latencia:**

![top_p]({{ site.baseurl }}/assets/img/practica2/exp_b_top_p.png)

**Efecto de top_k en TPS y latencia:**

![top_k]({{ site.baseurl }}/assets/img/practica2/exp_b_top_k.png)

### 6.6 Análisis general del Experimento C

Los tres parámetros muestran un comportamiento estable en TPS (~48.7 tokens/seg en todos los casos), lo que indica que `phi4-mini` en CPU no ve limitado su throughput por la configuración de muestreo. Sin embargo, **la latencia sí varía** con `temperature`: a mayor aleatoriedad, el modelo toma más tiempo por token. El parámetro de mayor impacto práctico fue `temperature`.

---

## 7. Tabla comparativa final

| Configuración óptima | Parámetro | Valor recomendado | Justificación |
|----------------------|-----------|-------------------|---------------|
| Mayor velocidad | Modelo | `llama3.2:3b` | 61.76 TPS, menor latencia |
| Mayor calidad | Modelo | `phi4-mini:latest` | 8.25/10, arquitectura eficiente |
| Menor latencia en temp | `temperature` | 0.1 | 2,866 ms media |
| Mayor calidad en sampling | `top_p` | 0.50 | calidad 8.30/10 |
| Balance calidad/latencia | `top_k` | 40 | 3,048 ms, calidad 8.22 |

---

## 8. Reflexión

### ¿Qué modelo tuvo menor latencia promedio?

`llama3.2:3b` con 2,802 ms de media, gracias a sus 3.21B parámetros (el menor del grupo). En sistemas con CPU sin aceleración GPU, el tamaño del modelo es el factor dominante de latencia.

### ¿Cuál fue el impacto de `temperature` en la calidad de respuestas?

El impacto fue modesto pero medible: temperatura 0.5 produjo la mejor calidad (8.26) y temperatura 0.9 la peor (8.17). Temperaturas altas introducen más variabilidad que puede generar respuestas menos precisas o más dispersas, aunque también más creativas. Para tareas académicas o técnicas, valores entre 0.3 y 0.7 son adecuados.

### ¿Cuándo conviene usar un modelo en CPU vs GPU?

La CPU es adecuada para prototipos, pruebas locales, datos sensibles y cuando la latencia de segundos es aceptable. La GPU se vuelve indispensable cuando se requieren respuestas en tiempo real (< 500 ms), múltiples usuarios simultáneos o modelos de más de 13B parámetros. En este experimento, los tres modelos corrieron exclusivamente en CPU obteniendo resultados usables para investigación.

### ¿Cómo afecta `top_k` bajo vs alto a la diversidad de respuestas?

Un `top_k=10` restringe el vocabulario a los 10 tokens más probables en cada paso, generando respuestas más predecibles y repetitivas. Un `top_k=80` permite mayor diversidad léxica. En este experimento, la diferencia de calidad fue pequeña (8.19 vs 8.24), pero en tareas creativas o de generación de texto variado, valores altos de `top_k` producen resultados más ricos.

### ¿Qué aprendiste sobre la relación tokens/segundo y tamaño del modelo?

Existe una relación inversa clara: a mayor número de parámetros, menores TPS en CPU. `llama3.2:3b` (3.21B parámetros) logró 61.76 TPS, mientras `gemma3:4b` (4B parámetros) solo alcanzó 43.81 TPS. Sin embargo, **más pequeño no significa mejor calidad**: `phi4-mini:latest` con 3.8B obtuvo la mayor calidad (8.25), demostrando que la arquitectura y el entrenamiento importan tanto como el tamaño.

### ¿Por qué los parámetros de muestreo apenas afectaron el TPS?

Porque en inferencia CPU el cuello de botella está en la multiplicación de matrices (operaciones de atención sobre los pesos del modelo), no en el algoritmo de muestreo. Los parámetros `temperature`, `top_p` y `top_k` solo afectan el paso final de selección de token, que es computacionalmente trivial comparado con las capas del transformer.

---

## 9. Conclusión

Esta práctica permitió caracterizar cuantitativamente el rendimiento de tres modelos LLM en un entorno local CPU y definir la plataforma óptima para el proyecto final. Los resultados muestran que **`phi4-mini:latest` ofrece el mejor balance calidad/tamaño** para aplicaciones académicas, mientras que **`llama3.2:3b` es la opción óptima en escenarios donde la latencia es crítica**.

El Experimento C confirmó que los parámetros de muestreo tienen un impacto menor en rendimiento cuando se trabaja con modelos pequeños en CPU, pero que `temperature` sigue siendo el más relevante para controlar el estilo de las respuestas. La configuración recomendada para uso académico es: `temperature=0.5`, `top_p=0.75`, `top_k=40`.

---

*Práctica elaborada con apoyo de **Claude (Anthropic)** para la estructuración del documento. Los experimentos, scripts, datos y análisis fueron ejecutados y validados por el estudiante.*  
*Curso IA Generativa — IBERO · Junio 2026*
