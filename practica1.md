---
layout: default
title: "Práctica 1 – LLM locales con Ollama"
nav_order: 2
---

# Práctica 1: Instalación, ejecución y comparación de modelos LLM locales con Ollama y Hugging Face

**Modalidad:** Equipo  
**Integrantes:** Jose Luis Macedo Escamilla · Fernanda Torres Abaroa · Alfredo José Mérida López  
**Fecha:** 1 de junio de 2026

---

## 1. Verificación de la instalación

```bash
$ ollama --version
ollama version is 0.24.0
```

---

## 2. Modelos instalados (`ollama ls`)

```
NAME                               ID              SIZE      MODIFIED
tinyllama:1.1b-chat-v1-q8_0        3746473cdb1e    1.2 GB    hace 13 min
phi4-mini:latest                   78fad5d182a7    2.5 GB    hace 13 min
mistral:7b                         6577803aa9a0    4.4 GB    hace 14 min
qwen2.5:7b                         845dbda0ea48    4.7 GB    hace 17 min
gemma3:4b                          a2af6cc3eb7f    3.3 GB    hace 20 min
llama3.2:3b                        a80c4f17acd5    2.0 GB    hace 24 min
```

---

## 3. Tabla comparativa de modelos

| Modelo | Fabricante | Tipo | Licencia | Parámetros | Idiomas reportados | Requerimiento sugerido | Comando | Tamaño en Ollama |
|--------|-----------|------|----------|------------|-------------------|----------------------|---------|-----------------|
| **Llama 3.2 3B Instruct** | Meta | LLM instruct, texto a texto | Llama 3.2 Community License | 3.21B | Inglés, alemán, francés, italiano, portugués, hindi, español y tailandés | Recomendable con 8 GB RAM o más | `ollama run llama3.2:3b` | 2.0 GB |
| **Gemma 3 4B IT** | Google DeepMind | LLM instruct multimodal, texto e imagen a texto | Gemma License | 4B | Más de 140 idiomas | Requiere Ollama 0.6+; recomendable 8 GB RAM | `ollama run gemma3:4b` | 3.3 GB |
| **Qwen2.5 7B Instruct** | Alibaba Cloud (Qwen Team) | LLM instruct causal | Apache 2.0 | 7.61B | Más de 29 idiomas (español, inglés, chino, francés, portugués, alemán, ruso, japonés, coreano…) | Recomendable 16 GB RAM o GPU | `ollama run qwen2.5:7b` | 4.7 GB |
| **Mistral 7B Instruct v0.3** | Mistral AI | LLM instruct con function calling | Apache 2.0 | 7B | Multilingüe; evaluar respuesta en español e inglés | Recomendable 16 GB RAM o GPU | `ollama run mistral:7b` | 4.4 GB |
| **Phi-4-mini-instruct** | Microsoft | LLM instruct compacto, decoder-only | MIT | 3.8B | 22 idiomas: árabe, chino, checo, danés, neerlandés, inglés, finés, francés, alemán, hebreo, húngaro, italiano, japonés, coreano, noruego, polaco, portugués, ruso, español, sueco, tailandés, turco y ucraniano | Diseñado para entornos con memoria restringida; requiere Ollama 0.5.13+ | `ollama run phi4-mini` | 2.5 GB |
| **TinyLlama 1.1B Chat** | TinyLlama | LLM chat compacto (arquitectura Llama 2) | Apache 2.0 | 1.1B | Principalmente inglés | Útil para equipos con recursos limitados; menor calidad esperada | `ollama run tinyllama:1.1b-chat-v1-q8_0` | 1.2 GB |
| **Qwen3 8B** | Alibaba Cloud (Qwen Team) | LLM instruct causal con modo *thinking* (razonamiento interno) | Apache 2.0 | 8.2B | 100+ idiomas y dialectos | Recomendable 16 GB RAM o GPU; requiere BF16 | `ollama run qwen3:8b` | 5.2 GB |

> **Nota:** "Parámetros" es el tamaño arquitectónico del modelo. "Tamaño en Ollama" es el espacio que ocupa la variante descargada (formato + cuantización), obtenido con `ollama ls`.

---

## 4. Prompts de prueba utilizados

Los mismos cuatro prompts se ejecutaron en todos los modelos:

