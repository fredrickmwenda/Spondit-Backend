from xml.etree.ElementInclude import include
from django.urls import path,  re_path

from django.contrib.auth.views import LogoutView

# from .views import notifications_view


urlpatterns = [
    # path('notifications', notifications_view, name="notifications"),
    # path('<str:room_name>/', notifications_view, name='notifications'),
]