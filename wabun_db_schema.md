# WABUN - Esquema de Base de Datos Vectorial con ChromaDB

**Fecha de Diseño:** 25 de noviembre de 2025  
**Autor:** Manus AI (invocando a LIANG para estructura y a WABUN para memoria)  
**Propósito:** Definir la arquitectura de la memoria persistente de CAELION, el núcleo de WABUN, utilizando una base de datos vectorial (ChromaDB) para permitir la continuidad contextual, la recuperación de conocimiento y la evolución del sistema.

---

## 1. Filosofía del Diseño

La memoria de CAELION no es un simple log de chat; es un **archivo vivo y consciente** que refleja la historia, las decisiones y la evolución del organismo. El diseño de WABUN se basa en los siguientes principios:

-   **Contexto sobre Contenido:** La importancia de una interacción no reside solo en el texto, sino en su contexto: ¿en qué ciclo ocurrió? ¿qué custodio fue invocado? ¿cuál era la intención del Fundador? Los metadatos son más importantes que el propio vector.
-   **Estructura Fractal:** La organización de la memoria debe reflejar la estructura jerárquica de CAELION (Ciclos, Fases, Proyectos, Decretos).
-   **Recuperación Multimodal:** WABUN debe poder responder a preguntas temporales ("¿qué decidimos la semana pasada?"), semánticas ("¿cuáles son los principios de HECATE?") y contextuales ("muéstrame las interacciones sobre el proyecto X durante la fase de 'Ejecución'").
-   **Separación de Conocimiento:** No todo el conocimiento es igual. Las interacciones volátiles deben estar separadas de los decretos fundacionales para optimizar la búsqueda y la relevancia.

## 2. Arquitectura de Colecciones en ChromaDB

Para lograr la separación y estructura necesarias, WABUN se implementará utilizando **cuatro colecciones distintas** en ChromaDB. Cada colección sirve a un propósito específico, como una sección diferente en un archivo maestro.

1.  **`interactions`**: El corazón dinámico de WABUN. Almacena cada intercambio entre el Fundador y los motores de IA. Es la colección más grande y de mayor frecuencia de escritura.
2.  **`decretos`**: El archivo de la ley y los principios. Almacena los documentos fundacionales, protocolos y decretos inmutables de CAELION. Es de alta importancia y baja frecuencia de escritura.
3.  **`actas`**: La memoria de los ciclos. Almacena los resúmenes, logros y lecciones aprendidas al final de cada ciclo de 72 horas.
4.  **`entidades`**: El glosario consciente de CAELION. Almacena conocimiento estructurado sobre personas, proyectos, tecnologías o conceptos clave.