- **Prompt 1 (Conceptual):** Explica la diferencia entre inteligencia artificial, aprendizaje automático, IA generativa y LLM para estudiantes universitarios. Responde en español, con tono académico y máximo 200 palabras.
- **Prompt 2 (Embeddings):** Dame un ejemplo sencillo de uso de embeddings en una búsqueda semántica dentro de un repositorio de documentos académicos.
- **Prompt 3 (Evaluación crítica):** Menciona tres riesgos académicos de usar LLM sin verificar fuentes. Incluye un ejemplo breve para cada riesgo.
- **Prompt 4 (Uso técnico ESP32):** Dame un ejemplo de cómo un estudiante de ingeniería podría usar un LLM para apoyar el desarrollo de un proyecto con ESP32, sin sustituir su aprendizaje.

---

## 5. Respuestas de los modelos

---

### 5.1 TinyLlama 1.1B Chat (`tinyllama:1.1b-chat-v1-q8_0`)

#### Prompt 1 – Conceptual

> Los conceptos de IA, ML, IA generativa y LLM se explican como una jerarquía. La IA es el campo general que usa herramientas computacionales para actuar automáticamente. El aprendizaje automático (MLP) construye modelos lineales sobre datos. Las GANs generan nuevas frases a partir de texto existente. Los LLM predicen palabras mediante aprendizaje automático. La respuesta fue extensa, superando las 200 palabras y perdiendo la precisión conceptual (confundió IA generativa con GANs).

#### Prompt 2 – Embeddings

> Describió una búsqueda semántica usando embeddings de Google API para encontrar artículos sobre "redes sociales". Explicó que los embeddings se representan en 100 dimensiones. La respuesta fue funcional pero superficial, sin ejemplo de código.

#### Prompt 3 – Riesgos académicos

> Mencionó tres riesgos: no reconocer la calidad del trabajo del LLM, no entender bien lo que hace un LLM, y no comprender el significado del LLM. **Importante:** el modelo interpretó "LLM" como "Licenciatura en Leyes" (LL.M.) en lugar de Large Language Model, lo que generó una respuesta completamente fuera de contexto.

#### Prompt 4 – ESP32

> Describió el uso de un LLM para aprender lenguajes especializados en la industria automotriz como Python, JavaScript o C++. La respuesta confundió "LLM" (Language Learning Modules) con Large Language Models y el contexto de ESP32 fue muy vago.

**Observación general:** TinyLlama muestra limitaciones evidentes con terminología técnica en español. Confunde siglas y pierde el hilo conceptual en prompts complejos.

---

### 5.2 Phi-4-mini-instruct (`phi4-mini:latest`)

#### Prompt 1 – Conceptual

> Explicó correctamente la jerarquía: IA es el campo general; ML es una subcategoría que aprende con experiencia; la IA generativa crea contenido original; los LLM son una forma especializada de IA generativa para comprender y generar texto. Respuesta dentro del límite de 200 palabras.

#### Prompt 2 – Embeddings

> Propuso un ejemplo con documentos sobre cáncer. Generó embeddings con Word2Vec/GloVe/BERT, calculó distancia euclidiana entre vectores y ordenó documentos por proximidad semántica. Incluyó ejemplo numérico de vectores. Claro y didáctico.

#### Prompt 3 – Riesgos académicos

> Identificó correctamente: (1) Información falsa presentada como factual; (2) sesgos y desigualdad en el contenido generado; (3) plagio no intencional al no reconocer fuentes. Cada riesgo acompañado de un ejemplo pertinente.

#### Prompt 4 – ESP32

> Listó 8 formas de uso: solución de problemas, documentación e investigación, diseño de código, optimización, desarrollo de aplicaciones IoT, integración con bibliotecas FOSS, aprendizaje conceptual y preparación para entrevistas técnicas. Muy completo y relevante.

**Observación general:** Phi-4-mini ofrece respuestas bien estructuradas, coherentes y dentro del formato solicitado. Excelente desempeño para su tamaño (3.8B parámetros).

---

### 5.3 Llama 3.2 3B Instruct (`llama3.2:3b`)

#### Prompt 1 – Conceptual

