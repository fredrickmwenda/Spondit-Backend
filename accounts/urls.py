from xml.etree.ElementInclude import include
from django.urls import path,  re_path
from .views import ChangeDeviceStatusAPIView, CurrentUserViewSet, DeviceListView, DisconnectDeviceAPIView, ChangeDeviceLanesAPIView, LoginAPIView, UserDevicesAPIView, SendNotificationAPIView, create_users, edit_users, history_view, login_view, logout_view, notifications_view, profile,   register_user, home, update_profile, users_device_add, users_device_list, users_list, password_reset_request
from django.contrib.auth.views import LogoutView
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('login/', login_view, name="login"),
    # path('register/', register_user, name="register"),
    path('home', home, name="home"),   
    path("logout/", logout_view, name="logout"),
    path('users/add/', create_users, name='users_add'),
    path('users/list/', users_list, name='users_list'),
    path('users/edit/<str:id>/', edit_users, name='edit_users'),
    path('users/delete/<int:id>/', users_list, name='users_list'),
    path('user/devices/list', users_device_list, name='users_device_list'),
    path('user/devices/add', users_device_add, name='users_device_add'),
    path('messages', notifications_view, name="messages"),
    path('activitylog', history_view, name="activity_log"),    
    path('users',CurrentUserViewSet.as_view() , name='users Details'),

    #apis
    path('devices/all',DeviceListView.as_view() , name='devices Details'),
    path('user/login',LoginAPIView.as_view() , name='user login'),
    #connected devices
    path('device/connection', UserDevicesAPIView.as_view(), name="connected devices" ),
    path('device/disconnection', DisconnectDeviceAPIView.as_view(), name="disconnect device" ),
    path('device/change-state',ChangeDeviceStatusAPIView.as_view(), name="change device state" ),
    path('device/lane',ChangeDeviceLanesAPIView.as_view(), name='change device lane' ),

    #notifications
    path('user/notifications', SendNotificationAPIView.as_view(), name='user notifications'),




    #profile
    path('profile/add', profile, name="profile_add"),
    path('profile/edit', update_profile, name="profile_edit"),


   path("password_reset", password_reset_request, name="password_reset")    
   
 



]