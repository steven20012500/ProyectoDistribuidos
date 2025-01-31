from kafka import KafkaConsumer
import mysql.connector
import json
import time

# Función para inicializar el consumidor Kafka con reintentos
def create_kafka_consumer():
    while True:
        try:
            consumer = KafkaConsumer(
                'pedidos',
                bootstrap_servers='kafka:9092',
                value_deserializer=lambda v: json.loads(v.decode('utf-8'))
            )
            print("Conexión exitosa al broker Kafka desde el consumidor")
            return consumer
        except Exception as e:
            print(f"No se pudo conectar a Kafka desde el consumidor: {e}. Reintentando en 5 segundos...")
            time.sleep(5)

# Función para conectar a la base de datos MySQL con reintentos
def connect_to_mysql():
    while True:
        try:
            db = mysql.connector.connect(
                host='mysql',
                user='user',
                password='password',
                database='pedidos'
            )
            print("Conexión exitosa a MySQL desde el consumidor")
            return db
        except mysql.connector.Error as e:
            print(f"No se pudo conectar a MySQL desde el consumidor: {e}. Reintentando en 5 segundos...")
            time.sleep(5)

# Inicializa las conexiones con reintentos
consumer = create_kafka_consumer()
db = connect_to_mysql()
cursor = db.cursor()

# Procesa los mensajes del topic 'pedidos'
for message in consumer:
    try:
        data = message.value
        print(f"Mensaje recibido: {data}")
        cursor.execute(
            "INSERT INTO pedidos (sucursal, producto, cantidad, fecha) VALUES (%s, %s, %s, %s)",
            (data['sucursal'], data['producto'], data['cantidad'], data['fecha'])
        )
        db.commit()
        print("Pedido insertado en la base de datos")
    except Exception as e:
        print(f"Error al procesar el mensaje: {e}")
