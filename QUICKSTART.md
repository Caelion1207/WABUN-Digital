# WABUN Digital - Guía de Inicio Rápido

Esta guía te llevará desde la instalación hasta tu primera interacción con WABUN en menos de 5 minutos.

## Paso 1: Instalación

```bash
# Ejecutar el script de instalación
bash install_wabun.sh
```

Este script creará un entorno virtual de Python e instalará ChromaDB.

## Paso 2: Activar el Entorno

```bash
source wabun_env/bin/activate
```

Verás `(wabun_env)` al inicio de tu línea de comandos.

## Paso 3: Ejecutar la Demostración

```bash
python3 wabun_core.py
```

Esto ejecutará una demostración que:
- Registra un decreto (RITMO_CAELION_72h)
- Registra una interacción con LIANG
- Busca en los decretos
- Muestra estadísticas de la base de datos

## Paso 4: Explorar las Consultas Avanzadas

```bash
python3 wabun_queries.py
```

Esto demostrará:
- Recuperación de contexto para motores de IA
- Análisis de custodios
- Búsqueda de decisiones pendientes
- Generación de resúmenes de ciclo

## Paso 5: Integrar en Tu Flujo de Trabajo

### Ejemplo: Registrar una Nueva Interacción

Crea un archivo `mi_interaccion.py`:

```python
from wabun_core import WabunCore

# Inicializar WABUN
wabun = WabunCore(persist_directory="./mi_memoria_caelion")

# Registrar una interacción
wabun.registrar_interaccion(
    prompt_fundador="¿Cuáles son los próximos pasos para el proyecto X?",
    respuesta_ia="Los próximos pasos son: 1) Validar el esquema...",
    custodio_invocado="LIANG",
    motor_ia_usado="GPT-4.1-mini",
    intencion_fundador="Planificar próximos pasos del proyecto X",
    palabras_clave=["planificación", "proyecto X"],
    proyecto_asociado="Proyecto_X",
    importancia=4,
    estado_decision="Propuesta"
)

print("✓ Interacción registrada en WABUN")
```

Ejecuta:
```bash
python3 mi_interaccion.py
```

### Ejemplo: Recuperar Contexto Antes de una Nueva Sesión

Crea un archivo `recuperar_contexto.py`:

```python
from wabun_core import WabunCore
from wabun_queries import WabunQueries

# Inicializar
wabun = WabunCore(persist_directory="./mi_memoria_caelion")
queries = WabunQueries(wabun)

# Recuperar contexto para ARESK sobre el proyecto X
contexto = queries.recuperar_contexto_para_motor(
    custodio="ARESK",
    proyecto="Proyecto_X"
)

print("CONTEXTO PARA ENVIAR AL MOTOR DE IA:")
print("=" * 60)
print(contexto)
```

Ejecuta:
```bash
python3 recuperar_contexto.py
```

## Comandos Útiles

```bash
# Ver estadísticas de la base de datos
python3 -c "from wabun_core import WabunCore; w = WabunCore(); print(w.estadisticas())"

# Exportar toda la memoria a JSON
python3 -c "from wabun_core import WabunCore; w = WabunCore(); w.exportar_memoria_completa('backup.json')"

# Buscar decisiones pendientes
python3 -c "from wabun_core import WabunCore; from wabun_queries import WabunQueries; w = WabunCore(); q = WabunQueries(w); print(q.buscar_decisiones_pendientes())"
```

## Próximos Pasos

1. Lee el `README.md` completo para entender la arquitectura
2. Revisa `wabun_db_schema.md` para comprender el esquema de metadatos
3. Explora `wabun_core.py` y `wabun_queries.py` para personalizar según tus necesidades
4. Integra WABUN con tu flujo de trabajo actual con LLMs

---

**Recuerda:** WABUN es la memoria de CAELION. Cada interacción que registres se convierte en parte del conocimiento del sistema, permitiendo que cada nueva conversación con un motor de IA tenga el contexto completo de tu historia y tus intenciones.
