---
layout: default
title: "Práctica 3 – Chatbot con LLM Local (Ollama)"
nav_order: 4
---

# Práctica 3 – Chatbot con LLM Local (Ollama)

| | |
|---|---|
| **Modalidad** | Individual |
| **Fecha** | Junio 2026 |
| **Curso** | IA Generativa — IBERO |
| **Profesor** | Huber Girón |
| **Herramientas** | Python 3 · FastAPI · Uvicorn · Ollama · HTML/CSS/JS |

---

## 1. Objetivo

Implementar un chatbot de propósito general que utilice un modelo de lenguaje ejecutado localmente mediante Ollama, comprendiendo la arquitectura cliente-servidor de tres capas: frontend web, API intermediaria y motor de inferencia local. El objetivo técnico es capturar y visualizar métricas de rendimiento en tiempo real (latencia, tokens y velocidad de generación).

---

## 2. Arquitectura del sistema

```
[Usuario]
    ↓
[Frontend — HTML/CSS/JS]   ← index.html en el navegador
    ↓  POST /chat (JSON)
[Backend — FastAPI :8000]  ← main.py con Uvicorn
    ↓  POST /api/chat (JSON)
[Ollama API — :11434]      ← motor de inferencia local
    ↓
[Modelo LLM — llama3.2:3b]
```

| Capa | Tecnología | Responsabilidad |
|------|-----------|-----------------|
| **Frontend** | HTML · CSS · JavaScript | Interfaz de chat: selector de modelo, controles de parámetros, visualización de métricas |
| **Backend** | Python · FastAPI · Uvicorn | Valida la entrada, gestiona CORS, reenvía al motor y retorna métricas estructuradas |
| **Inferencia** | Ollama · `llama3.2:3b` | Ejecuta el modelo LLM localmente sin enviar datos a servicios externos |

El backend usa el endpoint `/api/chat` de Ollama (modo conversación con roles `system`/`user`/`assistant`) en lugar de `/api/generate`, lo que permite mantener historial de contexto y capturar las 8 métricas de rendimiento con `stream: false`.

---

## 3. Modelo utilizado

| Parámetro | Valor |
|-----------|-------|
| **Modelo** | `llama3.2:3b` |
| **Parámetros** | 3.21B |
| **Tamaño en disco** | ~2 GB |
| **Contexto** | 4 096 tokens |
| **temperature** | 0.7 |
| **top_p** | 0.9 |
| **repeat_penalty** | 1.1 |
| **num_predict** | 512 tokens máx. por respuesta |

---

## 4. Endpoint de la API

**`POST http://localhost:8000/chat`**

**Request:**
```json
{
  "message": "texto del usuario",
  "model": "llama3.2:3b",
  "temperature": 0.7,
  "top_p": 0.9,
  "num_predict": 512,
  "num_ctx": 4096,
  "repeat_penalty": 1.1
}
```

**Response:**
```json
{
  "output": "respuesta generada por el modelo",
  "model": "llama3.2:3b",
  "latency_ms": 10924,
  "prompt_tokens": 34,
  "completion_tokens": 9,
  "total_tokens": 43,
  "tokens_per_sec": 0.8
}
```

Las métricas se calculan a partir de los campos `prompt_eval_count`, `eval_count` y `eval_duration` que devuelve Ollama en cada respuesta.

---

## 5. Alternativa sin backend: extensión Page Assist

Durante el desarrollo de esta práctica se identificó una alternativa que cumple el objetivo de interactuar con modelos Ollama locales sin necesidad de implementar un servidor FastAPI: la extensión **Page Assist — Una Web UI para modelos de IA Locales**, disponible en la Chrome Web Store.

### ¿Qué hace Page Assist?

Page Assist es una extensión de navegador de código abierto que se conecta directamente a la API local de Ollama (`http://localhost:11434`) y proporciona una interfaz de chat completa. Incluye selector de modelos, historial de conversación, soporte para múltiples idiomas y funciones de análisis de páginas web.

### Comparación de enfoques

| Característica | Page Assist (extensión) | Solución construida (FastAPI) |
|---------------|------------------------|-------------------------------|
| **Instalación** | Un clic desde la Chrome Web Store | Requiere Python, dependencias y levantar servidor |
| **Backend propio** | No — se conecta directo a Ollama | Sí — servidor FastAPI personalizable |
| **Métricas detalladas** | Básicas | Personalizables (latencia, TPS, tokens) |
| **Personalización** | Limitada (configuración de la extensión) | Total — código propio en Python y JS |
| **Privacidad** | Local (sin datos externos) | Local (sin datos externos) |
| **Uso recomendado** | Uso personal rápido, exploración | Integración en aplicaciones, control fino |

### Cuándo usar cada opción

- **Page Assist:** cuando se necesita una UI funcional de forma inmediata sin configurar infraestructura.
- **FastAPI + frontend propio:** cuando se requiere personalizar el comportamiento, capturar métricas propias, integrar con otros sistemas o construir una aplicación web completa.

---

## 6. Resultados

La interfaz implementada permite al usuario seleccionar el modelo desde un menú desplegable, enviar mensajes y recibir respuestas con las siguientes métricas visibles:

- Latencia total de respuesta (ms)
- Tokens de entrada (prompt)
- Tokens de salida (completion)
- Velocidad de generación (tokens/seg)
- Nombre del modelo activo

Con `llama3.2:3b` se observaron tiempos de respuesta de entre 8 000 y 14 000 ms para respuestas de 50–200 palabras, con velocidades de 0.7–1.2 tokens/seg en CPU (sin GPU dedicada). Estos valores son consistentes con los resultados del benchmark de la Práctica 2 para el mismo modelo.

---

## 7. Conclusiones

Esta práctica demostró que implementar un chatbot funcional con un LLM local no requiere acceso a servicios en la nube ni claves de API externas. La arquitectura de tres capas separa claramente las responsabilidades: el frontend gestiona la experiencia del usuario, FastAPI actúa como capa de validación y traducción, y Ollama administra la inferencia.

La comparación con Page Assist evidencia que existen soluciones listas para usar que reducen el tiempo de implementación a cero, pero sacrifican la capacidad de personalización y el acceso a métricas detalladas. Construir el backend propio, aunque más costoso en tiempo inicial, da control total sobre el flujo de datos y permite extender el sistema fácilmente — por ejemplo, agregando autenticación, almacenamiento de conversaciones o integración con otras APIs.
