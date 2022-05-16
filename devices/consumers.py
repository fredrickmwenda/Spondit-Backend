from channels.consumer import AsyncConsumer

#an Mqtt client for the consumers
class MqttConsumer(AsyncConsumer):
    # asynchrows when the websocket is opened
    async def connect(self):
    
        #join mqtt group
        await self.channel_layer.group_add(
            'mqtt',
            self.channel_name
        )

        # Receive message from mqtt group and send to websocket which is subscribing to the group
        await self.channel_layer.send(
            'mqtt',
            {
                'type': 'device_connected',
                'topic': f"chat/{self.room_name}",
                'group': 'mqtt',

            }
        )

        await self.accept()
   
    # Receive message from mqtt group and send to websocket
    async def chat_subscription(self, event):
        message = event['message']
        payload = message['payload']
        topic = message['topic']
        group = message['group']
        print(f"{topic} {payload} {group}")

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message': payload,
            'payload': event['payload'],
            'topic': event['topic']
        }))

    # Receive message from websocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        topic = text_data_json['topic']
        payload = text_data_json['payload']
        group = text_data_json['group']
        print(f"{topic} {message} {group}")

        #send message to mqtt group
        await self.channel_layer.send(
            'mqtt',
            {
                'type': 'mqtt_publish',
                'publish': {
                    'topic': f"chat/{self.room_name}_out",
                    'payload': message,
                    'qos': 0,
                    'retain': False,
                    'group': 'mqtt',


                } 
            }
        )

    # asynchrows when the websocket is closed
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            'mqttgroup',
            self.channel_name
        )
        
    
