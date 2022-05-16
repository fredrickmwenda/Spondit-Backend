from cgitb import text
# from celery import shared_task, Celery, states
# from celery.exceptions import Ignore
from channels.layers import get_channel_layer
from django.conf import settings
from django.core.mail import send_mail
from asgiref.sync import async_to_sync
from .models import NotificationChannel

import json
import asyncio

def send_notification(self, data):
    try:
        # notification = NotificationChannel.objects.get(pk=data['notification_id'])
        notification = NotificationChannel.objects.filter(id=int[data])
        if len (notification) > 0:
            notification = notification[0]
            channel_layer = get_channel_layer()
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(channel_layer.group_send()(
                "notifications",
                {
                    "type": "notification_message",
                    "message": json.dumps({
                        "notification_id": notification.id,
                        "title": notification.title,
                        "message": notification.message,
                        "created_at": notification.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                    })
                }

            ))

            notification.sent = True
            notification.save()
        else:
            self.update_state(meta={'error': 'Notification not found'})
            
    except Exception as e:
        self.update_state( meta={'error': str(e)})
        

        
        # data = json.loads(data)

# def send_notification(self, notification_id):
    
#     try:
#         # notification = NotificationChannel.objects.get(id=notification_id)
#         notification = NotificationChannel.objects.filter(id=int[data])
#         channel_layer = get_channel_layer()
#         async_to_sync(channel_layer.group_send)(
#             "notifications",
#             {
#                 "type": "notification.send",
#                 "text": json.dumps({
#                     "title": notification.title,
#                     "message": notification.message,
#                     "created_at": notification.created_at.strftime("%Y-%m-%d %H:%M:%S"),
#                     "sent": notification.sent,
#                     "is_read": notification.is_read,
#                     "is_deleted": notification.is_deleted,
#                 })
#             }
#         )
#         notification.sent = True
#         notification.save()
#     except SoftTimeLimitExceeded:
#         self.update_state(state=states.FAILURE, meta={'time': 'SoftTimeLimitExceeded'})
#     except NotificationChannel.DoesNotExist:
#         self.update_state(state=states.FAILURE, meta={'time': 'NotificationChannel.DoesNotExist'})
#     except Exception as e:
#         self.update_state(state=states.FAILURE, meta={'time': str(e)})
#     finally:
#         return


