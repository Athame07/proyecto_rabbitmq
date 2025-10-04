@echo off
chcp 65001 > nul
echo ========================================
echo    DIAGNOSTICO SISTEMA UNIDELIVERY
echo ========================================
echo.


echo 1. Verificando archivos...
if exist "src\productor_pedidos.py" (
    echo ✓ productor_pedidos.py encontrado
) else (
    echo ✗ ERROR: productor_pedidos.py no encontrado
    pause
    exit
)

if exist "templates\interfaz_pedidos.html" (
    echo ✓ interfaz_pedidos.html encontrado
) else (
    echo ✗ ERROR: interfaz_pedidos.html no encontrado
)

echo.
echo 2. Verificando RabbitMQ...
netstat -an | find ":5672" > nul
if %errorlevel% == 0 (
    echo ✓ RabbitMQ corriendo en puerto 5672
) else (
    echo ✗ RabbitMQ NO detectado en puerto 5672
)

echo.
echo 3. Verificando puerto 5000...
netstat -an | find ":5000" > nul
if %errorlevel% == 0 (
    echo ✗ Puerto 5000 esta en uso
) else (
    echo ✓ Puerto 5000 disponible
)

echo.
echo 4. Iniciando servidor Flask manualmente...
echo    (Mira si hay errores en esta ventana)
echo ========================================
cd src
python productor_pedidos.py

pause