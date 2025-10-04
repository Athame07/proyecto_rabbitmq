import json
from conexion import conectar_rabbitmq

def recibir_notificacion(ch, method, properties, body):
    """Recibe y muestra las notificaciones del sistema."""
    try:
        notificacion = json.loads(body.decode())
        
        print("\n" + "="*50)
        print("NUEVA NOTIFICACION DE PEDIDO")
        print("="*50)
        print(f"ID Pedido: {notificacion['pedido_id']}")
        print(f"Estado: {notificacion['estado'].upper()}")
        print(f"Repartidor: {notificacion['repartidor']}")
        print(f"Tiempo estimado: {notificacion['tiempo_estimado']} min")
        print(f"Mensaje: {notificacion['mensaje']}")
        print(f"Timestamp: {notificacion['timestamp']}")
        print("="*50 + "\n")
        
        ch.basic_ack(delivery_tag=method.delivery_tag)
        
    except Exception as e:
        print(f"Error procesando notificacion: {e}")

def iniciar_consumidor():
    """Escucha notificaciones en la cola 'cola_notificaciones'."""
    canal = conectar_rabbitmq()
    if not canal:
        return
    
    canal.basic_consume(
        queue='cola_notificaciones',
        on_message_callback=recibir_notificacion
    )
    
    print("[Consumidor] Escuchando notificaciones...")
    canal.start_consuming()

if __name__ == "__main__":
    iniciar_consumidor()