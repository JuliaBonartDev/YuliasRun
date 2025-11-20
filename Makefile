# Makefile para Julia's Run
# Proyecto educativo para aprender POO con Python y Pygame
# Comandos simplificados para estudiantes y educadores

# Variables de configuración
PYTHON = python
SRC_DIR = src
TESTS_DIR = tests
DOCS_DIR = docs

# Comando por defecto
.DEFAULT_GOAL := help

# === COMANDOS PRINCIPALES ===

.PHONY: run
run: ## 🎮 Ejecutar el juego directamente (sin venv)
	@echo "🚀 Iniciando Julia's Run..."
	@echo "💡 Presiona ESC para salir del juego"
	$(PYTHON) $(SRC_DIR)/main.py

.PHONY: install
install: ## 📦 Instalar dependencias necesarias
	@echo "📦 Instalando dependencias para Julia's Run..."
	@echo "🔍 Verificando Python..."
	@$(PYTHON) --version
	@echo "🎮 Instalando Pygame..."
	pip install pygame
	@echo "✅ ¡Dependencias instaladas correctamente!"
	@echo "💡 Ejecuta 'make run' para probar el juego"

.PHONY: check
check: ## ✅ Verificar que todo funciona correctamente
	@echo "Verificando funcionamiento del proyecto..."
	@echo "1. Verificando sintaxis de Python..."
	@$(PYTHON) -m py_compile src/main.py
	@$(PYTHON) -m py_compile src/entities.py
	@$(PYTHON) -m py_compile src/settings.py
	@echo "   Sintaxis correcta"
	@echo "2. Verificando que Pygame esta disponible..."
	@$(PYTHON) -c "import pygame; print('   Pygame disponible v' + pygame.version.ver)"
	@echo "3. Verificando estructura de archivos..."
	@if exist "src\main.py" (echo    main.py existe) else (echo    main.py falta)
	@if exist "src\entities.py" (echo    entities.py existe) else (echo    entities.py falta)
	@if exist "src\settings.py" (echo    settings.py existe) else (echo    settings.py falta)
	@if exist "assets\sprites" (echo    Carpeta de sprites existe) else (echo    Carpeta de sprites falta)
	@echo "Verificacion completada correctamente"

.PHONY: test
test: ## 🧪 Ejecutar tests (si están disponibles)
	@echo "🧪 Ejecutando tests..."
	@if exist "$(TESTS_DIR)\*.py" ($(PYTHON) -m unittest discover $(TESTS_DIR) -v) else (echo ℹ️ No hay tests disponibles todavía)

.PHONY: clean
clean: ## 🧹 Limpiar archivos temporales
	@echo "🧹 Limpiando archivos temporales..."
	@if exist "__pycache__" (rmdir /s /q __pycache__ && echo    ✅ Cache de Python limpiado)
	@if exist ".pytest_cache" (rmdir /s /q .pytest_cache && echo    ✅ Cache de pytest limpiado)
	@for /r %%i in (*.pyc) do @del "%%i" 2>nul
	@echo "✅ Limpieza completada"

.PHONY: docs
docs: ## 📚 Mostrar documentación disponible
	@echo "📚 Documentación educativa disponible:"
	@echo "   📖 README.md - Introducción y contexto del proyecto"
	@echo "   📖 $(DOCS_DIR)\01_intro_poo_con_julias_run.md - Tutorial completo de POO"
	@echo "   📖 $(DOCS_DIR)\02_reto_mejoras.md - Retos y sistema de evaluación"
	@echo "   📖 $(SRC_DIR)\README.md - Explicación técnica del código"
	@echo "   📖 assets\README.md - Información sobre recursos gráficos"
	@echo ""
	@echo "💡 Recomendación: Empieza leyendo README.md y luego el tutorial de POO"

.PHONY: setup
setup: install check ## 🔧 Configuración completa inicial
	@echo ""
	@echo "🎯 ¡Julia's Run configurado exitosamente!"
	@echo ""
	@echo "📋 Próximos pasos recomendados:"
	@echo "   1. 🎮 Ejecuta: make run"
	@echo "   2. 🕐 Juega al menos 5-10 minutos para entender la mecánica"
	@echo "   3. 📖 Lee: docs\01_intro_poo_con_julias_run.md"
	@echo "   4. 🔍 Explora el código en la carpeta src\"
	@echo "   5. 🚀 ¡Empieza a implementar mejoras!"
	@echo ""
	@echo "💡 Si tienes dudas, ejecuta 'make help' para ver todos los comandos"

# === COMANDOS PARA ESTUDIANTES ===