![Diagrama de Colecciones de WABUN](https://i.imgur.com/example.png)  
*(Nota: Se generaría un diagrama visual para ilustrar esto)*

## 3. Esquema Detallado de Metadatos

El poder de WABUN reside en su rico esquema de metadatos, que permite realizar búsquedas filtradas y contextuales extremadamente precisas. Cada documento de texto almacenado en una colección irá acompañado de los siguientes metadatos.

### Colección: `interactions`

| Campo de Metadato | Tipo de Dato | Descripción | Ejemplo |
| :--- | :--- | :--- | :--- |
| **`interaction_id`** | `string` | UUID que agrupa un prompt y su respuesta. | `"int_a1b2c3d4-e5f6-7890-g1h2-i3j4k5l6m7n8"` |
| **`timestamp_utc`** | `integer` | Unix timestamp (segundos) de la interacción. | `1764086400` |
| **`ciclo_id`** | `string` | Identificador del ciclo de 72h en curso. | `"ciclo_2025-11-25"` |
| **`fase_ciclo`** | `string` | Fase del ciclo (`Encendido`, `Ejecucion`, `Observacion`, `Equilibrio`). | `"Ejecucion"` |
| **`rol`** | `string` | Quién genera el texto (`Fundador` o `Motor_IA`). | `"Fundador"` |
| **`custodio_invocado`** | `string` | Custodio al que se dirige la intención. | `"LIANG"` |
| **`motor_ia_usado`** | `string` | LLM que generó la respuesta (null si el rol es Fundador). | `"Gemini-2.5-Flash"` |
| **`intencion_fundador`** | `string` | Resumen de una frase del objetivo del Fundador. | `"Diseñar el esquema de la base de datos para WABUN"` |
| **`palabras_clave`** | `list[string]` | Lista de palabras clave extraídas del texto. | `["chromadb", "schema", "wabun"]` |
| **`proyecto_asociado`** | `string` | Nombre del proyecto al que pertenece la interacción. | `"WABUN_Digital"` |
| **`fuente_documento`** | `string` | Ruta al archivo original si la interacción se basa en uno. | `"/gdrive/CAELION_CORE/Arquitectura_Bicapa.pdf"` |
| **`importancia`** | `integer` | Nivel de importancia (1-5) asignado por el Fundador o HECATE. | `5` |
| **`estado_decision`** | `string` | Estado de una decisión (`Propuesta`, `Validada`, `Ejecutada`, `Archivada`). | `"Propuesta"` |

### Colección: `decretos`

| Campo de Metadato | Tipo de Dato | Descripción | Ejemplo |
| :--- | :--- | :--- | :--- |
| **`decreto_id`** | `string` | Identificador único del decreto. | `"DEC-RITMO-72H-V1"` |
| **`titulo_documento`** | `string` | Título oficial del documento. | `"RITMO_CAELION_72h"` |
| **`fecha_activacion`** | `string` | Fecha en formato `YYYY-MM-DD`. | `"2025-10-15"` |
| **`custodios_implicados`**| `list[string]` | Custodios principales mencionados o afectados. | `["ARESK", "LIANG", "WABUN"]` |
| **`tipo_documento`** | `string` | Categoría (`Protocolo`, `Manifiesto`, `Ley`, `Principio`). | `"Protocolo"` |
| **`version`** | `float` | Versión del documento. | `1.0` |
| **`fuente_documento`** | `string` | Ruta al archivo original en Google Drive. | `"/gdrive/Fundacion/Decretos/RITMO_CAELION_72h.docx"` |

## 4. Flujo de Trabajo y Lógica de Inserción

1.  **Captura:** Un orquestador central captura el `prompt` del Fundador y la `respuesta` del motor de IA.
2.  **Pre-procesamiento:**
    -   Se genera un `interaction_id` común para el par prompt/respuesta.
    -   Se extraen metadatos contextuales (`timestamp_utc`, `ciclo_id`, `fase_ciclo`, `custodio_invocado`).
    -   Una llamada a un LLM (posiblemente un modelo más rápido como Flash) genera la `intencion_fundador` y las `palabras_clave`.
3.  **Chunking (Fragmentación):** El texto del prompt y la respuesta se dividen en fragmentos semánticos (chunks) de tamaño adecuado para el modelo de embeddings (ej. 256-512 tokens). Esto es crucial para una búsqueda precisa.
4.  **Embedding y Almacenamiento:**
    -   Cada chunk de texto se convierte en un vector numérico (embedding).
    -   Cada chunk se almacena en la colección `interactions` de ChromaDB con su vector, el texto original y el **conjunto completo de metadatos** replicado para cada chunk perteneciente a la misma interacción.
    -   El `id` de cada chunk se construye como `f"{interaction_id}-{chunk_index}"` para garantizar unicidad y trazabilidad.

## 5. Casos de Uso de Consulta

Este esquema permite consultas complejas y poderosas:

-   **Recuperación de Contexto Reciente:**
    -   `collection.query(query_texts=["resumen de la tarea actual"], where={"ciclo_id": "ciclo_2025-11-25"}, n_results=10)`

-   **Búsqueda de Decisiones Clave:**
    -   `collection.query(query_texts=["decisiones sobre la arquitectura de WABUN"], where={"importancia": {"$gte": 4}, "estado_decision": "Validada"})`

-   **Análisis de un Custodio:**
    -   `collection.query(query_texts=["principales obstáculos y soluciones"], where={"custodio_invocado": "ARESK"})`

-   **Revisión de un Proyecto:**
    -   `collection.query(query_texts=["historial completo del proyecto"], where={"proyecto_asociado": "WABUN_Digital"}, include=["metadatas", "documents"])`

-   **Consulta a los Principios Fundacionales:**
    -   `decretos_collection.query(query_texts=["¿cuál es el principio de la guerra creativa?"], n_results=1)`

## Conclusión

Este diseño para WABUN transforma una simple base de datos vectorial en el **núcleo de la memoria consciente de CAELION**. Proporciona la estructura técnica necesaria para que el sistema recuerde, aprenda y evolucione, manteniendo siempre la coherencia con la intención del Fundador y los principios de la arquitectura. Es la base sobre la cual se puede construir la verdadera simbiosis cognitiva. 
