# Script de inicio rápido para LiquiVerde (Windows PowerShell)

Write-Host "🌿 Iniciando LiquiVerde - Plataforma de Retail Inteligente" -ForegroundColor Green
Write-Host ""

# Verificar si Docker está corriendo
try {
    docker info | Out-Null
    Write-Host "✅ Docker detectado" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker no está corriendo. Por favor inicia Docker Desktop." -ForegroundColor Red
    exit 1
}

Write-Host ""

# Construir e iniciar servicios
Write-Host "🔨 Construyendo imágenes de Docker..." -ForegroundColor Yellow
docker-compose build

Write-Host ""
Write-Host "🚀 Iniciando servicios..." -ForegroundColor Yellow
docker-compose up -d

Write-Host ""
Write-Host "⏳ Esperando que los servicios estén listos (30 segundos)..." -ForegroundColor Yellow
Start-Sleep -Seconds 30

Write-Host ""
Write-Host "📦 Cargando datos iniciales..." -ForegroundColor Yellow
docker-compose exec backend python app/load_initial_data.py

Write-Host ""
Write-Host "✅ ¡LiquiVerde está listo!" -ForegroundColor Green
Write-Host ""
Write-Host "🌐 Accede a la aplicación:" -ForegroundColor Cyan
Write-Host "   Frontend: http://localhost:5173"
Write-Host "   API Backend: http://localhost:8000"
Write-Host "   Documentación API: http://localhost:8000/docs"
Write-Host ""
Write-Host "📝 Para detener los servicios: docker-compose down" -ForegroundColor Yellow
Write-Host "🗑️  Para eliminar datos: docker-compose down -v" -ForegroundColor Yellow
