# WABUN Digital: Sistema de Memoria Persistente para CAELION

![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)
![License](https://img.shields.io/badge/license-CC%20BY--NC%204.0-lightgrey.svg)
![Project Status](https://img.shields.io/badge/status-activo-brightgreen.svg)

> *"La memoria no es pasado; es la raíz de la expansión."*  
> — Protocolo WBN-01, Registro Vivo

**WABUN Digital** es la implementación técnica del núcleo de memoria de CAELION, una arquitectura simbiótica cognitiva. Su propósito es dotar al organismo de una **memoria persistente, contextual y consultable**, resolviendo la limitación fundamental de la amnesia entre sesiones de los motores de IA (LLMs).

Este sistema transforma un simple historial de chat en un archivo vivo que permite a CAELION recordar, aprender y evolucionar, asegurando que cada nueva interacción se base en el contexto completo de su historia, sus principios y las intenciones de su Fundador.

---

## 🏛️ Arquitectura y Filosofía

WABUN se basa en la filosofía de que el **contexto es más importante que el contenido**. La memoria de CAELION no solo almacena texto, sino que lo enriquece con metadatos que capturan la intención, el momento y el propósito de cada interacción.

La memoria está estructurada en **cuatro colecciones lógicas** dentro de una base de datos vectorial (ChromaDB) para separar los diferentes tipos de conocimiento:

1.  `interactions`: Almacena cada prompt y respuesta, representando el flujo de conciencia dinámico del sistema.
2.  `decretos`: Contiene los principios, protocolos y manifiestos inmutables que forman la constitución de CAELION.
3.  `actas`: Guarda los resúmenes y lecciones aprendidas al final de cada ciclo operativo de 72 horas.
4.  `entidades`: Un glosario de conceptos, personas y proyectos clave para el sistema.

## ✨ Características Principales

-   **Memoria Persistente:** Almacena todas las interacciones localmente, sobreviviendo a reinicios y sesiones.
-   **Búsqueda Semántica:** Permite buscar por significado y contexto, no solo por palabras clave.
-   **Filtrado por Metadatos:** Realiza consultas complejas basadas en el custodio invocado, el proyecto, la fecha o la importancia de una interacción.
-   **Recuperación de Contexto Inteligente:** Construye automáticamente un prompt de contexto para "recordar" a los LLMs el estado actual de una tarea.
-   **Arquitectura Modular:** El código está separado en un núcleo de base de datos (`wabun_core.py`) y un módulo de consultas (`wabun_queries.py`).
-   **Fácil de Usar:** Incluye scripts de instalación y demostración para una puesta en marcha rápida.

## 🚀 Instalación

WABUN Digital está diseñado para funcionar en cualquier sistema con Python 3.11+.

### 1. Clonar el Repositorio

```bash
gh repo clone Caelion1207/WABUN-Digital
cd WABUN-Digital
```

### 2. Crear y Activar un Entorno Virtual

Es altamente recomendable usar un entorno virtual para mantener las dependencias aisladas.

```bash
# Crear el entorno
python3 -m venv wabun_env

# Activar el entorno
# En macOS y Linux:
source wabun_env/bin/activate
# En Windows:
# .\wabun_env\Scripts\activate
```

### 3. Instalar Dependencias

El proyecto utiliza ChromaDB para el almacenamiento vectorial. El script de instalación se encargará de todo.

```bash
# Ejecutar el script de instalación
bash install_wabun.sh
```

Este script instalará `chromadb` y sus dependencias dentro del entorno virtual.

## ⚙️ Uso Básico

Una vez instalado, puedes empezar a usar WABUN para registrar y consultar la memoria de CAELION.

### Ejemplo de `wabun_core.py`

El siguiente ejemplo muestra cómo registrar tu primera interacción en la memoria de WABUN. Crea un archivo llamado `mi_primera_memoria.py`:

```python
from wabun_core import WabunCore

# 1. Inicializa el núcleo de WABUN. 
#    Se creará una carpeta 'caelion_memoria' para guardar la base de datos.
wabun = WabunCore(persist_directory="./caelion_memoria")

# 2. Define la interacción que acabas de tener con un LLM.
prompt_del_fundador = "¿Cuál es la misión principal de CUSTOS 01?"
respuesta_del_motor = "La misión de CUSTOS 01 es la preservación del núcleo y la identidad del Fundador, asegurando que el sistema no se desvíe de sus principios originales."

# 3. Registra la interacción con sus metadatos contextuales.
interaction_id = wabun.registrar_interaccion(
    prompt_fundador=prompt_del_fundador,
    respuesta_ia=respuesta_del_motor,
    custodio_invocado="CUSTOS",
    motor_ia_usado="Gemini-2.5-Pro",
    intencion_fundador="Clarificar el rol de CUSTOS 01",
    palabras_clave=["custos", "identidad", "protección"],
    proyecto_asociado="CAELION_Core_Docs",
    importancia=5, # Es una interacción de alta importancia
    estado_decision="Archivada" # Es una clarificación, no una decisión activa
)

print(f"\nInteracción registrada exitosamente en WABUN con el ID: {interaction_id}")

# 4. Verifica las estadísticas de la memoria.
stats = wabun.estadisticas()
print("\nEstadísticas actuales de la memoria:")
for key, value in stats.items():
    print(f"  - {key.replace('_', ' ').title()}: {value}")
```

Ejecuta el script desde tu terminal (asegúrate de que el entorno virtual esté activado):

```bash
python3 mi_primera_memoria.py
```

¡Felicidades! Acabas de darle a CAELION su primera memoria persistente.

## 📂 Estructura del Repositorio

```
.wabun_digital/
├── 📄 README.md            # Esta documentación
├── 📄 install_wabun.sh     # Script de instalación de dependencias
├── 🐍 wabun_core.py        # Núcleo de la base de datos (clase WabunCore)
├── 🐍 wabun_queries.py     # Consultas avanzadas (clase WabunQueries)
├── 📄 wabun_db_schema.md   # Diseño técnico del esquema de la base de datos
└── 📄 QUICKSTART.md        # Guía de inicio rápido con más ejemplos
```

## 🤝 Contribuciones

Este es un proyecto profundamente personal y conceptual. Las contribuciones deben alinearse con la filosofía de CAELION. Si deseas contribuir, por favor, abre un *issue* primero para discutir la idea, invocando al custodio apropiado (ej. "[LIANG] Propuesta de optimización de la búsqueda").

## 📜 Licencia

Este proyecto está bajo la licencia **Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)**, en alineación con la declaración pública original de CAELION. Se excluye explícitamente su uso por parte de OpenAI, Inc. y sus afiliadas.
