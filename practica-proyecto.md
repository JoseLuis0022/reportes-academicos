---
layout: default
title: "Proyecto"
nav_order: 8
---

# Proyecto Final — TORQUE: Sistema Operativo de IA para Talleres Mecánicos

| | |
|---|---|
| **Modalidad** | Equipo |
| **Integrantes** | Jose Luis Macedo Escamilla · Fernanda Torres Abaroa · Alfredo José Mérida López |
| **Curso** | IA Generativa — IBERO |
| **Profesor** | Huber Girón |
| **Herramientas** | n8n · WhatsApp · LLMs (OpenAI, Anthropic, OpenRouter) · Google Cloud · Cloudflare |

---

## Resumen

**TORQUE** es un sistema operativo de inteligencia artificial multiagente que administra la operación diaria de un taller mecánico completamente a través de WhatsApp: recibe mensajes de texto, notas de voz o fotografías, decide qué acción tomar, la ejecuta sobre los datos reales del negocio y, además, actúa de forma **proactiva** en segundo plano para vigilar el estado del taller sin que nadie se lo pida.

El documento de arquitectura (dirigido a un público de ingeniería) cubre, en orden:

- **Justificación:** el dolor operativo de los talleres mecánicos, el panorama competitivo y la cuña de mercado elegida.
- **Arquitectura general:** por qué se optó por un diseño **multiagente** implementado en **n8n**, con un agente **orquestador** que delega tareas a agentes especializados siguiendo reglas críticas de delegación.
- **Roles y permisos:** cinco niveles de acceso resueltos por número de teléfono de WhatsApp.
- **Ingeniería de prompts:** estructura común de *system prompt* por agente y reglas de negocio como fuente de verdad.
- **Loop agéntico:** ruteo de modelo según el nivel del usuario y límite de iteraciones por agente.
- **Proactividad:** tareas programadas que aplican criterio de negocio, no solo lectura de datos.
- **Modelo de datos**, con el ciclo de vida de una orden de servicio como la regla que más agentes consumen.
- **Manejo de errores y resiliencia:** verificación post-escritura y encadenamiento para peticiones complejas.
- **Herramientas e integraciones externas** y los modelos de LLM utilizados.
- **Fase de pruebas** técnicas en curso.

El despliegue completo de la documentación (con diagramas, capturas de los flujos en n8n y evidencia de campo) está embebido a continuación.

---

## Documentación completa

<div style="text-align:right; margin-bottom: 8px;">
  <a href="{{ site.baseurl }}/Proyecto/TORQUE_Documentacion_Arquitectura.html" target="_blank" rel="noopener">Abrir en pantalla completa ↗</a>
</div>

<iframe
  src="{{ site.baseurl }}/Proyecto/TORQUE_Documentacion_Arquitectura.html"
  title="TORQUE — Documentación de Arquitectura del Sistema Operativo de IA"
  style="width:100%; height:85vh; border:1px solid var(--border); border-radius:12px;"
  loading="lazy">
</iframe>