.PHONY: student-setup
student-setup: ## 🎓 Configuración específica para estudiantes
	@echo "🎓 Configurando entorno de aprendizaje..."
	@make install --no-print-directory
	@make check --no-print-directory
	@echo "📁 Creando espacio de trabajo personal..."
	@if not exist "mi_trabajo" mkdir mi_trabajo
	@echo "# Mis Notas sobre Julia's Run" > mi_trabajo\notas.md
	@echo.>> mi_trabajo\notas.md
	@echo "## 🎯 Objetivos de aprendizaje" >> mi_trabajo\notas.md
	@echo "- [ ] Entender qué son las clases y objetos" >> mi_trabajo\notas.md
	@echo "- [ ] Identificar atributos y métodos" >> mi_trabajo\notas.md
	@echo "- [ ] Comprender la encapsulación" >> mi_trabajo\notas.md
	@echo "- [ ] Implementar mi primera mejora" >> mi_trabajo\notas.md
	@echo.>> mi_trabajo\notas.md
	@echo "## 📝 Notas del código" >> mi_trabajo\notas.md
	@echo "(Escribe aquí tus observaciones mientras exploras el código)" >> mi_trabajo\notas.md
	@echo ""
	@echo "🎉 ¡Configuración de estudiante completada!"
	@echo "📁 Usa la carpeta 'mi_trabajo\' para tus anotaciones y ejercicios"

.PHONY: validate-student
validate-student: ## 🎓 Validar el trabajo de un estudiante
	@echo "🎓 Validando trabajo de estudiante..."
	@echo "1️⃣ Verificando funcionamiento básico..."
	@make check --no-print-directory
	@echo "2️⃣ Verificando documentación del estudiante..."
	@if exist "mi_trabajo\README_MEJORAS.md" (echo    ✅ Documentación de mejoras presente) else (echo    ⚠️ Falta documentación de mejoras)
	@if exist "mi_trabajo\" (echo    ✅ Carpeta de trabajo existe) else (echo    ❌ Falta carpeta de trabajo)
	@echo "3️⃣ Verificando tests personalizados..."
	@if exist "mi_trabajo\test_*.py" (echo    ✅ Tests personalizados encontrados) else (echo    ℹ️ No hay tests personalizados)
	@echo "🎉 Validación completada - Revisa los resultados arriba"

# === COMANDOS PARA DESARROLLO ===

.PHONY: dev-run
dev-run: ## 🛠️ Ejecutar en modo debug/desarrollo
	@echo "🛠️ Ejecutando en modo desarrollo..."
	@echo "💡 Presiona Ctrl+C para terminar"
	$(PYTHON) $(SRC_DIR)/main.py

.PHONY: profile
profile: ## 📊 Análisis de rendimiento del juego
	@echo "📊 Ejecutando análisis de rendimiento..."
	$(PYTHON) -m cProfile -s cumulative $(SRC_DIR)/main.py

.PHONY: backup
backup: ## 💾 Crear respaldo del trabajo actual
	@echo "💾 Creando respaldo..."
	@for /f "tokens=1-4 delims=/ " %%a in ('date /t') do set mydate=%%c%%a%%b
	@for /f "tokens=1-2 delims=: " %%a in ('time /t') do set mytime=%%a%%b
	@set timestamp=%mydate%_%mytime: =0%
	@powershell Compress-Archive -Path .\* -DestinationPath backup_julia_run_%timestamp%.zip -Force 2>nul || echo ❌ Error creando backup
	@echo ✅ Backup creado con timestamp

# === INFORMACIÓN Y AYUDA ===

.PHONY: info
info: ## ℹ️ Información detallada del proyecto
	@echo "🎮 Julia's Run - Proyecto Educativo de POO"
	@echo "════════════════════════════════════════"
	@echo "📊 Estadísticas del proyecto:"
	@for /f %%i in ('dir /s /b $(SRC_DIR)\*.py ^| find /c ".py"') do echo    📄 Archivos Python: %%i
	@for /f %%i in ('dir /s /b $(DOCS_DIR)\*.md ^| find /c ".md"') do echo    📚 Documentos: %%i
	@for /f %%i in ('dir /s /b assets\sprites\*.jpg ^| find /c ".jpg" 2^>nul') do echo    🎨 Sprites: %%i
	@echo ""
	@echo "🎯 Objetivos educativos:"
	@echo "   - Comprensión práctica de POO"
	@echo "   - Trabajo con código legacy real"
	@echo "   - Refactorización y mejora continua"
	@echo "   - Desarrollo de habilidades de debugging"
	@echo ""
	@echo "🔗 Tecnologías: Python 3 + Pygame"

.PHONY: help
help: ## ❓ Mostrar todos los comandos disponibles
	@echo "🎮 Julia's Run - Comandos disponibles"
	@echo "═══════════════════════════════════════"
	@echo ""
	@findstr /R "^[a-zA-Z_-]*:.*##" Makefile | for /f "tokens=1,2* delims=:##" %%a in ('more') do @echo   %%a: %%c
	@echo ""
	@echo "💡 Comandos más utilizados:"
	@echo "   make run          - Ejecutar el juego"
	@echo "   make setup        - Configuración inicial completa"
	@echo "   make student-setup - Configuración para estudiantes"
	@echo "   make docs         - Ver documentación disponible"
	@echo "   make help         - Mostrar esta ayuda"
	@echo ""
	@echo "🎓 Para estudiantes: make student-setup
	@echo "🔧 Para desarrollo: make dev-run"

.PHONY: watch
watch: ## 👀 Ejecutar el juego con nodemon (reinicio automático al guardar)
	@echo "👀 Iniciando Julia's Run con nodemon..."
	@echo "💡 Cada vez que guardes un archivo, el juego se reiniciará"
	nodemon --exec $(PYTHON) $(SRC_DIR)/main.py