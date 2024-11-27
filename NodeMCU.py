import paho.mqtt.client as mqtt
import threading

# Konfigurasi Broker dan Port
BROKER = "test.mosquitto.org"
PORT = 1883

# Daftar topik sesuai aturan
TOPICS = {
    "DariKamar1": "KeHP1",
    "DariKamar2": "KeHP2",
    "DariHP1": "KeKamar1",
    "DariHP2": "KeKamar2",
}

# Callback saat terhubung ke broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("NodeMCU connected successfully!")
    else:
        print("Connection failed with result code", rc)
    # Subscribe ke semua topik dalam daftar TOPICS
    for topic in TOPICS.keys():
        client.subscribe(topic)
        print(f"Subscribed to topic: {topic}")

# Callback saat menerima pesan dari broker
def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode()
        print(f"NodeMCU received: {msg.topic} {payload}")
        if msg.topic in TOPICS:
            forward_topic = TOPICS[msg.topic]
            client.publish(forward_topic, payload)
            print(f"NodeMCU forwarded to {forward_topic}: {payload}")
    except Exception as e:
        print(f"Error processing message: {e}")

# Fungsi untuk menjalankan MQTT client
def run_mqtt_client():
    client = mqtt.Client(client_id="NodeMCU", protocol=mqtt.MQTTv311)
    client.on_connect = on_connect
    client.on_message = on_message

    # Koneksi ke broker
    client.connect(BROKER, PORT, 60)
    client.loop_forever()

# Multithreading untuk NodeMCU
if __name__ == "__main__":
    node_mcu_thread = threading.Thread(target=run_mqtt_client)
    node_mcu_thread.start()
