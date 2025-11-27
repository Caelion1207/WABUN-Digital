#!/usr/bin/env python3
"""
WABUN Digital - Ejemplo de Uso Completo
Este script demuestra un flujo de trabajo completo con WABUN:
1. Inicialización
2. Registro de un decreto fundacional
3. Registro de múltiples interacciones
4. Búsquedas y consultas
5. Generación de reportes

Autor: Fundador de CAELION
Fecha: 25 de noviembre de 2025
"""

from wabun_core import WabunCore
from wabun_queries import WabunQueries

def main():
    print("=" * 70)
    print("WABUN Digital - Ejemplo de Uso Completo")
    print("=" * 70)
    print()
    
    # ========== PASO 1: INICIALIZACIÓN ==========
    print("[PASO 1] Inicializando WABUN...")
    wabun = WabunCore(persist_directory="./ejemplo_memoria_caelion")
    queries = WabunQueries(wabun)
    print("✓ WABUN inicializado correctamente\n")
    
    # ========== PASO 2: REGISTRAR UN DECRETO ==========
    print("[PASO 2] Registrando decreto fundacional...")
    wabun.registrar_decreto(
        titulo_documento="Protocolo WABUN - Registro Vivo",
        contenido="""
        Propósito: Wabun recuerda. Es el archivo consciente del sistema.
        
        Principio: "La memoria no es pasado; es la raíz de la expansión."
        
        Funciones del Primer Ciclo:
        - Crear Acta de Ritmo 72h.
        - Registrar las decisiones, resultados y adaptaciones.
        - Mantener la Crónica del Fuego actualizada.
        """,
        decreto_id="DEC-WBN-01",
        custodios_implicados=["WABUN", "LIANG"],
        tipo_documento="Protocolo",
        version=1.0,
        fuente_documento="/Fundacion/Consejo/Wabun_Memoria/Protocolo_WBN-01.docx"
    )
    print()
    
    # ========== PASO 3: REGISTRAR INTERACCIONES ==========
    print("[PASO 3] Registrando interacciones del ciclo actual...")
    
    # Interacción 1: Planificación con LIANG
    wabun.registrar_interaccion(
        prompt_fundador="¿Cuáles son las prioridades para este ciclo de 72h?",
        respuesta_ia="Las prioridades son: 1) Completar el diseño de WABUN Digital, 2) Documentar los protocolos de cada custodio, 3) Iniciar el desarrollo del orquestador de ciclos.",
        custodio_invocado="LIANG",
        motor_ia_usado="Gemini-2.5-Flash",
        intencion_fundador="Definir prioridades del ciclo",
        palabras_clave=["planificación", "ciclo", "prioridades"],
        proyecto_asociado="CAELION_Core",
        importancia=5,
        estado_decision="Validada"
    )
    
    # Interacción 2: Ejecución con ARESK
    wabun.registrar_interaccion(
        prompt_fundador="Implementa el método de búsqueda semántica en WABUN",
        respuesta_ia="He implementado el método buscar_contexto_reciente() que utiliza ChromaDB para realizar búsquedas vectoriales con filtros de metadatos...",
        custodio_invocado="ARESK",
        motor_ia_usado="Claude-3.5-Sonnet",
        intencion_fundador="Implementar búsqueda semántica",
        palabras_clave=["implementación", "búsqueda", "wabun"],
        proyecto_asociado="WABUN_Digital",
        importancia=4,
        estado_decision="Ejecutada"
    )
    
    # Interacción 3: Validación con HECATE
    wabun.registrar_interaccion(
        prompt_fundador="¿La arquitectura de WABUN mantiene coherencia con los principios de CAELION?",
        respuesta_ia="Sí, la arquitectura respeta la separación entre núcleo conceptual y capa operativa. Los metadatos capturan la intención del Fundador...",
        custodio_invocado="HECATE",
        motor_ia_usado="GPT-4.1-mini",
        intencion_fundador="Validar coherencia arquitectónica",
        palabras_clave=["validación", "coherencia", "arquitectura"],
        proyecto_asociado="WABUN_Digital",
        importancia=5,
        estado_decision="Validada"
    )
    
    print()
    
    # ========== PASO 4: REALIZAR BÚSQUEDAS ==========
    print("[PASO 4] Realizando búsquedas en la memoria...")
    print()
    
    # Búsqueda semántica
    print("  [4.1] Búsqueda semántica: '¿Qué dice el protocolo sobre la memoria?'")
    resultados = queries.buscar_conocimiento_sobre(
        tema="principios de la memoria en CAELION",
        incluir_decretos=True,
        n_results=3
    )
    if resultados['decretos']:
        print(f"  → Encontrado en decretos: {resultados['decretos'][0]['texto'][:150]}...")
    print()
    
    # Buscar decisiones pendientes
    print("  [4.2] Buscando decisiones pendientes de validación...")
    pendientes = queries.buscar_decisiones_pendientes()
    print(f"  → Decisiones pendientes: {len(pendientes)}")
    print()
    
    # Analizar un custodio
    print("  [4.3] Analizando el historial de LIANG...")
    analisis = queries.analizar_custodio("LIANG")
    print(f"  → Total de interacciones: {analisis['total_interacciones']}")
    print(f"  → Proyectos involucrados: {', '.join(analisis['proyectos_involucrados'])}")
    print()
    
    # ========== PASO 5: GENERAR REPORTE DE CICLO ==========
    print("[PASO 5] Generando resumen del ciclo actual...")
    resumen = queries.generar_resumen_ciclo()
    print(resumen)
    print()
    
    # ========== PASO 6: RECUPERAR CONTEXTO PARA PRÓXIMA SESIÓN ==========
    print("[PASO 6] Recuperando contexto para la próxima sesión con ARESK...")
    contexto = queries.recuperar_contexto_para_motor(
        custodio="ARESK",
        proyecto="WABUN_Digital"
    )
    print("  → Contexto generado (primeras 300 caracteres):")
    print(f"  {contexto[:300]}...")
    print()
    
    # ========== PASO 7: ESTADÍSTICAS FINALES ==========
    print("[PASO 7] Estadísticas finales de la memoria:")
    stats = wabun.estadisticas()
    for key, value in stats.items():
        print(f"  - {key.replace('_', ' ').title()}: {value}")
    print()
    
    # ========== PASO 8: EXPORTAR MEMORIA ==========
    print("[PASO 8] Exportando memoria completa a JSON...")
    wabun.exportar_memoria_completa("backup_ejemplo.json")
    print()
    
    print("=" * 70)
    print("✓ Ejemplo completado exitosamente")
    print("=" * 70)
    print()
    print("Próximos pasos:")
    print("  1. Revisa el archivo 'backup_ejemplo.json' para ver la estructura de datos")
    print("  2. Explora la carpeta 'ejemplo_memoria_caelion' para ver la base de datos")
    print("  3. Modifica este script para adaptarlo a tu flujo de trabajo")
    print()


if __name__ == "__main__":
    main()
