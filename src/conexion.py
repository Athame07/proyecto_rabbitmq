import pika

def conectar_rabbitmq():
    """Establece conexión con RabbitMQ en localhost."""
    try:
        conexion = pika.BlockingConnection(
            pika.ConnectionParameters('localhost')
        )
        canal = conexion.channel()
        
        # Declarar exchanges y colas
        canal.exchange_declare(exchange='pedidos_exchange', exchange_type='direct')
        canal.exchange_declare(exchange='notificaciones_exchange', exchange_type='fanout')
        
        canal.queue_declare(queue='cola_pedidos', durable=True)
        canal.queue_declare(queue='cola_notificaciones', durable=True)
        
        # Binding de colas
        canal.queue_bind(exchange='pedidos_exchange', queue='cola_pedidos', routing_key='pedido.nuevo')
        canal.queue_bind(exchange='notificaciones_exchange', queue='cola_notificaciones')
        
        return canal
    except Exception as e:
        print(f"Error conectando a RabbitMQ: {e}")
        return None