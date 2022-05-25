from math import e
from django.urls import path
from .views import  connect_device, delete_device, device_add, device_list, device_edit, disconnect_device, enableState
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('device/add/', device_add, name='device_add'),
    path('device/list/', device_list, name='device_list'),
    path('device/edit/<str:id>/', device_edit, name='device_edit'),
    path('delete/<int:id>/', delete_device, name='device_delete'),
    # path('<int:id>/delete',device_delete, name='device_delete'),

    # connect a device to a user and mqtt broker
    path('device/connect/<str:id>/', connect_device, name='device_connect'),

    
    # disconnect a device from a user and mqtt broker
    path('device/disconnect/<str:id>/', disconnect_device, name='device_disconnect'),

    #update device enable_1, enable_2, enable_3, and enable_4 states
    path('enableState/<str:id>/', enableState, name='enableState'),



]