
from os import access
from re import U
from urllib import response
from django import template
from django.shortcuts import render, redirect
from django.contrib import messages 
from django.contrib.auth.decorators import login_required
from django.contrib.admin.models import LogEntry, DELETION, CHANGE, ADDITION
from django.contrib.contenttypes.models import ContentType
from django.db.models import Sum
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.contrib.auth import authenticate, login
from django.urls import reverse
from django.contrib.auth import get_user_model, logout
from .consumers import NotificationConsumer

from devices.models import Device

from .permissions import IsAdminUser, AdvancedUserManage

from .serializers import DeviceDataSerializer, DeviceSerializer, LoginSerializer, RegistrationSerializer, UserDevicesSerializer, UsersSerializer

from .models import NotificationChannel, UserDevices, UserProfile

from .forms import CreateUserDevice, CreateUsers, LoginForm, ProfileForm,  SignUpForm, User, UserForm


from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from rest_framework.authtoken.models import Token

from .authentication import create_access_token, create_refresh_token

#RefreshToken
from rest_framework_simplejwt.tokens import RefreshToken





# Create your views here.
# User = get_user_model()
def register_user(request):
    msg = None
    success = False

    if request.method == "POST":
        form = SignUpForm(request.POST)
        context ={
            "form" : form
        }
        if form.is_valid():
            print('check')
            form.save()
                     
            return redirect("/login")
        else:
            msg = 'Form is not valid'
    else:
        form = SignUpForm()

    return render(request, "accounts/register.html", {"form": form, "msg": msg, "success": success})

def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")
    form = LoginForm(request.POST or None)
    msg = None
    if request.method == 'POST':
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect("home")
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating the form'

    return render(request, "accounts/login.html", {"form": form, "msg": msg})


def logout_view(request):
    logout(request)
    return redirect("/login")


# After successfull login user is taken to homepage
# @login_required(login_url= "/login/")
def home(request):
    msg = "Not authenticated "
    if request.user.is_authenticated:
        # get all users using the system

        all_users = get_user_model().objects.all().filter(admin__in = [True]).count()
        all_devices = Device.objects.all().count()
        normal_users = get_user_model().objects.all().filter(normal_user__in = [True]).count()
        advanced_users = get_user_model().objects.filter(advanced_user__in = [True]).count()
        active_users = get_user_model().objects.filter(is_active__in = [True]).count()
        notifications = NotificationChannel.objects.all().filter(user_id = request.user.id).count()

        #users connected to devices
        admin_devices = UserDevices.objects.filter(active=True)


        # get count of device_connections for a user using device_connections field
        queryset = UserDevices.objects.filter(user_detail_id = request.user.id)
        user_device_connections = queryset.aggregate(sum=Sum('device_connections')).get('sum')
        #print(f'user_device_connections: {user_device_connections}')

        #produce a chart of the number of devices connected to the user
        #get all devices connected to the user
        queryset = UserDevices.objects.filter(user_detail_id = request.user.id)
        #get the number of devices connected to the user
        user_device_connections = queryset.aggregate(sum=Sum('device_connections')).get('sum')

        
        
        #print(notifications)

        if request.user.staff:
           user_devices = UserDevices.objects.all()
           devices_count = user_devices.count()
        else:
            #check all devices connected to a user which are active
            user_devices = UserDevices.objects.filter(user_detail_id = request.user.id,)
            devices_count = user_devices.count()
            #user_devices = UserDevices.objects.filter(user_detail_id = request.user.id, active=1)

            #get count of devices connected to a user
            #devices_count = user_devices.count()

        

        # 'allusers' = all_users, 'alldevices': all_devices, 'normalusers':normal_users, 'advancedusers': advanced_users , 'activeusers': active_users, 'userdevices': user_devices, 'devicescount': devices_count
        #'devicescount': devices_count,
        return render(request, "home/index.html", {'room': 'broadcast', 'allusers': all_users, 'alldevices': all_devices, 'normalusers':normal_users, 'advancedusers': advanced_users , 
        'activeusers': active_users,    
        'notification_count': notifications,
        'userdevices': user_devices,
        'devices_count': devices_count,
        'user_device_connections': user_device_connections,    
        })
    return render(request, "accounts/login.html") 


@login_required(login_url="/login/")
def notifications_view(request):
    user_notifications = NotificationChannel.objects.all().filter(user_id = request.user.id)
    notifications = NotificationChannel.objects.all().filter(user_id = request.user.id).count()
    return render(request, "home/notifications.html",{'user_notifications': user_notifications, 'notification_count': notifications})


