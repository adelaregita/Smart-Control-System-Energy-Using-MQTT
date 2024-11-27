import paho.mqtt.client as mqtt
import threading
import time
import random

# Konfigurasi broker dan topik
BROKER = "test.mosquitto.org"
PORT = 1883
TOPIC_SEND = "DariKamar1"
TOPIC_RECEIVE = "KeKamar1"

# Callback saat terhubung ke broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Sensor 1 connected successfully!")
    else:
        print("Connection failed with result code", rc)
    # Subscribe ke topik untuk menerima data
    client.subscribe(TOPIC_RECEIVE)
    print(f"Subscribed to topic: {TOPIC_RECEIVE}")

# Callback saat menerima pesan
def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode()
        print(f"Sensor 1 received: {msg.topic} {payload}")
    except Exception as e:
        print(f"Error processing message: {e}")

# Fungsi untuk mengirim data
def send_data(client):
    while True:
        try:
            data = f"Sensor1 data: {random.randint(0, 100)}"
            client.publish(TOPIC_SEND, data)
            print(f"Sensor 1 sent: {data}")
            time.sleep(5)
        except Exception as e:
            print(f"Error sending data: {e}")

# Fungsi utama untuk menjalankan MQTT client
def run_sensor1():
    client = mqtt.Client(client_id="Sensor1", protocol=mqtt.MQTTv311)
    client.on_connect = on_connect
    client.on_message = on_message

    # Koneksi ke broker
    client.connect(BROKER, PORT, 60)
    client.loop_start()

    # Jalankan pengiriman data
    send_data(client)

# Multithreading untuk Sensor 1
if __name__ == "__main__":
    sensor1_thread = threading.Thread(target=run_sensor1)
    sensor1_thread.start()
