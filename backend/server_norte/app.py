from flask import Flask, request, jsonify
import mysql.connector
from kafka import KafkaProducer
import json
import time
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import os

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="eventlet")

# Variable de sucursal (obtenida del entorno)
SUCURSAL = os.getenv("SUCURSAL", "Norte")

# Función para inicializar KafkaProducer con reintentos
def create_kafka_producer(max_retries=10, wait_time=5):
    retries = 0
    while retries < max_retries:
        try:
            producer = KafkaProducer(
                bootstrap_servers='kafka:9092',
                value_serializer=lambda v: json.dumps(v).encode('utf-8')
            )
            print("Conexión exitosa al broker Kafka desde API")
            return producer
        except Exception as e:
            retries += 1
            print(f"No se pudo conectar a Kafka desde API: {e}. Reintentando en {wait_time} segundos... (Intento {retries}/{max_retries})")
            time.sleep(wait_time)
    raise Exception("No se pudo conectar a Kafka después de varios intentos.")

producer = create_kafka_producer()

# Conexión con MySQL
def connect_to_mysql():
    try:
        db = mysql.connector.connect(
            host='mysql',
            user='user',
            password='password',
            database='pedidos'
        )
        return db
    except mysql.connector.Error as e:
        print(f"No se pudo conectar a MySQL: {e}")
        return None

# Endpoint para obtener los pedidos
@app.route('/pedido', methods=['GET'])
def obtener_pedido():
    sucursal = request.args.get('sucursal')
    db = connect_to_mysql()
    if db is None:
        return jsonify({"error": "No se pudo conectar a la base de datos"}), 500

    cursor = db.cursor(dictionary=True)
    query = "SELECT * FROM pedidos"
    if sucursal:
        query += " WHERE sucursal = %s"
        cursor.execute(query, (sucursal,))
    else:
        cursor.execute(query)
        
    pedidos = cursor.fetchall()
    pedidos_sorted = sorted(pedidos, key=lambda x: x['fecha'], reverse=True)

    return jsonify(pedidos_sorted)

# Endpoint para crear un pedido
@app.route('/pedido', methods=['POST'])
def crear_pedido():
    data = request.json
    try:
        # Envía el mensaje al topic 'pedidos'
        producer.send('pedidos', data)
        print(f"Pedido enviado a Kafka: {data}")
        socketio.emit('actualizacion', {'mensaje': 'Nuevo pedido añadido', 'pedido': data}, broadcast=True)
        return jsonify({"message": "Pedido enviado a Kafka"}), 201
    except Exception as e:
        print(f"Error al enviar el mensaje a Kafka: {e}")
        return jsonify({"error": "No se pudo enviar el pedido a Kafka"}), 500
@app.route('/api/sucursal', methods=['GET'])
def get_sucursal():
    return jsonify({"sucursal": SUCURSAL})

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)
