
import random
import time

from paho.mqtt import client as mqtt_client


C
# generate client ID with pub prefix randomly
#client_id = f'python-mqtt-{random.randint(0, 1000)}'
client_id = 'mqttx_0b0b748c'
username = 'fred'
password = 'fredm12o'


def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
            client.subscribe(topic, {'qos': 0})
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id, transport='websockets')
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def publish(client):
    msg_count = 0
    while True:
        time.sleep(1)
        msg = f"messages: {msg_count}"
        result = client.publish(topic, msg)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")
        msg_count += 1

def disconnect(client):
    client.disconnect()
    print("Disconnected from MQTT Broker!")




# def run():
#     client = connect_mqtt()
#     client.loop_start()
#     publish(client)


# if __name__ == '__main__':
#     run()