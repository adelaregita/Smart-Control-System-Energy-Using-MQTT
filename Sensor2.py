import paho.mqtt.client as mqtt
import threading
import time
import random  # Import modul random

# Konfigurasi broker dan topik
BROKER = "test.mosquitto.org"
PORT = 1883
TOPIC_SEND = "DariKamar2"
TOPIC_RECEIVE = "KeKamar2"

# Variabel global untuk menyimpan akumulasi data
accumulated_value = 0

# Callback saat terhubung ke broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Sensor 2 connected successfully!")
    else:
        print("Connection failed with result code", rc)
    # Subscribe ke topik untuk menerima data
    client.subscribe(TOPIC_RECEIVE)
    print(f"Subscribed to topic: {TOPIC_RECEIVE}")

# Callback saat menerima pesan
def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode()
        print(f"Sensor 2 received: {msg.topic} {payload}")
    except Exception as e:
        print(f"Error processing message: {e}")

# Fungsi untuk mengirim data
def send_data(client):
    global accumulated_value  # Gunakan variabel global untuk akumulasi
    while True:
        try:
            # Tambahkan nilai random ke akumulasi
            random_value = random.randint(1, 20)  # Nilai random antara 1 dan 20
            accumulated_value += random_value  # Tambahkan ke akumulasi
            data = f"Sensor2 accumulated data: {accumulated_value}"
            client.publish(TOPIC_SEND, data)
            print(f"Sensor 2 sent: {data}")
            time.sleep(5)  # Tunggu 5 detik sebelum mengirim data berikutnya
        except Exception as e:
            print(f"Error sending data: {e}")

# Fungsi utama untuk menjalankan MQTT client
def run_sensor2():
    client = mqtt.Client(client_id="Sensor2", protocol=mqtt.MQTTv311)
    client.on_connect = on_connect
    client.on_message = on_message

    # Koneksi ke broker
    client.connect(BROKER, PORT, 60)
    client.loop_start()

    # Jalankan pengiriman data
    send_data(client)

# Multithreading untuk Sensor 2
if __name__ == "__main__":
    sensor2_thread = threading.Thread(target=run_sensor2)
    sensor2_thread.start()