@login_required(login_url="/login/")
def create_users(request):
    msg = None
    success = False
    
    if request.method == "POST":
        form = CreateUsers(request.POST)
        context ={
            "form" : form
        }
        # context['form']= form
        if form.is_valid():
            
            form.save()
            # LogEntry.objects.log_action(
            #     user_id=request.user.id,
            #     content_type_id=1,
            #     object_id=1,
            #     object_repr='User',
            #     action_flag=1,
            #     change_message='User created'
            # )

            msg = "User is created"
            return redirect('/users/list/')
        else:
            msg = 'Form is not valid'
            print(form.errors.as_data())
    else:
        form = CreateUsers()
    
    return render(request, "home/users-add.html", {"form": form, "msg": msg, "success": success})  
    
    
 
@login_required(login_url="/login/")
def users_list(request):
    """
    :param request:
    :return:
    """
    users_list = True
    list = User.objects.all()
    return render(request, "home/users-list.html", locals())

@login_required(login_url="/login/")
def delete_user(request, id):
    user = User.objects.get(id=id)
    user.delete()
    LogEntry.objects.log_action(
        user_id=request.user.id,
        content_type_id=1,
        object_id=1,
        object_repr='User',
        action_flag=1,
        change_message='User deleted'
    )
    return redirect('/users/list')

# Profile management
@login_required(login_url="/login/")
#user profile
def profile(request):
    user = get_user_model().objects.get(id=request.user.id)

    #if user doesnt have a profile, create one
    profile = UserProfile.objects.get_or_create(user=user)
    return render(request, "home/profile.html", {"user": profile})

    # user = UserForm(instance=request.user)
    # #get the user_profile by their id
    # user_profile = ProfileForm(instance=request.user)
    # return render(request, "home/profile.html", {"user": user_profile})


#update profile
def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES,instance=request.user.profile )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            #get the user_profile by their id
            messages.success(request, ('Your profile was successfully updated!'))
            return redirect('profile')
        else:
            messages.error(request, ('Please correct the error below.'))
            print(user_form.errors.as_data())
            print(profile_form.errors.as_data())
    else:
        user_form = UserForm(instance=request.user.profile)
        profile_form = ProfileForm(instance=request.user)
    return render(request, 'home/profile.html', {'user_form': user_form,'profile_form': profile_form})

@login_required(login_url="/login/")
def users_device_add(request):
    msg = None
    success = False
    context_dict={}
    
    if request.method == "POST":
        form = CreateUserDevice(request.POST, instance=request.user)

        if form.is_valid():
            device_name = Device.objects.get(name=form.cleaned_data.get("device_name"))
            #only return devices that user hasnt connected to if connected to all then no vlue is in the dropdown
            UserDevices.objects.create(user_detail= request.user, device_name=device_name, )
            LogEntry.objects.log_action(
                user_id=request.user.pk,
                content_type_id=ContentType.objects.get_for_model(form).pk,
                object_id=form.pk,
                object_repr=str(form.instance),
                action_flag=ADDITION,
                change_message=request.user.full_name + ' has connected to ' + device_name.name,
            )
            return redirect('/home')
        else:
            msg = 'Error validating the form'
            print(msg)
    else:
        form =  CreateUserDevice()
        if request.user.normal_user:
            devices = Device.objects.order_by('id')[:2]
            users = User.objects.filter(id = request.user.id)
            print(users)
        elif request.user.advanced_user:
            devices = Device.objects.all()
            users = User.objects.filter(id = request.user.id)
        else:
            devices = Device.objects.all()
            users = User.objects.all()
        
        # context_dict = {'form': form, 'devices': devices, 'users': users, 'msg': msg, 'success': success}
        context_dict['form'] = form
        context_dict['devices'] = devices
        context_dict['users'] = users
       
    return render(request, "home/user-devices.html", context_dict)



@login_required(login_url="/login/")
def users_device_list(request):
    """
    :param request:
    :return:
    """
    users_list = True
    list = UserDevices.objects.all()
    return render(request, "home/users-device-list.html", locals())



@login_required(login_url="/login/")
def user_device_delete(request, id):
    user_device = UserDevices.objects.get(id=id)
    user_device.delete()
    return redirect('/users/list')    


@login_required(login_url="/login/")
def history_view(request):
    logs = LogEntry.objects.order_by('-action_time')[:20]
    logCount = LogEntry.objects.order_by('-action_time').count()
    return render(request, "home/history.html", {"logs":logs, "logCount":logCount})




