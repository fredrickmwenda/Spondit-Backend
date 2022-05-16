
# from curses.ascii import SUB
import json
import threading
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

SUB_TOPIC = ("lane1/msg", "lane2/msg", "lane3/msg", "lane4/msg")
RECONNECT_TIME = 5


class MqttClient(threading.Thread):
    #create a client instance to connect to the broker via websocket
    client = mqtt.Client( client_id="mqttx_be44fa7", clean_session=True,protocol=mqtt.MQTTv311, transport="websockets")
    #client = mqtt.Client(client_id="mqttx_07c399d2", clean_session=True,protocol=mqtt.MQTTv311)
    #client.ws_set_options(path="/mqtt", headers=None)

    def __init__(self, host, port, topic, data, qos=0):
        threading.Thread.__init__(self)
        self._host = host
        self._port = port
        self._topic = topic
        self._data = data
        self._qos = qos

    def run(self):
        self.client.connect(self._host, self._port, 60)
        self.client.publish(self._topic, self._data, self._qos)
        self.client.disconnect()
    
    #set path and headers for websocket
    def ws_set_options(self, path, headers):
        self.client.ws_set_options(path, headers)

    def publish(self, topic, data, qos=0):
        self.client.publish(topic, data, qos)

    def subscribe(self, topic, qos=0):
        self.client.subscribe(topic, qos)

    def loop(self, timeout=None):
        if not timeout:
            self.client.loop_start()
        else:
            self.client.loop(timeout)

    def connect(self):
        self.client.connect(self._host, self._port, 60)

    def _on_connect(self, client, userdata, flags, rc):
        if(rc == 0):
            print("\nMQTT Connected success!\r\n")
            client.subscribe('mqtt/msg', 0)
        else:
            print("\nMQTT Connected faild!\r\n")
        
        for topic in SUB_TOPIC:
            self.client.subscribe(topic, 0)
    
    def _on_message(self, client, userdata, msg):
        if(msg.topic == "mqtt/msg"):
            data = self._is_json(msg.payload)
            if(data):
                msg_topic_callback(data)
            else:
                print("is not json data")
        else:
            print("default message!")

    def _is_json(self, data):
        try:
            msd_data = json.loads(data)
        except ValueError:
            return False
        return msd_data
    
    def publish_loop(self):
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        self.client.connect(self._host, self._port, 60)
        self.client.loop_forever()

    def disconnect(self):
        self.client.disconnect()


client = MqttClient("broker.emqx.io", 1883, "mqtt/msg", "hello world")
# start connection
client.connect()
client.publish_loop()


#start connection in the views \
def connect_mqtt():
    client = MqttClient("broker.emqx.io", 1883, "mqtt/msg", "hello world")
    #call the path and headers
    client.ws_set_options("/mqtt", None)
    # start connection
    client.connect()
    client.publish_loop()

# def create_connection(host, port):
#     try:
#         cx = sqlite3.connect("db.sqlite3")
#         return cx
#     except Error as e:
#         print(e)
#     return None

def msg_topic_callback(data):
    print(data)
    print(data['rtc'])
    # cx = sqlite3.connect("db.sqlite3")





    