> Distinguió correctamente los cuatro conceptos: IA como campo general de sistemas autónomos, Aprendizaje Automático como subcampo con algoritmos de datos, IA Generativa enfocada en crear contenido original, y LLM (sin definir el acrónimo explícitamente). Respuesta clara, académica y dentro del límite.

#### Prompt 2 – Embeddings

> Presentó un ejemplo con un repositorio CSV de artículos académicos (cambio climático, salud mental). Incluyó código Python con BertTokenizer y BertModel para generar embeddings y realizar búsqueda por similitud coseno. Respuesta técnica y detallada.

#### Prompt 3 – Riesgos académicos

> Identificó: (1) Falta de precisión y exactitud (ejemplo: fechas incorrectas de la Revolución Francesa); (2) Dependencia excesiva que elimina el pensamiento crítico (ejemplo: economía sin diversidad de perspectivas); (3) Plagio y robo intelectual (ejemplo: tesis doctoral con frases de otros autores sin citar). Ejemplos pertinentes y bien explicados.

#### Prompt 4 – ESP32

> Estructuró el uso del LLM en tres pasos: investigación (preguntas sobre algoritmos de control de temperatura), análisis y optimización, y generación de código fuente en C. Proyecto de ejemplo: control de temperatura con ESP32. Claro y técnicamente orientado.

**Observación general:** Llama 3.2 3B ofrece respuestas estructuradas y técnicamente correctas. Buen balance entre tamaño y calidad de respuesta en español.

---

### 5.4 Gemma 3 4B IT (`gemma3:4b`)

#### Prompt 1 – Conceptual

> Respuesta más concisa y clara de todos los modelos. Definió: IA como objetivo general, AA como subconjunto que aprende de datos, IA Generativa como tipo de AA que crea contenido nuevo, y LLM como tipo específico de IA Generativa entrenado en texto masivo (mencionó ChatGPT como referencia). Perfecta para estudiantes universitarios.

#### Prompt 2 – Embeddings

> Presentó el ejemplo más completo: preparación de datos, creación de embeddings con Sentence Transformers, almacenamiento en base de datos vectorial (Pinecone, Weaviate, FAISS), y búsqueda semántica por distancia coseno. Incluyó código Python funcional y consideraciones sobre escala, actualización y costo.

#### Prompt 3 – Riesgos académicos

> Identificó: (1) Desinformación (ejemplo: texto que argumenta que el mercurio es nutriente); (2) Plagio al presentar texto del LLM como propio sin citar; (3) Dependencia excesiva que reduce el pensamiento crítico (ejemplo: no investigar las causas de la Primera Guerra Mundial por sí mismo). Ejemplos creativos y bien contextualizados.

#### Prompt 4 – ESP32

> Proyecto de ejemplo: control de lámpara inteligente con Google Assistant vía ESP32. Describió cuatro usos del LLM: aclaración conceptual (WebRTC), generación de fragmentos de código C++, debugging (error "connection refused"), y optimización de latencia. Subrayó que el LLM no resuelve solo sino que guía la investigación.

**Observación general:** Gemma 3 4B es el modelo con mejor desempeño general en esta práctica. Respuestas precisas, estructuradas, con excelentes ejemplos y el mejor equilibrio entre concisión y profundidad.

---

### 5.5 Qwen2.5 7B Instruct (`qwen2.5:7b`)

#### Prompt 1 – Conceptual

> Explicó la jerarquía en cuatro puntos numerados: IA como sistemas que imitan funciones humanas, Aprendizaje Automático como algoritmos adaptativos, IA Generativa como sistemas que crean contenido original, y LLM como modelos entrenados con grandes volúmenes de texto para múltiples idiomas. Respuesta correcta y académica.

#### Prompt 2 – Embeddings

> Propuso código Python detallado con BertTokenizer para un repositorio de artículos educativos. Calculó similitud coseno entre embeddings de la consulta y los documentos. Incluyó código C++ funcional para ESP32 con sensor DHT11 y conexión WiFi.

#### Prompt 3 – Riesgos académicos

> Identificó: (1) Plagio potencial (descripción del efecto de luz azul sin citar la fuente); (2) Información inexacta o estadísticas erróneas; (3) Dependencia excesiva que produce análisis sin perspectiva crítica. Respuesta concisa y directa.

#### Prompt 4 – ESP32

