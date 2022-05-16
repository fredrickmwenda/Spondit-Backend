import json
from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

class NotificationConsumer(AsyncWebsocketConsumer):
    async  def connect(self):
            self.room_name = 'notification'
            self.room_group_name = 'notification_group'

            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()
            self.send(text_data=json.dumps({
                'message': 'Connected to notification channel'
            }))

    async  def disconnect(self, close_code):
            # Leave room group
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )


    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
       
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )


       



    
    # Receive message from room group
    async def notification_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps(
            message
            # When recieving many messages, we need to send a list of messages
            # {
            # 'message': message
            # }
            )
        )

    def notification_send(self,event):
        print('here')
        print(event)
        self.send(text_data=json.dumps({'payload': event.get('value')}))



    # also check if a certain user is requesting for the websocket
    # and send notification to specific users

    

