from xml.etree.ElementInclude import include
from django.urls import path,  re_path
from .views import CurrentUserViewSet, DeviceListView, DisconnectDeviceAPIView, LoginAPIView, UserDevicesAPIView, create_users, history_view, login_view, logout_view, notifications_view, profile,   register_user, home, update_profile, users_device_add, users_device_list, users_list
from django.contrib.auth.views import LogoutView
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('login/', login_view, name="login"),
    # path('register/', register_user, name="register"),
    path('home', home, name="home"),
    
    path("logout/", logout_view, name="logout"),
    path('users/add/', create_users, name='users_add'),
    path('users/list/', users_list, name='users_list'),
    path('users/delete/<int:id>/', users_list, name='users_list'),

    path('user/devices/list', users_device_list, name='users_device_list'),
    path('user/devices/add', users_device_add, name='users_device_add'),
    path('messages', notifications_view, name="messages"),
    path('activitylog', history_view, name="activity_log"),
    
    path('users',CurrentUserViewSet.as_view() , name='users Details'),
    path('devices/all',DeviceListView.as_view() , name='devices Details'),
    path('user/login',LoginAPIView.as_view() , name='user login'),
   # path('devices/all', DeviceAPIView.as_view(), name="all devices" ),
    #connected devices
    path('devices/connected', UserDevicesAPIView.as_view(), name="connected devices" ),
    path('device/disconnect', DisconnectDeviceAPIView.as_view(), name="disconnect device" ),


    #profile
    path('profile/add', profile, name="profile_add"),
    path('profile/edit', update_profile, name="profile_edit"),
    

    # path('', include("devices@urls"))
        # Matches any html file
    # re_path(r'^.*\.*', pages, name='pages'),
  
]