> Proyecto: monitoreo de humedad y temperatura con DHT11, conexión WiFi y base de datos remota. Mostró cuatro usos del LLM: generación de código inicial, consultas técnicas, documentación, y aprendizaje continuo. Incluyó código C++ funcional para ESP32.

**Observación general:** Qwen2.5 7B es el modelo más consistente en español gracias a su soporte oficial para más de 29 idiomas. Respuestas detalladas con código técnico pertinente.

---

### 5.6 Mistral 7B Instruct v0.3 (`mistral:7b`)

#### Prompt 1 – Conceptual

> Explicó: IA como rama científica de sistemas inteligentes, AA como subdisciplina donde los sistemas aprenden de la experiencia, IA Generativa como subdisciplina del AA para crear nueva información, y LLM como herramienta de IA Generativa para generar texto coherente en múltiples idiomas. Correcta pero algo genérica.

#### Prompt 2 – Embeddings

> Describió el uso de Word2Vec con Gensim para crear embeddings, almacenarlos en una matriz de 300 dimensiones y realizar búsqueda por vecinos más cercanos (distancia euclidiana). Conceptualmente correcto pero sin código de ejemplo.

#### Prompt 3 – Riesgos académicos

> Identificó: (1) Información incorrecta (capital de Alemania como "París"); (2) Información obsoleta (presidente de EE.UU. desactualizado); (3) Falta de perspectiva cultural (celebración de Navidad solo desde la cultura inglesa). Ejemplos simples pero ilustrativos.

#### Prompt 4 – ESP32

> Describió cuatro usos: documentación automática (Markdown/HTML/PDF desde código), generación de código adicional (GUI, configuración CLI, algoritmos), solución de problemas y optimización, y ayuda en investigación para explorar algoritmos. Respuesta estructurada y práctica.

**Observación general:** Mistral 7B ofrece respuestas correctas y bien organizadas, aunque con menor profundidad que Qwen2.5 o Gemma3. Su desempeño en español es funcional pero no tan fluido como modelos con soporte multilingüe explícito.

---

### 5.7 Qwen3 8B (`qwen3:8b`)

> **Característica destacada:** Qwen3 8B opera en **modo *thinking*** por defecto. Antes de cada respuesta, el modelo genera un bloque interno de razonamiento (`<think>...</think>`) donde planifica su respuesta paso a paso. Este proceso no es visible en el resultado final pero sí fue observable durante la ejecución en Ollama, donde el modelo imprimió su cadena de pensamiento antes de responder.

#### Prompt 1 – Conceptual

> Explicó la jerarquía de forma concisa y precisa: **IA** como campo general que busca imitar funciones cognitivas humanas; **aprendizaje automático (ML)** como subdisciplina que aprende patrones en datos sin programación explícita; **IA generativa** como tipo de IA que crea contenido nuevo (texto, imágenes, música); y **LLM** como subconjunto específico de IA generativa basado en arquitecturas *transformer* para procesar y generar texto. Respuesta dentro del límite de 200 palabras, en español impecable y con estructura lógica clara: IA → ML → IA Generativa → LLM.

#### Prompt 2 – Embeddings

> Presentó el ejemplo más completo y ejecutable de todos los modelos. Usó `sentence-transformers` con el modelo `all-MiniLM-L6-v2` para un repositorio de documentos sobre criptografía cuántica. Incluye código Python funcional en 4 pasos bien diferenciados: (1) preparación de documentos, (2) generación de embeddings, (3) búsqueda semántica con similitud coseno (`util.cos_sim`), y (4) explicación del resultado esperado. También mencionó bases de datos vectoriales (`FAISS`, `Annoy`) para producción. El ejemplo es autocontenido, reproducible y didáctico.

#### Prompt 3 – Riesgos académicos

> Identificó tres riesgos de forma concisa y directa: (1) **Plagio no intencional** — usar un LLM para generar un ensayo sin verificar si el contenido coincide con textos existentes; (2) **Información falsa o sesgada** — citar un estudio inexistente generado por el modelo como fuente confiable; (3) **Falta de rigor metodológico** — desarrollar una teoría académica basándose exclusivamente en la salida del LLM sin contrastar datos o argumentos. Respuesta muy concisa (3 puntos breves) pero completa y bien ejemplificada.

