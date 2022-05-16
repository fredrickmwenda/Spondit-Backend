"""
ASGI config for channels_celery_project project.
It exposes the ASGI callable as a module-level variable named ``application``.
For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os
import django
from channels.routing import ProtocolTypeRouter, URLRouter, ChannelNameRouter
from django.core.asgi import get_asgi_application

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'channels_celery_project.settings', )
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'IOTManager.settings' )
django.setup()

#from channels.auth import AuthMiddleware, AuthMiddlewareStack
# from accounts.routing import websocket_urlpatterns
from devices.consumers import MqttConsumer
# from chanmqttproxy import MqttConsumer


# from notifications.routing import websocket_urlpatterns


# Enable the Django channel layer
application = ProtocolTypeRouter({
    
    "http": get_asgi_application(),
    # AuthMiddlewareStack is a wrapper for the default AuthMiddlewareStack
    # that adds the ability to pass a custom authentication backend.
    # And check which user is basically requesting for the websocket
    # and also send notification to specific users
    # "websocket": AuthMiddlewareStack(        
    #     URLRouter(
    #         websocket_urlpatterns
    #     )
  
    # ),

    #"mqtt": MqttConsumer().as_asgi(),
    "channel": ChannelNameRouter(
        {
            "mqtt": MqttConsumer(),
        }
    )

    # "websocket": AuthMiddlewareStack(
    #     HandleRouteNotFoundMiddleware(
    #         URLRouter(
    #             websocket_urlpatterns
    #         )
    #     )
    # ),
    # 'channel': router,
})