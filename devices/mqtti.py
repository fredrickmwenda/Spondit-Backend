# import json
# import sqlite3
# import time
# from datetime import datetime
# import paho.mqtt.client as mqtt
# import paho.mqtt.publish as publish


# class MqttClient:
#     #create a client instance to connect to the broker via websocket
#     client = mqtt.Client( client_id="mqttx_be44fa7", clean_session=True,protocol=mqtt.MQTTv311, transport="websockets")
#     client.ws_set_options(path="/mqtt", headers=None)
    

#     def __init__(self, host, port):
#         self._host = host
#         self._port = port
#         self.client.on_connect = self._on_connect  
#         self.client.on_message = self._on_message  

#     def connect(self):

#         self.client.connect(self._host, self._port, 60)

#     def disconnect(self):
#         self.client.disconnect()

#     def publish(self, topic, data, qos=0):
#         self.client.publish(topic, data, qos)

#     def subscribe(self, topic, qos=0):
#         self.client.subscribe(topic, qos)

#     def loop(self, timeout=None):
#         if not timeout:
#             self.client.loop_start()
#         else:
#             self.client.loop(timeout)

#     def _on_connect(self, client, userdata, flags, rc):
#         if(rc == 0):
#             print("\nMQTT Connected success!\r\n")
#             client.subscribe('mqtt/msg', 0)
#         else:
#             print("\nMQTT Connected faild!\r\n")

#     def _on_message(self, client, userdata, msg):  
#         if(msg.topic == "mqtt/msg"):
#             data = self._is_json(msg.payload)
#             if(data):
#                 msg_topic_callback(data)
#             else:
#                 print("is not json data")
#         else:
#             print("default message!")

#     def _is_json(self, data):
#         try:
#             msd_data = json.loads(data)
#         except ValueError:
#             return False
#         return msd_data

#     def publish_loop(self):
#         pass


# def msg_topic_callback(data):
#     print(data)
#     print(data['rtc'])

#     # cx = sqlite3.connect("db.sqlite3")
#     # cu = cx.cursor()
#     # save_sql = '''insert into main_msg values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
#     # data = (None, datetime.now(), 223, 444, "00:00:00:01",
#     #         "00:00:00:02", 99, 00, 00, 00, 00, 11)
#     # cu.execute(save_sql, data)
#     # cx.commit()
#     # cx.close()

#     local_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(data['rtc'])))
#     my_msg = msg(None, local_time, int(data['device_sn']), int(data['imei']), data['eth_mac'], data['wifi_mac'],
#                  int(data['temper']), int(data['adc1']), int(data['adc2']), int(data['485']), int(data['lora1']), int(data['lora2']))
#     my_msg.save()


# host = "broker.emqx.io"
# port = 1883
# client = MqttClient(host, port)
# #set the path and headers for the websocket
# client.ws_set_options(path="/mqtt", headers=None)
# # client.ws_set_options(path="/mqtt", headers=None)   # set websocket path
# client.connect()
# client.publish('test-0', '')
# client.loop()


# def mqtt_publish(topic, message):
#     client.publish(topic, message)

# def subscribe_mqtt(topic):
#     client.subscribe(topic)
#     client.loop()

# #disconnect
# def disconnectMqtt():
#     client.disconnect()


# def connectMqtt():
#     client.connect()
#     client.publish('test-k1', '')
#     client.loop()
    


# def mqtt_main():
#     client.connect()
#     client.publish('test-0', '')
#     client.loop()
#     while True:
#         client.publish('test-0', '!')
#         time.sleep(2)


# if __name__ == '__main__':
#     mqtt_main()