#### Prompt 4 – ESP32

> Proyecto de ejemplo: sistema de monitoreo de temperatura con sensor **DS18B20**, ESP32, Blynk y ThingSpeak. Estructuró el uso del LLM en 4 etapas explícitas: (1) planificación e investigación (bibliotecas `OneWire` y `DallasTemperature`), (2) desarrollo del código (fragmento C++ funcional completo), (3) depuración y optimización (diagnóstico de errores con resistencia pull-up), y (4) documentación y aprendizaje. En cada etapa diferencia claramente la **respuesta del LLM** de la **acción esperada del estudiante**, subrayando que el LLM acelera la investigación pero el estudiante es quien aplica, verifica y reflexiona.

**Observación general:** Qwen3 8B es el modelo de mayor calidad en esta práctica. Su modo *thinking* le permite planificar respuestas antes de generarlas, lo que se traduce en respuestas más estructuradas, código funcional de alta calidad y razonamiento más cuidadoso. En español fue fluido y preciso. La contrapartida es que al incluir el bloque de pensamiento visible en Ollama, la generación total es más lenta que qwen2.5:7b, aunque el resultado final justifica la espera.

---

## 6. Análisis comparativo de respuestas

| Modelo | Calidad en español | Precisión técnica | Longitud/profundidad | Adherencia al formato | Modo *thinking* |
|--------|:------------------:|:-----------------:|:--------------------:|:---------------------:|:---------------:|
| TinyLlama 1.1B | ⭐ Baja | ⭐ Baja | Larga pero imprecisa | ❌ No respetó límite | ❌ |
| Phi-4-mini 3.8B | ⭐⭐⭐⭐ Alta | ⭐⭐⭐⭐ Alta | Adecuada | ✅ Respetó límite | ❌ |
| Llama 3.2 3B | ⭐⭐⭐ Media-alta | ⭐⭐⭐⭐ Alta | Detallada | ✅ Respetó límite | ❌ |
| Gemma 3 4B | ⭐⭐⭐⭐⭐ Muy alta | ⭐⭐⭐⭐⭐ Muy alta | Óptima | ✅ Respetó límite | ❌ |
| Qwen2.5 7B | ⭐⭐⭐⭐⭐ Muy alta | ⭐⭐⭐⭐⭐ Muy alta | Muy detallada | ✅ Respetó límite | ❌ |
| Mistral 7B | ⭐⭐⭐ Media | ⭐⭐⭐ Media | Adecuada | ✅ Respetó límite | ❌ |
| **Qwen3 8B** | ⭐⭐⭐⭐⭐ Muy alta | ⭐⭐⭐⭐⭐ Muy alta | Muy detallada y estructurada | ✅ Respetó límite | ✅ Sí (por defecto) |

---

## 7. Reflexión

### ¿Qué modelo fue más fácil de instalar y ejecutar?

Todos los modelos se instalaron con el mismo flujo usando `ollama pull <modelo>`, lo que demuestra la gran ventaja de Ollama como plataforma unificada. En cuanto a velocidad de ejecución, **TinyLlama 1.1B** fue el más rápido (responde en segundos), seguido de **Phi-4-mini**. Los modelos de 7B (Qwen, Mistral) tardaron considerablemente más en generar respuestas completas, especialmente en equipos sin GPU dedicada.

### ¿Qué modelo respondió mejor en español?

**Gemma 3 4B** y **Qwen2.5 7B** ofrecieron las mejores respuestas en español. Gemma3 por la claridad y coherencia de su redacción; Qwen2.5 por su soporte oficial para más de 29 idiomas y la precisión técnica de sus respuestas. **TinyLlama** fue el de peor desempeño en español, llegando a confundir el significado de siglas académicas.

### ¿Qué diferencia observaste entre un modelo pequeño y uno más grande?

La diferencia es notable en tres dimensiones:

1. **Comprensión contextual:** Los modelos de 7B comprenden mejor instrucciones complejas y restricciones (como "máximo 200 palabras" o "tono académico"). TinyLlama ignora estas restricciones.
2. **Precisión factual:** Modelos más grandes cometen menos errores conceptuales. TinyLlama confundió "LLM" (Large Language Model) con "LL.M." (Licenciatura en Leyes) en el Prompt 3.
3. **Calidad del código generado:** Llama 3.2, Gemma3 y Qwen2.5 generaron ejemplos de código Python/C++ funcionales y bien comentados. TinyLlama no logró generar código útil.

