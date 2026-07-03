---
layout: default
title: "Práctica 5 – APIs LLM Externas vs Ollama Local"
nav_order: 6
---

# Práctica 5 – Uso de APIs Externas para LLM y Comparación con Ollama Local

| | |
|---|---|
| **Modalidad** | Equipo |
| **Integrantes** | Jose Luis Macedo Escamilla · Fernanda Torres Abaroa · Alfredo José Mérida López |
| **Fecha** | Junio 2026 |
| **Curso** | IA Generativa — IBERO |
| **Profesor** | Huber Girón |
| **Herramientas** | Python 3 · FastAPI · Ollama (local) · OpenRouter API (externo) |

---

## 1. Objetivo

Explicar las diferencias entre ejecutar un LLM localmente (Ollama) y consumir un LLM vía API externa; configurar la API key de forma segura (variables de entorno, nunca en el repositorio); comparar al menos dos modelos externos contra Ollama local en el mismo prompt, midiendo latencia y tokens.

---

## 2. Decisión de proveedor externo

La guía original sugiere Gemini API y GroqCloud. Este equipo ya cuenta con una cuenta de **OpenRouter**, que actúa como gateway unificado hacia decenas de proveedores (OpenAI, Meta, Google, Mistral, etc.) con un único API key y facturación consolidada — opción ya elegida como plataforma del proyecto final según la Práctica 2. Se usó OpenRouter para acceder a **dos modelos externos de bajo costo**, manteniendo el espíritu de la comparación "local pequeño / remoto cerrado / remoto abierto":

| Proveedor | Modelo | Tipo |
|-----------|--------|------|
| Ollama (local) | `gemma3:4b` | Local pequeño |
| OpenRouter → OpenAI | `openai/gpt-4o-mini` | Remoto cerrado, bajo costo |
| OpenRouter → Meta | `meta-llama/llama-3.1-8b-instruct` | Remoto abierto, bajo costo |

---

## 3. Manejo seguro de la API key

La API key de OpenRouter se almacena en `practica5/backend/.env` (no versionado), cargada con `python-dotenv`. Se agregó `.env` y `*.env` al `.gitignore` del repositorio para evitar que se publique por accidente. `practica5/backend/.env.example` documenta la variable requerida sin exponer el valor real:

```
OPENROUTER_API_KEY=tu_api_key_aqui
```

**Nota de privacidad:** no se envió ningún dato personal, contraseña, información institucional sensible ni dato de terceros en los prompts de prueba — únicamente el prompt técnico de robótica descrito abajo.

---

## 4. Arquitectura

Se extendió el backend de la Práctica 4 con un parámetro `provider` (`ollama` | `openrouter`) que selecciona la URL y el formato de petición correspondiente, manteniendo el mismo perfil de copiloto (`robotica`) y los mismos parámetros de generación para los tres proveedores. Código en [`practica5/backend/main.py`](practica5/backend/main.py).

---

## 5. Prueba comparativa

**Prompt usado (idéntico en los tres proveedores):**
> "Explica qué es la odometría diferencial en un robot móvil de dos ruedas. Incluye: 1) explicación conceptual; 2) ecuaciones básicas; 3) ejemplo para estudiantes de ingeniería; 4) una limitación práctica. Responde en máximo 250 palabras."

**Configuración:** `temperature=0.7`, `top_p=0.9`, `max_tokens=300`, perfil "Copiloto de robótica móvil".

### Tabla de métricas (datos reales medidos)

| Proveedor / Modelo | Tiempo total (s) | Tokens entrada | Tokens salida | Tokens totales | Tokens/seg |
|---|---:|---:|---:|---:|---:|
| Ollama `gemma3:4b` | 12.75 | 137 | 300 | 437 | 39.69 |
| OpenRouter `gpt-4o-mini` | 3.90 | 135 | 300 | 435 | 76.87 |
| OpenRouter `llama-3.1-8b-instruct` | 2.47 | 168 | 300 | 468 | 121.41 |

### Tabla de evaluación cualitativa (escala 1–5)

| Criterio | `gemma3:4b` (Ollama) | `gpt-4o-mini` | `llama-3.1-8b` |
|---|:---:|:---:|:---:|
| Claridad conceptual | 4 | 5 | 4 |
| Precisión técnica de ecuaciones | 2 | 5 | 2 |
| Uso correcto de ecuaciones | 2 | 5 | 1 |
| Calidad del ejemplo | 3 (truncado, sin terminar) | 4 (truncado, sin terminar) | 3 (truncado) |
| Nivel adecuado para ingeniería | 4 | 5 | 3 |
| Alucinaciones/errores | Sí — fórmula del ángulo (`atan2`) no es la forma estándar | No | Sí — `v = r₁ω₁ + r₂ω₂` (suma en vez de promedio; fórmula físicamente incorrecta) |
| Utilidad final | 3 | 5 | 2 |

**Hallazgo clave:** las ecuaciones canónicas de cinemática diferencial son `v = (r/2)(v_L + v_R)` y `ω = (r/d)(v_R − v_L)`. Solo `gpt-4o-mini` las reprodujo correctamente. `gemma3:4b` propuso una fórmula de ángulo no estándar, y `llama-3.1-8b-instruct` cometió un error físico real (suma en lugar de promedio ponderado), confirmando que el tamaño/calidad del modelo importa específicamente para contenido técnico con ecuaciones, no solo para fluidez del texto.

