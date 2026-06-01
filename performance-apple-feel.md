---
layout: default
title: "Rendimiento — Apple Feel"
nav_order: 3
---

# Rendimiento y experiencia de usuario — Apple Feel

10 principios para que cualquier app se sienta **rápida, fluida y premium**.

---

## 1. Optimiza "tiempo a respuesta", no "tiempo total"

La gente perdona que algo tarde 2–3 s **si responde de inmediato**.

- En cuanto el usuario haga click/tap: **feedback en menos de 100 ms** (cambio visual, estado "cargando", botón deshabilitado).
- Divide tareas largas en pasos: *Preparando… / Procesando… / Listo*.
- Muestra progreso real o estimado si pasa de 1 s.

**Regla rápida:**

| Tiempo | Percepción |
|:------:|-----------|
| < 100 ms | "Instantáneo" |
| 100–300 ms | OK |
| > 300 ms | Ya se siente lento |
| > 1 s | Pon indicador sí o sí |

---

## 2. Haz el trabajo pesado fuera del hilo principal (UI)

Este es **el punto #1 para fluidez**. El UI thread solo debe pintar y manejar input — todo lo demás, async.

| Plataforma | Herramienta recomendada |
|-----------|------------------------|
| **Web** | Web Workers / OffscreenCanvas / `requestIdleCallback` |
| **Mobile** | Hilos / background queues |
| **Desktop** | Threads / async; I/O y cómputo fuera del UI loop |

> **Patrón clave:** UI thread = pintar + input. Nada más.

---

## 3. Preserva 60/120 fps — presupuesto de frame

Si quieres animaciones suaves, cada frame tiene un presupuesto fijo que incluye JS + layout + paint + render:

| FPS objetivo | Presupuesto por frame |
|:------------:|:--------------------:|
| 60 fps | **16.7 ms** |
| 120 fps | **8.3 ms** |

**Tips para mantenerse dentro del presupuesto:**

- [ ] Reduce layouts y reflows (web)
- [ ] Virtualiza listas largas
- [ ] Precalcula, cachea y memoiza

---

## 4. "Rendimiento percibido" con skeletons y placeholders

Apple no te deja ver "nada" — te deja ver "algo". El secreto es que **el layout no brinque**.

- **Skeleton loading** — bloques con shimmer del tamaño real del contenido
- **Listas placeholder** — con altura real antes de cargar datos
- **Blur preview (LQIP)** — imagen de baja resolución mientras carga la real

> **Clave:** layout estable = sensación premium.

---

## 5. Preload inteligente (sin quemar batería)

Mac se siente rápido porque **anticipa**. Aplica las mismas ideas:

- Prefetch de la siguiente pantalla si el usuario está por navegar
- Cache de resultados frecuentes
- Warm-up de conexiones (HTTP keep-alive)
- Lazy-load de todo lo que no es visible ni crítico

**Truco:** *carga primero lo visible, lo demás después*.

---

## 6. Haz rápidas las operaciones comunes — p95 / p99

No optimices solo el promedio. El usuario recuerda el peor caso.

**Mide estos tiempos en percentiles:**

- Tiempo de arranque (cold start / warm start)
- Tiempo de interacción (tap to response)
- Tiempo de respuesta de API

> **Regla:** optimiza el peor 5% (p95). Es lo que el usuario recuerda.

---

## 7. Evita "jank" por GC / memoria

Las pausas por recolección de basura o memory leaks matan la sensación de "seda".

- [ ] Evita crear miles de objetos por frame (en animaciones)
- [ ] Reutiliza buffers y arrays
- [ ] Elimina listeners, timers y referencias globales al desmontar componentes
- [ ] En móviles: comprime imágenes, no uses resoluciones gigantes

---

## 8. Microinteracciones — el "sabor" Apple

Son pequeñas, pero cambian todo. **La consistencia es la clave** — el cerebro ama patrones.

| Elemento | Especificación |
|---------|--------------|
| Duración de animaciones | 150–250 ms |
| Easing | Suave / ease-out (nunca lineal) |
| Hover / pressed states | Siempre visibles y claros |
| Sonidos / haptics | Solo si la plataforma lo espera |
| Curva de transición | La misma en toda la app |

---

## 9. Input-first — que el app "agarre" el toque / click

Prioriza que el input se procese antes que cualquier otra tarea:

- **Scroll / resize / search** → debounce o throttle
- **Búsqueda** → muestra resultados anteriores + "actualizando…" mientras llegan los nuevos
- **Formularios** → validación incremental (no al enviar)

---

## 10. Instrumenta todo — lo que no se mide no se mejora

Define métricas concretas por plataforma:

### Web — Core Web Vitals

| Métrica | Qué mide |
|--------|---------|
| **LCP** | Largest Contentful Paint — cuándo carga lo principal |
| **INP** | Interaction to Next Paint — latencia de inputs |
| **CLS** | Cumulative Layout Shift — saltos de layout |
| Long tasks | Bloques > 50 ms en main thread |
| FPS scroll | Fluidez durante desplazamiento |

### Mobile / Desktop

- Cold start y warm start
- Frame drops durante scroll / animaciones
- Tiempo de respuesta a taps
- Memoria y CPU sostenidas bajo uso real

---

## Checklist rápido — "Apple Feel"

- [ ] Feedback visual inmediato (< 100 ms)
- [ ] UI nunca se bloquea por cómputo o I/O
- [ ] Scroll fluido (virtualización si hay listas largas)
- [ ] Skeletons + layout estable (sin saltos al cargar)
- [ ] Cache y prefetch de lo más común
- [ ] p95 / p99 bajo control y monitoreado
- [ ] Memory leaks y pausas de GC minimizadas
- [ ] Microinteracciones consistentes en toda la app

---

*Notas de ingeniería de rendimiento — compiladas para el portafolio de JoseLuis0022.*
