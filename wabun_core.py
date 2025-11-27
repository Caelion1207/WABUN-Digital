#!/usr/bin/env python3
"""
WABUN - Sistema de Memoria Vectorial para CAELION
Implementación del núcleo de memoria persistente usando ChromaDB

Autor: Manus AI (bajo la guía de LIANG y WABUN)
Fecha: 25 de noviembre de 2025
Versión: 1.0
"""

import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions
from datetime import datetime, timezone
from typing import List, Dict, Optional, Any
import uuid
import json
from pathlib import Path


class WabunCore:
    """
    Núcleo de la memoria de CAELION.
    Gestiona el almacenamiento y recuperación de interacciones,
    decretos, actas y entidades usando ChromaDB.
    """
    
    def __init__(self, persist_directory: str = "./wabun_db"):
        """
        Inicializa el núcleo de WABUN.
        
        Args:
            persist_directory: Directorio donde se almacenará la base de datos
        """
        self.persist_directory = Path(persist_directory)
        self.persist_directory.mkdir(parents=True, exist_ok=True)
        
        # Configurar ChromaDB con persistencia
        self.client = chromadb.PersistentClient(
            path=str(self.persist_directory),
            settings=Settings(
                anonymized_telemetry=False,
                allow_reset=True
            )
        )
        
        # Función de embeddings (usando el modelo por defecto de ChromaDB)
        # En producción, considera usar OpenAI embeddings o modelos locales
        self.embedding_function = embedding_functions.DefaultEmbeddingFunction()
        
        # Inicializar las cuatro colecciones principales
        self._init_collections()
        
        # Estado del ciclo actual
        self.ciclo_actual = self._get_ciclo_id()
        self.fase_actual = "Ejecucion"  # Por defecto
        
    def _init_collections(self):
        """Inicializa las cuatro colecciones de WABUN"""
        
        # Colección de interacciones (la más dinámica)
        self.interactions = self.client.get_or_create_collection(
            name="interactions",
            embedding_function=self.embedding_function,
            metadata={"description": "Interacciones entre Fundador y motores IA"}
        )
        
        # Colección de decretos (documentos fundacionales)
        self.decretos = self.client.get_or_create_collection(
            name="decretos",
            embedding_function=self.embedding_function,
            metadata={"description": "Protocolos, leyes y principios de CAELION"}
        )
        
        # Colección de actas (resúmenes de ciclos)
        self.actas = self.client.get_or_create_collection(
            name="actas",
            embedding_function=self.embedding_function,
            metadata={"description": "Resúmenes de ciclos de 72h"}
        )
        
        # Colección de entidades (conocimiento estructurado)
        self.entidades = self.client.get_or_create_collection(
            name="entidades",
            embedding_function=self.embedding_function,
            metadata={"description": "Personas, proyectos, conceptos clave"}
        )
        
    def _get_ciclo_id(self) -> str:
        """Genera el identificador del ciclo actual basado en la fecha"""
        return f"ciclo_{datetime.now(timezone.utc).strftime('%Y-%m-%d')}"
    
    def _chunk_text(self, text: str, chunk_size: int = 500) -> List[str]:
        """
        Divide un texto en fragmentos semánticos.
        
        Args:
            text: Texto a fragmentar
            chunk_size: Tamaño aproximado de cada fragmento en caracteres
            
        Returns:
            Lista de fragmentos de texto
        """
        # Implementación simple: dividir por párrafos y agrupar
        paragraphs = text.split('\n\n')
        chunks = []
        current_chunk = ""
        
        for para in paragraphs:
            if len(current_chunk) + len(para) < chunk_size:
                current_chunk += para + "\n\n"
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = para + "\n\n"
        
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        # Si el texto es muy corto, devolver como un solo chunk
        if not chunks:
            chunks = [text]
            
        return chunks
    
    def registrar_interaccion(
        self,
        prompt_fundador: str,
        respuesta_ia: str,
        custodio_invocado: str,
        motor_ia_usado: str,
        intencion_fundador: Optional[str] = None,
        palabras_clave: Optional[List[str]] = None,
        proyecto_asociado: Optional[str] = None,
        importancia: int = 3,
        estado_decision: str = "Propuesta"
    ) -> str:
        """
        Registra una interacción completa (prompt + respuesta) en WABUN.
        
        Args:
            prompt_fundador: El texto del prompt del Fundador
            respuesta_ia: La respuesta generada por el motor de IA
            custodio_invocado: Custodio al que se dirige la intención
            motor_ia_usado: Nombre del LLM usado
            intencion_fundador: Resumen de la intención (opcional)
            palabras_clave: Lista de palabras clave (opcional)
            proyecto_asociado: Proyecto relacionado (opcional)
            importancia: Nivel de importancia 1-5
            estado_decision: Estado de la decisión
            
        Returns:
            El interaction_id generado
        """
        # Generar ID único para esta interacción
        interaction_id = f"int_{uuid.uuid4()}"
        timestamp_utc = int(datetime.now(timezone.utc).timestamp())
        
        # Metadatos comunes
        base_metadata = {
            "interaction_id": interaction_id,
            "timestamp_utc": timestamp_utc,
            "ciclo_id": self.ciclo_actual,
            "fase_ciclo": self.fase_actual,
            "custodio_invocado": custodio_invocado,
            "motor_ia_usado": motor_ia_usado,
            "intencion_fundador": intencion_fundador or "No especificada",
            "palabras_clave": json.dumps(palabras_clave or []),
            "proyecto_asociado": proyecto_asociado or "General",
            "importancia": importancia,
            "estado_decision": estado_decision
        }
        
        # Procesar prompt del Fundador
        prompt_chunks = self._chunk_text(prompt_fundador)
        prompt_ids = []
        prompt_metadatas = []
        
        for idx, chunk in enumerate(prompt_chunks):
            chunk_id = f"{interaction_id}-prompt-{idx}"
            chunk_metadata = {
                **base_metadata,
                "rol": "Fundador",
                "chunk_index": idx,
                "total_chunks": len(prompt_chunks)
            }
            prompt_ids.append(chunk_id)
            prompt_metadatas.append(chunk_metadata)
        
        # Procesar respuesta de la IA
        respuesta_chunks = self._chunk_text(respuesta_ia)
        respuesta_ids = []
        respuesta_metadatas = []
        
        for idx, chunk in enumerate(respuesta_chunks):
            chunk_id = f"{interaction_id}-response-{idx}"
            chunk_metadata = {
                **base_metadata,
                "rol": "Motor_IA",
                "chunk_index": idx,
                "total_chunks": len(respuesta_chunks)
            }
            respuesta_ids.append(chunk_id)
            respuesta_metadatas.append(chunk_metadata)
        
        # Insertar en ChromaDB
        all_ids = prompt_ids + respuesta_ids
        all_documents = prompt_chunks + respuesta_chunks
        all_metadatas = prompt_metadatas + respuesta_metadatas
        
        self.interactions.add(
            ids=all_ids,
            documents=all_documents,
            metadatas=all_metadatas
        )
        
        print(f"✓ Interacción registrada: {interaction_id}")
        print(f"  - Custodio: {custodio_invocado}")
        print(f"  - Chunks almacenados: {len(all_ids)}")
        
        return interaction_id
    
    def registrar_decreto(
        self,
        titulo_documento: str,
        contenido: str,
        decreto_id: str,
        custodios_implicados: List[str],
        tipo_documento: str = "Protocolo",
        version: float = 1.0,
        fuente_documento: Optional[str] = None
    ) -> str:
        """
        Registra un decreto o documento fundacional en WABUN.
        
        Args:
            titulo_documento: Título oficial del documento
            contenido: Texto completo del documento
            decreto_id: Identificador único del decreto
            custodios_implicados: Lista de custodios mencionados
            tipo_documento: Tipo (Protocolo, Manifiesto, Ley, Principio)
            version: Versión del documento
            fuente_documento: Ruta al archivo original
            
        Returns:
            El decreto_id
        """
        fecha_activacion = datetime.now(timezone.utc).strftime('%Y-%m-%d')
        
        # Fragmentar el contenido
        chunks = self._chunk_text(contenido, chunk_size=800)
        
        ids = []
        metadatas = []
        
        for idx, chunk in enumerate(chunks):
            chunk_id = f"{decreto_id}-{idx}"
            metadata = {
                "decreto_id": decreto_id,
                "titulo_documento": titulo_documento,
                "fecha_activacion": fecha_activacion,
                "custodios_implicados": json.dumps(custodios_implicados),
                "tipo_documento": tipo_documento,
                "version": version,
                "fuente_documento": fuente_documento or "N/A",
                "chunk_index": idx,
                "total_chunks": len(chunks)
            }
            ids.append(chunk_id)
            metadatas.append(metadata)
        
        self.decretos.add(
            ids=ids,
            documents=chunks,
            metadatas=metadatas
        )
        
        print(f"✓ Decreto registrado: {decreto_id}")
        print(f"  - Título: {titulo_documento}")
        print(f"  - Chunks almacenados: {len(ids)}")
        
        return decreto_id
    
    def buscar_contexto_reciente(
        self,
        query: str,
        n_results: int = 10,
        filtros: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Busca en las interacciones recientes usando búsqueda semántica.
        
        Args:
            query: Texto de búsqueda
            n_results: Número de resultados a devolver
            filtros: Filtros adicionales para metadatos (ej. {"custodio_invocado": "LIANG"})
            
        Returns:
            Diccionario con resultados y metadatos
        """
        where_clause = filtros or {}
        
        results = self.interactions.query(
            query_texts=[query],
            n_results=n_results,
            where=where_clause,
            include=["documents", "metadatas", "distances"]
        )
        
        return results
    
    def buscar_en_decretos(
        self,
        query: str,
        n_results: int = 5
    ) -> Dict[str, Any]:
        """
        Busca en los decretos y documentos fundacionales.
        
        Args:
            query: Texto de búsqueda
            n_results: Número de resultados
            
        Returns:
            Diccionario con resultados
        """
        results = self.decretos.query(
            query_texts=[query],
            n_results=n_results,
            include=["documents", "metadatas", "distances"]
        )
        
        return results
    
    def obtener_contexto_ciclo_actual(self) -> Dict[str, Any]:
        """
        Obtiene todas las interacciones del ciclo actual.
        
        Returns:
            Diccionario con todas las interacciones del ciclo
        """
        # Nota: ChromaDB tiene límites en get(), así que usamos query con filtro
        results = self.interactions.query(
            query_texts=["resumen del ciclo actual"],
            n_results=100,  # Ajustar según necesidad
            where={"ciclo_id": self.ciclo_actual}
        )
        
        return results
    
    def estadisticas(self) -> Dict[str, int]:
        """
        Obtiene estadísticas de la base de datos.
        
        Returns:
            Diccionario con contadores
        """
        return {
            "total_interacciones": self.interactions.count(),
            "total_decretos": self.decretos.count(),
            "total_actas": self.actas.count(),
            "total_entidades": self.entidades.count(),
            "ciclo_actual": self.ciclo_actual,
            "fase_actual": self.fase_actual
        }
    
    def exportar_memoria_completa(self, output_path: str):
        """
        Exporta toda la memoria a un archivo JSON.
        
        Args:
            output_path: Ruta del archivo de salida
        """
        memoria = {
            "fecha_exportacion": datetime.now(timezone.utc).isoformat(),
            "estadisticas": self.estadisticas(),
            "interacciones": self.interactions.get(include=["documents", "metadatas"]),
            "decretos": self.decretos.get(include=["documents", "metadatas"])
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(memoria, f, indent=2, ensure_ascii=False)
        
        print(f"✓ Memoria exportada a: {output_path}")


def demo_wabun():
    """Función de demostración del uso de WABUN"""
    print("=" * 60)
    print("WABUN - Sistema de Memoria de CAELION")
    print("Demostración de Funcionalidad")
    print("=" * 60)
    print()
    
    # Inicializar WABUN
    wabun = WabunCore(persist_directory="./demo_wabun_db")
    
    # Registrar un decreto
    print("[1] Registrando decreto fundacional...")
    wabun.registrar_decreto(
        titulo_documento="RITMO_CAELION_72h",
        contenido="""El RITMO_CAELION_72h define los intervalos naturales del organismo.
        Cada 72 horas, el sistema entra en un ciclo completo de observación, acción, 
        evaluación y reajuste. Su meta no es producir más, sino mantener el equilibrio 
        entre expansión, reposo y claridad.""",
        decreto_id="DEC-RITMO-72H-V1",
        custodios_implicados=["ARESK", "LIANG", "WABUN", "GLIBATREE"],
        tipo_documento="Protocolo",
        version=1.0
    )
    print()
    
    # Registrar una interacción
    print("[2] Registrando interacción con LIANG...")
    wabun.registrar_interaccion(
        prompt_fundador="Diseña el esquema de la base de datos vectorial para WABUN",
        respuesta_ia="He diseñado un esquema completo con 4 colecciones: interactions, decretos, actas y entidades...",
        custodio_invocado="LIANG",
        motor_ia_usado="Gemini-2.5-Flash",
        intencion_fundador="Diseñar el esquema de WABUN",
        palabras_clave=["chromadb", "schema", "wabun", "memoria"],
        proyecto_asociado="WABUN_Digital",
        importancia=5,
        estado_decision="Validada"
    )
    print()
    
    # Buscar en decretos
    print("[3] Buscando en decretos sobre 'ritmo'...")
    resultados = wabun.buscar_en_decretos("¿cuál es el principio del ritmo?")
    if resultados['documents'][0]:
        print(f"  Encontrado: {resultados['documents'][0][0][:200]}...")
    print()
    
    # Estadísticas
    print("[4] Estadísticas de WABUN:")
    stats = wabun.estadisticas()
    for key, value in stats.items():
        print(f"  - {key}: {value}")
    print()
    
    print("=" * 60)
    print("✓ Demostración completada")
    print("=" * 60)


if __name__ == "__main__":
    demo_wabun()