Datos crudos completos en [`practica5/comparison_results.json`](practica5/comparison_results.json).

<div class="stat-box">
  <span class="stat-number">$0.005 USD</span>
  <span class="stat-label">Costo total de la prueba comparativa vía OpenRouter (modelos pagados: <code>gpt-4o-mini</code> — 435 tokens — y <code>meta-llama/llama-3.1-8b-instruct</code> — 468 tokens. <code>gemma3:4b</code> en Ollama local: $0.00, sin costo por ejecutarse en el equipo propio.)</span>
</div>

---

## 6. Reflexión comparativa

**1. ¿Cuál fue más rápido?**
`llama-3.1-8b-instruct` vía OpenRouter (2.47 s, 121.4 tok/s), seguido de `gpt-4o-mini` (3.90 s). Ollama local con `gemma3:4b` en CPU fue el más lento (12.75 s, 39.7 tok/s).

**2. ¿Cuál dio la mejor explicación técnica?**
`gpt-4o-mini`: fue el único con las ecuaciones de cinemática diferencial correctas.

**3. ¿Un modelo más grande siempre es mejor?**
No necesariamente por tamaño de parámetros puro: `llama-3.1-8b-instruct` (8B) cometió un error físico que `gemma3:4b` (4B, más pequeño) no cometió en la misma magnitud, aunque ambos fallaron en algo. La calidad del entrenamiento y alineamiento importa más que el conteo de parámetros en este caso puntual.

**4. ¿Qué diferencia hay entre usar Ollama local y una API externa?**
Local: sin costo por token, sin dependencia de internet, datos nunca salen del equipo, pero limitado por el hardware disponible (CPU, sin GPU dedicada → 3x más lento). Externo: rápido y consistente, pero depende de conectividad, tiene costo por token y envía el contenido del prompt a un tercero.

**5. ¿Qué riesgos implica enviar datos a terceros?**
Exposición de información sensible si el prompt contiene datos personales, institucionales o de propiedad intelectual; dependencia del proveedor para retención/uso de los datos según su política; necesidad de revisar el manejo de logs y cumplimiento (ej. GDPR) antes de enviar datos reales de producción.

**6. ¿Qué pasa si la API cambia de precio o desaparece?**
El uso de OpenRouter como gateway mitiga parcialmente este riesgo: si un modelo sube de precio o se retira, basta con cambiar el parámetro `model` en la petición sin reescribir el backend, ya que la interfaz hacia OpenRouter es uniforme entre proveedores.

**7. ¿Cuándo conviene Ollama local vs. API externa?**
Local: desarrollo, prototipado, datos sensibles, sin presupuesto recurrente, o uso offline. Externo: producción con SLA de latencia/calidad, picos de carga que el hardware local no soporta, o cuando se requiere el modelo de mayor calidad disponible en el mercado sin invertir en GPU propia.

**8. ¿Qué proveedor fue más fácil de integrar?**
OpenRouter, porque expone un único formato de API (compatible con el estándar de OpenAI) para múltiples modelos/proveedores, evitando reimplementar un cliente distinto por cada API (a diferencia de tener que integrar Gemini y Groq por separado, cada uno con su propio SDK).

**9. ¿Qué información técnica no fue publicada por el proveedor?**
OpenRouter no expone el `total_duration`/`load_duration` que sí entrega Ollama (tiempo de carga del modelo en memoria); solo se obtiene tiempo de respuesta medido en el cliente y conteo de tokens vía el campo `usage` estándar de OpenAI.

**10. ¿Qué tan estable fue la calidad entre proveedores con el mismo prompt y parámetros?**
Inestable en cuanto a corrección técnica: con parámetros idénticos, dos de los tres modelos (`gemma3:4b` y `llama-3.1-8b-instruct`) produjeron ecuaciones incorrectas o no estándar, mientras que solo `gpt-4o-mini` fue preciso — la calidad varió más por el modelo/proveedor que por los parámetros de generación.

---

## 7. Conclusiones

La comparación confirma que la elección de proveedor no es solo una decisión de costo o privacidad: en contenido técnico con ecuaciones, hubo diferencias reales de corrección entre modelos del mismo orden de tamaño (4B–8B), independientemente de si corrían local o en la nube. OpenRouter resultó práctico como gateway único para probar múltiples modelos sin reescribir integraciones, validando la decisión de plataforma tomada en la Práctica 2 para el proyecto final del curso.

**Costo:** la prueba comparativa completa vía OpenRouter (`gpt-4o-mini` + `meta-llama/llama-3.1-8b-instruct`) tuvo un costo total de **$0.005 USD**, frente a $0.00 de `gemma3:4b` ejecutado localmente con Ollama. Para un solo prompt de prueba el costo es marginal, pero a escala de producción (miles de solicitudes) esa diferencia por token es exactamente el factor que justifica evaluar un modelo local para cargas de trabajo de alto volumen y externo solo cuando se necesita la máxima precisión técnica.
