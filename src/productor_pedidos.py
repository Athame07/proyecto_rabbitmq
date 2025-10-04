import pika
import os
import json
import random
from datetime import datetime
from flask import Flask, render_template, request, jsonify

# Importación corregida
try:
    from conexion import conectar_rabbitmq
except ImportError:
    # Si falla, intenta importar de manera absoluta
    import sys
    sys.path.append(os.path.dirname(__file__))
    from conexion import conectar_rabbitmq

def generar_pedido_aleatorio():
    """Genera un pedido simulado con datos aleatorios."""
    usuarios = ["estudiante_001", "profesor_015", "admin_003", "estudiante_078"]
    productos = ["Café Americano", "Café con Leche", "Caballeros", "Empanadas", "Hamburguesa","Arepa de Queso", "Perros Calientes"]
    ubicaciones = ["Bloque A", "Bloque B", "Biblioteca", "Laboratorios", "Administración"]
    
    return {
        "id_pedido": f"PED{random.randint(1000, 9999)}",
        "usuario": random.choice(usuarios),
        "producto": random.choice(productos),
        "cantidad": random.randint(1, 3),
        "ubicacion_entrega": random.choice(ubicaciones),
        "timestamp": datetime.now().isoformat(),
        "estado": "pendiente"
    }

def publicar_pedido(pedido_personalizado=None):
    """Publica un pedido en la cola 'cola_pedidos'."""
    canal = conectar_rabbitmq()
    if not canal:
        print("ERROR: No se pudo conectar a RabbitMQ")
        return False
    
    pedido = pedido_personalizado if pedido_personalizado else generar_pedido_aleatorio()
    
    try:
        mensaje = json.dumps(pedido)
        canal.basic_publish(
            exchange='pedidos_exchange',
            routing_key='pedido.nuevo',
            body=mensaje,
            properties=pika.BasicProperties(
                delivery_mode=2,
            )
        )
        print(f"[Productor] Pedido publicado: {pedido['id_pedido']} - {pedido['producto']}")
        return True
    except Exception as e:
        print(f"Error publicando pedido: {e}")
        return False

# Configuración de Flask SIMPLIFICADA
app = Flask(__name__)

# Rutas absolutas para templates y static
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
app.template_folder = os.path.join(base_dir, 'templates')
app.static_folder = os.path.join(base_dir, 'static')

@app.route('/')
def index():
    try:
        return render_template('interfaz_pedidos.html')
    except Exception as e:
        return f"Error cargando template: {e}"

@app.route('/generar-pedido', methods=['POST'])
def generar_pedido_web():
    try:
        data = request.json
        pedido_personalizado = {
            "id_pedido": f"PED{random.randint(1000, 9999)}",
            "usuario": data.get('usuario', 'usuario_generico'),
            "producto": data.get('producto', 'Producto General'),
            "cantidad": int(data.get('cantidad', 1)),
            "ubicacion_entrega": data.get('ubicacion', 'Bloque Principal'),
            "timestamp": datetime.now().isoformat(),
            "estado": "pendiente"
        }
        
        if publicar_pedido(pedido_personalizado):
            return jsonify({"status": "success", "pedido": pedido_personalizado})
        else:
            return jsonify({"status": "error", "message": "Error al publicar pedido"})
    except Exception as e:
        return jsonify({"status": "error", "message": f"Error del servidor: {e}"})

if __name__ == "__main__":
    print("=" * 50)
    print("INICIANDO SERVIDOR FLASK")
    print("=" * 50)
    print(f"Template folder: {app.template_folder}")
    print(f"Static folder: {app.static_folder}")
    print("Servidor web iniciado en http://localhost:5001")
    print("=" * 50)
    
    try:
        app.run(debug=True, host='0.0.0.0', port=5001, use_reloader=False)
    except Exception as e:
        print(f"ERROR al iniciar Flask: {e}")
        input("Presiona Enter para continuar...")