La contrapartida es que los modelos más grandes requieren más RAM, más tiempo de carga y más espacio en disco.

### ¿Qué importancia tiene la licencia del modelo?

La licencia determina qué se puede hacer con el modelo:

- **Apache 2.0** (Qwen2.5, Mistral, TinyLlama): La más permisiva. Permite uso comercial, modificación y distribución sin restricciones mayores, siempre que se mantenga el aviso de copyright.
- **MIT** (Phi-4-mini): Igualmente permisiva. Ideal para proyectos académicos y comerciales sin complicaciones legales.
- **Llama 3.2 Community License** (Meta): Permite uso comercial pero requiere atribución ("Built with Llama") y tiene restricciones si la aplicación supera 700 millones de usuarios activos.
- **Gemma License** (Google): Requiere aceptar términos de uso específicos. Permite uso educativo y de investigación, pero con restricciones comerciales adicionales.

Para uso académico, todas las licencias permiten experimentar libremente. La licencia importa principalmente cuando el trabajo derivado se quiere comercializar o publicar.

### ¿Por qué no debe usarse un LLM como única fuente académica?

Los LLM no son fuentes confiables por sí solos por varias razones:

1. **Alucinaciones:** Los modelos pueden generar información plausible pero incorrecta (fechas, nombres, datos estadísticos, referencias bibliográficas inventadas).
2. **Sin citación:** Los LLM no citan sus fuentes. Esto hace imposible verificar la veracidad de sus afirmaciones.
3. **Corte de conocimiento (*knowledge cutoff*):** Los modelos tienen una fecha límite de entrenamiento y no conocen eventos o publicaciones posteriores.
4. **Sesgos en los datos:** Si el corpus de entrenamiento contiene información sesgada, el modelo la reproducirá.
5. **Falta de profundidad disciplinar:** Un LLM generalista no tiene el rigor de una publicación revisada por pares (*peer-reviewed*).

Los LLM son herramientas útiles para explorar ideas, generar borradores y comprender conceptos, pero cualquier afirmación importante debe verificarse en fuentes primarias (artículos científicos, libros académicos, documentación oficial).

### ¿Qué ventajas y limitaciones tiene ejecutar modelos localmente?

**Ventajas:**
- **Privacidad:** Los datos no salen del equipo; no se envían a servidores externos.
- **Sin costo por uso:** No hay cobro por token ni suscripción mensual.
- **Funcionamiento sin internet:** Una vez descargado, el modelo funciona completamente offline.
- **Control total:** Se puede elegir el modelo, la versión y los parámetros de generación.
- **Experimentación libre:** Se puede probar y comparar múltiples modelos sin restricciones de API.

**Limitaciones:**
- **Requerimientos de hardware:** Los modelos de 7B necesitan al menos 8–16 GB de RAM; sin GPU el rendimiento es lento.
- **Modelos más pequeños:** Los mejores modelos (GPT-4o, Claude, Gemini Ultra) no están disponibles localmente.
- **Instalación y mantenimiento:** Requiere conocimientos técnicos básicos y espacio en disco (los 6 modelos ocupan ~18 GB en total).
- **Velocidad de generación:** Sin GPU dedicada, la generación de texto puede tardar segundos o minutos por respuesta.

---

## 8. Conclusión

Esta práctica permitió comparar de forma directa seis modelos LLM de diferentes fabricantes, tamaños y licencias ejecutados completamente de forma local mediante Ollama. Los resultados demuestran que el tamaño del modelo influye directamente en la calidad de las respuestas en español y en la precisión técnica, aunque modelos compactos como Phi-4-mini ofrecen un excelente desempeño para su tamaño gracias a técnicas avanzadas de entrenamiento. Herramientas como Ollama y Hugging Face democratizan el acceso a estos modelos, permitiendo a estudiantes y desarrolladores experimentar sin depender de APIs comerciales ni conexión a internet.

---

*Práctica desarrollada para el curso de IA Generativa — IBERO. Modelos verificados en Hugging Face. Respuestas generadas localmente con Ollama v0.24.0.*
