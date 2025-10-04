@echo off
chcp 65001 > nul
echo ========================================
echo    SISTEMA UNIDELIVERY - RABBITMQ
echo ========================================
echo.

echo Iniciando procesador de pedidos...
start "Procesador" cmd /k "cd src && python procesador_pedidos.py"

timeout /t 3 > nul

echo Iniciando consumidor de notificaciones...
start "Consumidor" cmd /k "cd src && python consumidor_notificaciones.py"

timeout /t 3 > nul

echo Iniciando servidor web...
start "Servidor Web" cmd /k "cd src && python productor_pedidos.py"

timeout /t 5 > nul

echo Abriendo navegador...
start http://localhost:5001  // <- CAMBIADO A 5001

echo.
echo ========================================
echo Sistema iniciado correctamente!
echo Interfaz web: http://localhost:5001  // <- CAMBIADO A 5001
echo ========================================
echo.
pause