# APIViews
#unauthenticated users can access the DeviceListView
class DeviceListView(APIView):
    """
    List all devices, or create a new device.
    """
    # be available to all users
    permission_classes = (IsAuthenticated,)
    serializer_class = DeviceSerializer
    def get(self, request, format=None):
        devices = Device.objects.all()
        serializer = DeviceSerializer(devices, many=True)
        return Response(serializer.data)

class CurrentUserViewSet(APIView):
    #permission_class = (IsAuthenticated)
    queryset = User.objects.all()
    serializer_class = UsersSerializer

def UserAvailable(request):
    if request.method == 'GET':
        specific_users = User.objects.filter(id=request.user.id)
        serializer = UsersSerializer(specific_users)
        return Response(serializer.data)

class RegistrationAPIView(APIView):
    # Allow any user (authenticated or not) to hit this endpoint.
    permission_classes = [IsAdminUser]
    serializer_class = RegistrationSerializer

    def post(self, request):
        user = request.data.get('user', {})

        # The create serializer, validate serializer, save serializer pattern
        # below is common and you will see it a lot throughout this course and
        # your own work later on. Get familiar with it.
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    #serializer_class = LoginSerializer

    def post(self, request):
        # get email and password from request body
        email = request.data.get('email', {})
        password = request.data.get('password', {})

        # check if user exists
        user = User.objects.filter(email=request.data['email']).first()

       # if not user.is_active:
        #    return Response({"error": "User is not active, contact Admin"}, status=status.HTTP_400_BAD_REQUEST)

        if user:
            # check if password is correct
            if user.check_password(request.data['password']):
                # if user is authenticated, then generate access & refresh token
               # create and assign tokens
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)
                refresh_token = str(refresh)
 
                # return response with token
                #return Response({'access_token': access_token, 'refresh_token': refresh_token, 'email': email, 'password': password  }, status=status.HTTP_200_OK)
                response = Response()
                response.set_cookie(key='refreshToken', value=refresh_token, httponly=True)
                #include headers in response
                # headers = {
                #     'Access-Control-Allow-Origin': '*',
                #     'Access-Control-Allow-Headers': 'Content-Type',
                #     'content-disposition': 'attachment; filename="file.csv"',
                # }
                response.data = {
                    'access_token': access_token,
                    'refresh_token': refresh_token,
                    'full_name': user.full_name,
                    'email': user.email,
                    'password': user.password,
                    'normal': user.normal_user,
                    'advanced':user.advanced_user,
                    'id': user.id,
                    #'headers': headers
                    
                }
                return response
            else:
                return Response({'error': 'Invalid credentials, not right password'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Invalid credentials, wrong user'}, status=status.HTTP_400_BAD_REQUEST)
    
# get the devices connected to a user
class UserDevicesAPIView(APIView):
    serializer_class  = UserDevicesSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        # get user id from request body
        user_id = request.data.get('user_id', {})
        # get device_id from request body
        device_id = request.data.get('device_id', {})

       # check if device is connection to user exists
        user_device = UserDevices.objects.filter(user_detail=user_id, device_name=device_id).first()
        if user_device:
            #check if device connection is active
            if user_device.active:
                return Response({'error': 'Device is already connected to user'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                user_device.active = True
                user_device.device_connections += 1
                user_device.save()
                return Response({'success': 'Device is connected to user'}, status=status.HTTP_200_OK)
        else:
            #device does not exist
            return Response({'error': 'Device does not exist'}, status=status.HTTP_400_BAD_REQUEST)


    
class DisconnectDeviceAPIView(APIView):
    permission_class = (IsAuthenticated)
    serializer = DeviceDataSerializer

    def post(self, request):
        user_id = request.data.get('user_id', {})
        device_id = request.data.get('device_id', {})
        # check if device is connection to user exists
        user_device = UserDevices.objects.filter(user_detail=user_id, device_name=device_id).first()
        if user_device:
            #check if device connection is active
            if user_device.active:
                user_device.active = False
                #user_device.device_connections -= 1
                user_device.save()
                return Response({'success': 'Device is disconnected from user'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Device is already disconnected from user'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            #device does not exist
            return Response({'error': 'Device does not exist'}, status=status.HTTP_400_BAD_REQUEST)


#change enable1, enable_2, enable_3 and enable_4 to true or false
class ChangeDeviceStatusAPIView(APIView):
    serializer_class = DeviceSerializer
    permission_class = (IsAuthenticated)
    def post(self, request):
        # get user id from request body     
        enable_1 = request.data.get('enable_1', {})
        enable_2 = request.data.get('enable_2', {})
        enable_3 = request.data.get('enable_3', {})
        enable_4 = request.data.get('enable_4', {})
        
        #use serializer to save data
        serializer = DeviceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

   






        




