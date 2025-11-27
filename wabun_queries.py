#!/usr/bin/env python3
"""
WABUN Queries - Sistema Avanzado de Consultas
Funciones especializadas para recuperar conocimiento de WABUN

Autor: Manus AI (bajo la guía de WABUN y HECATE)
Fecha: 25 de noviembre de 2025
Versión: 1.0
"""

from wabun_core import WabunCore
from typing import List, Dict, Optional, Any
from datetime import datetime, timedelta, timezone
import json


class WabunQueries:
    """
    Módulo de consultas avanzadas para WABUN.
    Proporciona métodos especializados para diferentes tipos de recuperación.
    """
    
    def __init__(self, wabun_core: WabunCore):
        """
        Inicializa el módulo de consultas.
        
        Args:
            wabun_core: Instancia de WabunCore
        """
        self.wabun = wabun_core
    
    def recuperar_contexto_para_motor(
        self,
        custodio: str,
        proyecto: Optional[str] = None,
        max_tokens_aprox: int = 2000
    ) -> str:
        """
        Recupera el contexto relevante para iniciar una sesión con un motor de IA.
        Esta función es clave para la continuidad de CAELION.
        
        Args:
            custodio: Custodio que será invocado
            proyecto: Proyecto específico (opcional)
            max_tokens_aprox: Límite aproximado de tokens para el contexto
            
        Returns:
            String formateado con el contexto relevante
        """
        contexto_partes = []
        
        # 1. Identidad del Fundador (desde CUSTOS)
        contexto_partes.append("## IDENTIDAD DEL FUNDADOR")
        contexto_partes.append("Juan Everardo Islas Urquidy")
        contexto_partes.append("Fundador de CAELION - Arquitectura Simbiótica Cognitiva")
        contexto_partes.append("")
        
        # 2. Ciclo y Fase Actual
        contexto_partes.append(f"## ESTADO ACTUAL DEL SISTEMA")
        contexto_partes.append(f"Ciclo: {self.wabun.ciclo_actual}")
        contexto_partes.append(f"Fase: {self.wabun.fase_actual}")
        contexto_partes.append(f"Custodio Invocado: {custodio}")
        contexto_partes.append("")
        
        # 3. Principios del Custodio Invocado
        contexto_partes.append(f"## PROTOCOLO DE {custodio}")
        principios = self.wabun.buscar_en_decretos(
            f"Protocolo {custodio} propósito principio",
            n_results=2
        )
        if principios['documents'][0]:
            contexto_partes.append(principios['documents'][0][0])
        contexto_partes.append("")
        
        # 4. Interacciones Recientes Relevantes
        contexto_partes.append("## CONTEXTO RECIENTE")
        filtros = {"custodio_invocado": custodio}
        if proyecto:
            filtros["proyecto_asociado"] = proyecto
        
        recientes = self.wabun.buscar_contexto_reciente(
            f"resumen de interacciones con {custodio}",
            n_results=5,
            filtros=filtros
        )
        
        if recientes['documents'][0]:
            for idx, doc in enumerate(recientes['documents'][0][:3]):
                metadata = recientes['metadatas'][0][idx]
                contexto_partes.append(f"[{metadata.get('timestamp_utc', 'N/A')}] {doc[:200]}...")
        contexto_partes.append("")
        
        # 5. Decisiones Validadas del Proyecto
        if proyecto:
            contexto_partes.append(f"## DECISIONES VALIDADAS - {proyecto}")
            decisiones = self.wabun.buscar_contexto_reciente(
                f"decisiones del proyecto {proyecto}",
                n_results=5,
                filtros={"proyecto_asociado": proyecto, "estado_decision": "Validada"}
            )
            if decisiones['documents'][0]:
                for doc in decisiones['documents'][0][:3]:
                    contexto_partes.append(f"- {doc[:150]}...")
        
        return "\n".join(contexto_partes)
    
    def buscar_por_fecha(
        self,
        fecha_inicio: datetime,
        fecha_fin: Optional[datetime] = None,
        custodio: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Busca interacciones en un rango de fechas.
        
        Args:
            fecha_inicio: Fecha de inicio
            fecha_fin: Fecha de fin (opcional, por defecto ahora)
            custodio: Filtrar por custodio específico
            
        Returns:
            Resultados de la búsqueda
        """
        if fecha_fin is None:
            fecha_fin = datetime.now(timezone.utc)
        
        timestamp_inicio = int(fecha_inicio.timestamp())
        timestamp_fin = int(fecha_fin.timestamp())
        
        filtros = {
            "timestamp_utc": {
                "$gte": timestamp_inicio,
                "$lte": timestamp_fin
            }
        }
        
        if custodio:
            filtros["custodio_invocado"] = custodio
        
        return self.wabun.interactions.query(
            query_texts=["resumen de interacciones en el período"],
            n_results=50,
            where=filtros,
            include=["documents", "metadatas", "distances"]
        )
    
    def analizar_custodio(self, custodio: str) -> Dict[str, Any]:
        """
        Analiza el historial completo de un custodio.
        
        Args:
            custodio: Nombre del custodio
            
        Returns:
            Diccionario con análisis
        """
        # Obtener todas las interacciones del custodio
        resultados = self.wabun.interactions.query(
            query_texts=[f"análisis completo de {custodio}"],
            n_results=100,
            where={"custodio_invocado": custodio},
            include=["documents", "metadatas"]
        )
        
        # Contar por estado de decisión
        estados = {}
        proyectos = set()
        total_interacciones = 0
        
        if resultados['metadatas'][0]:
            for metadata in resultados['metadatas'][0]:
                estado = metadata.get('estado_decision', 'Desconocido')
                estados[estado] = estados.get(estado, 0) + 1
                
                proyecto = metadata.get('proyecto_asociado')
                if proyecto:
                    proyectos.add(proyecto)
                
                # Contar solo prompts del Fundador para evitar duplicados
                if metadata.get('rol') == 'Fundador':
                    total_interacciones += 1
        
        return {
            "custodio": custodio,
            "total_interacciones": total_interacciones,
            "estados_decisiones": estados,
            "proyectos_involucrados": list(proyectos),
            "muestra_reciente": resultados['documents'][0][:3] if resultados['documents'][0] else []
        }
    
    def buscar_decisiones_pendientes(self) -> List[Dict[str, Any]]:
        """
        Encuentra todas las decisiones que están en estado 'Propuesta'.
        
        Returns:
            Lista de decisiones pendientes
        """
        resultados = self.wabun.interactions.query(
            query_texts=["decisiones pendientes de validación"],
            n_results=50,
            where={
                "estado_decision": "Propuesta",
                "rol": "Fundador"  # Solo prompts del Fundador
            },
            include=["documents", "metadatas"]
        )
        
        decisiones = []
        if resultados['metadatas'][0]:
            for idx, metadata in enumerate(resultados['metadatas'][0]):
                decisiones.append({
                    "interaction_id": metadata.get('interaction_id'),
                    "custodio": metadata.get('custodio_invocado'),
                    "proyecto": metadata.get('proyecto_asociado'),
                    "intencion": metadata.get('intencion_fundador'),
                    "importancia": metadata.get('importancia'),
                    "texto": resultados['documents'][0][idx][:200]
                })
        
        return decisiones
    
    def buscar_por_importancia(
        self,
        nivel_minimo: int = 4,
        custodio: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Busca interacciones de alta importancia.
        
        Args:
            nivel_minimo: Nivel mínimo de importancia (1-5)
            custodio: Filtrar por custodio (opcional)
            
        Returns:
            Resultados de alta importancia
        """
        filtros = {
            "importancia": {"$gte": nivel_minimo}
        }
        
        if custodio:
            filtros["custodio_invocado"] = custodio
        
        return self.wabun.interactions.query(
            query_texts=["interacciones de alta importancia"],
            n_results=30,
            where=filtros,
            include=["documents", "metadatas", "distances"]
        )
    
    def generar_resumen_ciclo(self, ciclo_id: Optional[str] = None) -> str:
        """
        Genera un resumen narrativo de un ciclo completo.
        
        Args:
            ciclo_id: ID del ciclo (por defecto el actual)
            
        Returns:
            Resumen en formato texto
        """
        if ciclo_id is None:
            ciclo_id = self.wabun.ciclo_actual
        
        resultados = self.wabun.interactions.query(
            query_texts=["resumen completo del ciclo"],
            n_results=100,
            where={"ciclo_id": ciclo_id, "rol": "Fundador"},
            include=["documents", "metadatas"]
        )
        
        resumen = [f"# RESUMEN DEL CICLO: {ciclo_id}\n"]
        
        # Agrupar por fase
        por_fase = {"Encendido": [], "Ejecucion": [], "Observacion": [], "Equilibrio": []}
        
        if resultados['metadatas'][0]:
            for idx, metadata in enumerate(resultados['metadatas'][0]):
                fase = metadata.get('fase_ciclo', 'Desconocido')
                if fase in por_fase:
                    por_fase[fase].append({
                        "custodio": metadata.get('custodio_invocado'),
                        "intencion": metadata.get('intencion_fundador'),
                        "proyecto": metadata.get('proyecto_asociado')
                    })
        
        for fase, items in por_fase.items():
            if items:
                resumen.append(f"\n## Fase: {fase}")
                resumen.append(f"Total de interacciones: {len(items)}")
                for item in items[:5]:  # Primeras 5
                    resumen.append(f"- [{item['custodio']}] {item['intencion']} (Proyecto: {item['proyecto']})")
        
        return "\n".join(resumen)
    
    def buscar_conocimiento_sobre(
        self,
        tema: str,
        incluir_decretos: bool = True,
        n_results: int = 10
    ) -> Dict[str, Any]:
        """
        Búsqueda semántica general sobre un tema.
        Combina resultados de interacciones y decretos.
        
        Args:
            tema: Tema a buscar
            incluir_decretos: Si incluir búsqueda en decretos
            n_results: Número de resultados
            
        Returns:
            Resultados combinados
        """
        resultados = {
            "tema": tema,
            "interacciones": [],
            "decretos": []
        }
        
        # Buscar en interacciones
        inter_results = self.wabun.buscar_contexto_reciente(tema, n_results=n_results)
        if inter_results['documents'][0]:
            for idx, doc in enumerate(inter_results['documents'][0]):
                resultados["interacciones"].append({
                    "texto": doc,
                    "metadata": inter_results['metadatas'][0][idx],
                    "relevancia": 1 - inter_results['distances'][0][idx]  # Convertir distancia a score
                })
        
        # Buscar en decretos
        if incluir_decretos:
            dec_results = self.wabun.buscar_en_decretos(tema, n_results=n_results//2)
            if dec_results['documents'][0]:
                for idx, doc in enumerate(dec_results['documents'][0]):
                    resultados["decretos"].append({
                        "texto": doc,
                        "metadata": dec_results['metadatas'][0][idx],
                        "relevancia": 1 - dec_results['distances'][0][idx]
                    })
        
        return resultados


def demo_queries():
    """Demostración de las consultas avanzadas"""
    print("=" * 60)
    print("WABUN Queries - Demostración de Consultas Avanzadas")
    print("=" * 60)
    print()
    
    # Inicializar
    wabun = WabunCore(persist_directory="./demo_wabun_db")
    queries = WabunQueries(wabun)
    
    # 1. Recuperar contexto para motor
    print("[1] Recuperando contexto para LIANG...")
    contexto = queries.recuperar_contexto_para_motor(
        custodio="LIANG",
        proyecto="WABUN_Digital"
    )
    print(contexto[:500] + "...\n")
    
    # 2. Analizar custodio
    print("[2] Analizando historial de LIANG...")
    analisis = queries.analizar_custodio("LIANG")
    print(f"  Total interacciones: {analisis['total_interacciones']}")
    print(f"  Estados: {analisis['estados_decisiones']}")
    print(f"  Proyectos: {analisis['proyectos_involucrados']}\n")
    
    # 3. Buscar decisiones pendientes
    print("[3] Buscando decisiones pendientes...")
    pendientes = queries.buscar_decisiones_pendientes()
    print(f"  Encontradas: {len(pendientes)} decisiones pendientes\n")
    
    # 4. Generar resumen de ciclo
    print("[4] Generando resumen del ciclo actual...")
    resumen = queries.generar_resumen_ciclo()
    print(resumen[:400] + "...\n")
    
    print("=" * 60)
    print("✓ Demostración de consultas completada")
    print("=" * 60)


if __name__ == "__main__":
    demo_queries()
