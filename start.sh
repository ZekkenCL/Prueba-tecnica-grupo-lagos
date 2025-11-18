#!/bin/bash
# Script de inicio rápido para LiquiVerde

echo "🌿 Iniciando LiquiVerde - Plataforma de Retail Inteligente"
echo ""

# Verificar si Docker está corriendo
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker no está corriendo. Por favor inicia Docker Desktop."
    exit 1
fi

echo "✅ Docker detectado"
echo ""

# Construir e iniciar servicios
echo "🔨 Construyendo imágenes de Docker..."
docker-compose build

echo ""
echo "🚀 Iniciando servicios..."
docker-compose up -d

echo ""
echo "⏳ Esperando que los servicios estén listos (30 segundos)..."
sleep 30

echo ""
echo "📦 Cargando datos iniciales..."
docker-compose exec backend python app/load_initial_data.py

echo ""
echo "✅ ¡LiquiVerde está listo!"
echo ""
echo "🌐 Accede a la aplicación:"
echo "   Frontend: http://localhost:5173"
echo "   API Backend: http://localhost:8000"
echo "   Documentación API: http://localhost:8000/docs"
echo ""
echo "📝 Para detener los servicios: docker-compose down"
echo "🗑️  Para eliminar datos: docker-compose down -v"
