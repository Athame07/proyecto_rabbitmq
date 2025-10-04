import pika
import json
import time
import random
from conexion import conectar_rabbitmq

def procesar_pedido(ch, method, properties, body):
    """Procesa el pedido recibido y publica la notificación."""
    try:
        pedido = json.loads(body.decode())
        print(f"[Procesador] Pedido recibido: {pedido['id_pedido']}")
        
        # Simular procesamiento del pedido
        time.sleep(2)  # Simular tiempo de procesamiento
        
        # Asignar repartidor aleatorio
        repartidores = ["Carlos R.", "Ana M.", "Luis P.", "María G."]
        repartidor_asignado = random.choice(repartidores)
        
        # Actualizar estado del pedido
        pedido['estado'] = 'en_preparacion'
        pedido['repartidor'] = repartidor_asignado
        pedido['tiempo_estimado'] = random.randint(10, 25)
        
        # Publicar notificación
        canal = conectar_rabbitmq()
        if canal:
            notificacion = {
                "tipo": "estado_pedido",
                "pedido_id": pedido['id_pedido'],
                "estado": pedido['estado'],
                "repartidor": repartidor_asignado,
                "tiempo_estimado": pedido['tiempo_estimado'],
                "mensaje": f"Pedido {pedido['id_pedido']} en preparación. Repartidor: {repartidor_asignado}",
                "timestamp": pedido['timestamp']
            }
            
            mensaje = json.dumps(notificacion)
            canal.basic_publish(
                exchange='notificaciones_exchange',
                routing_key='',
                body=mensaje,
                properties=pika.BasicProperties(
                    delivery_mode=2,
                )
            )
            print(f"[Procesador] Notificación publicada para: {pedido['id_pedido']}")
        
        ch.basic_ack(delivery_tag=method.delivery_tag)
        
    except Exception as e:
        print(f"Error procesando pedido: {e}")

def iniciar_procesador():
    """Escucha pedidos en la cola 'cola_pedidos'."""
    canal = conectar_rabbitmq()
    if not canal:
        return
    
    canal.basic_qos(prefetch_count=1)
    canal.basic_consume(
        queue='cola_pedidos',
        on_message_callback=procesar_pedido
    )
    
    print("[Procesador] Iniciando procesamiento de pedidos...")
    canal.start_consuming()

if __name__ == "__main__":
    iniciar_procesador()