#!/bin/bash
# Script de instalación para WABUN Digital
# Autor: Manus AI
# Fecha: 25 de noviembre de 2025

echo "=========================================="
echo "WABUN Digital - Instalación"
echo "=========================================="
echo ""

# Crear entorno virtual
echo "[1/3] Creando entorno virtual..."
python3 -m venv wabun_env

# Activar entorno virtual
echo "[2/3] Instalando dependencias..."
source wabun_env/bin/activate

# Instalar ChromaDB
pip install chromadb --quiet

echo "[3/3] Verificando instalación..."
python3 -c "import chromadb; print('✓ ChromaDB instalado correctamente')"

echo ""
echo "=========================================="
echo "✓ Instalación completada"
echo "=========================================="
echo ""
echo "Para usar WABUN:"
echo "  1. Activa el entorno: source wabun_env/bin/activate"
echo "  2. Ejecuta: python3 wabun_core.py"
echo ""
