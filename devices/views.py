from cmath import pi
import json
from asyncio import transports
from asyncio.windows_events import CONNECT_PIPE_INIT_DELAY
from cgitb import enable
from http import client
from re import M, U
from this import d
from django.apps import apps
from django.core import serializers
from django.contrib import messages 
from django.contrib.auth import authenticate, login
from django.contrib.admin.models import LogEntry, DELETION, CHANGE, ADDITION
from django.contrib.contenttypes.models import ContentType
from django.db.models import F
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from accounts.models import UserDevices
from .forms import DeviceField
from .models import DeviceImages
from devices.forms import DeviceForm
from devices.models import Device
from json import load
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import paho.mqtt.client as mqtt
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages


@login_required(login_url="/login/")
@csrf_exempt
def device_add(request):
    """
    :param request:
    :return:
    """
    device_add = True
    msg_ok = ""
    msg_err = ""

    # context = {'p':p}

    if request.method == 'POST':
        # enable = request.POST['enable',] == 'on'
        form = DeviceForm(request.POST)
        file_image = DeviceField(request.POST or None, request.FILES or None,)          
        files = request.FILES.getlist('device_images')
        if form.is_valid() and file_image.is_valid():
            device_name = form.cleaned_data.get('name')
            device_type = form.cleaned_data.get('device_type')
            device_id = form.cleaned_data.get('device_id')
            lane_1 = form.cleaned_data.get('lane_1')
            enable_1 = form.cleaned_data.get('enable_1')
            lane_2 = form.cleaned_data.get('lane_2')
            enable_2 = form.cleaned_data.get('enable_2')
            lane_3 = form.cleaned_data.get('lane_3')
            enable_3 = form.cleaned_data.get('enable_3')
            lane_4 = form.cleaned_data.get('lane_4')
            enable_4 = form.cleaned_data.get('enable_4')
            description= form.cleaned_data.get('description')
            state = form.cleaned_data.get('state')
            city = form.cleaned_data.get('city')
            #latitude = form.cleaned_data.get('lat')
            #longitude = form.cleaned_data.get('lng')
            enable = form.cleaned_data.get('enable')

            # x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            # if x_forwarded_for:
            #     remote_address = x_forwarded_for.split(',')[-1].strip()
            # else:
            #     remote_address = request.META.get('REMOTE_ADDR') + "&" + request.META.get(
            #         'HTTP_USER_AGENT') + "&" + request.META.get('SERVER_PROTOCOL')
            
            device_save = Device.objects.create(name = device_name, device_type = device_type, device_id = device_id, 
            lane_1 = lane_1, enable_1 = enable_1, lane_2 = lane_2, enable_2 = enable_2, lane_3 = lane_3, enable_3 = enable_3, 
            lane_4 = lane_4, enable_4 = enable_4,  description = description, state = state, city = city,
            # lat = latitude, lng = longitude, 
             enable = enable, 
             #remote_address = remote_address
             )
            


            device_save.save()

            for file in files:
                DeviceImages.objects.create(feed=device_save, device_images=file)
            
            #create a log for the device added
            LogEntry.objects.log_action(
                user_id=request.user.pk,
                content_type_id=ContentType.objects.get_for_model(device_save).pk,
                object_id=device_save.pk,
                object_repr=device_save.name,
                action_flag=ADDITION,
                change_message=_('Added device'),
            )

            msg_ok = "Device added successfully"
            messages.success(request, msg_ok)
            return redirect('device_list')
            
        else:
            print(form.errors)
            msg_err = _(u'Attention! Please correct the errors!')
            messages.error(request, msg_err)


    form = DeviceForm()

    #return with msg_ok and msg_err
    return render(request, 'home/device-add.html', locals())


@login_required(login_url="/login/")
def device_list(request):


    """
    :param request:
    :return:
    """
    device_list = True
    #dont show deleted devices
    list = Device.objects.all()
    #show all userdevices for the user
    user_devices = UserDevices.objects.filter(user_detail_id=request.user)

    context = {'list': list, 'user_devices': user_devices}

    return render(request, "home/device-list.html", context)


@login_required(login_url="/login/")
def device_edit(request, id):
    """
    :param request:
    :param id:
    :return:
    """
    
    val = get_object_or_404(Device, id=id)
    initial = {
        'name': val.name,
        'device_type': val.device_type,
        'device_id': val.device_id,
        'lane_1': val.lane_1,
        'lane_2': val.lane_2,
        'lane_3': val.lane_3,
        'lane_4': val.lane_4,
        'description': val.description,
        'state': val.state,
        'city': val.city,
        #'lat': val.lat,
        #'lng': val.lng,     
    }
    #get the device images
    # device_initial ={
    #     'device_images': val.device_images.all()
    # }



     
    if request.method == 'POST':
        form = DeviceForm(request.POST, instance=val)
        file_image = DeviceField(request.POST or None, request.FILES or None,)
        files = request.FILES.getlist('device_images')
        if form.is_valid() and file_image.is_valid():
            print('here')
            device_name = form.cleaned_data.get('name')
            print(device_name)
            device_type = form.cleaned_data.get('device_type')
            device_id = form.cleaned_data.get('device_id')
            lane_1 = form.cleaned_data.get('lane_1')
            enable_1 = form.cleaned_data.get('enable_1')
            lane_2 = form.cleaned_data.get('lane_2')
            enable_2 = form.cleaned_data.get('enable_2')
            lane_3 = form.cleaned_data.get('lane_3')
            enable_3 = form.cleaned_data.get('enable_3')
            lane_4 = form.cleaned_data.get('lane_4')
            enable_4 = form.cleaned_data.get('enable_4')
            description= form.cleaned_data.get('description')
            state = form.cleaned_data.get('state')
            city = form.cleaned_data.get('city')
            latitude = form.cleaned_data.get('lat')
            longitude = form.cleaned_data.get('lng')
            enable = form.cleaned_data.get('enable')
            print(enable)

            val.name = device_name
            val.device_type = device_type
            val.device_id = device_id
            val.lane_1 = lane_1
            val.enable_1 = enable_1
            val.lane_2 = lane_2
            val.enable_2 = enable_2
            val.lane_3 = lane_3
            val.enable_3 = enable_3
            val.lane_4 = lane_4
            val.enable_4 = enable_4
            val.description = description
            val.state = state
            val.city = city
            #val.lat = longitude
            #val.lng = latitude
            val.enable = enable
            #get the value of images
            #val.device_images = file_image.cleaned_data.get('device_images')    

            #devices port address
            # x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            # if x_forwarded_for:
            #     f.remote_address = x_forwarded_for.split(',')[-1].strip()
            # else:
            #     f.remote_address = request.META.get('REMOTE_ADDR') + "&" + request.META.get(
            #         'HTTP_USER_AGENT') + "&" + request.META.get('SERVER_PROTOCOL') 
             
            #save the device
            check = Device.objects.update(
                name=device_name, device_type=device_type, device_id=device_id, 
            lane_1=lane_1, enable_1=enable_1, lane_2=lane_2, enable_2=enable_2, lane_3=lane_3,
             enable_3=enable_3, lane_4=lane_4, enable_4=enable_4, description=description, state=state, 
            city=city, 
            # lat=latitude, lng=longitude, 
             enable=enable)
            

            

            # if images are not changed
            if not files:
                #update the device
                val.save()
                #create a log for the device updated
                LogEntry.objects.log_action(
                    user_id=request.user.pk,
                    content_type_id=ContentType.objects.get_for_model(val).pk,
                    object_id=val.pk,
                    object_repr=val.name,
                    action_flag=CHANGE,
                    change_message=_('Updated device'),
                )

                msg_ok = "Device updated successfully"
                messages.success(request, msg_ok)
                return redirect('device_list')
            #if images are changed
            else:
                for f in files:
                    #update the images
                    DeviceImages.objects.update_or_create(device=val, defaults={'device_images': f})
                    #create a log for the device and images updated
                    LogEntry.objects.log_action(
                        user_id=request.user.pk,
                        content_type_id=ContentType.objects.get_for_model(val).pk,
                        object_id=val.pk,
                        object_repr=val.name,
                        action_flag=CHANGE,
                        change_message=_('Updated device and images'),
                    )

                    msg_ok = "Device updated successfully"
                    messages.success(request, msg_ok)
                    return redirect('device_list')    
        else:
            msg_err = _(u'Attention! Please correct the errors!')
            messages.error(request, msg_err)

            #print(form.errors + file_image.errors)

            form = DeviceForm(instance=val, initial=initial)
            #file_image = DeviceField(initial=device_initial)
    return render(request, "home/device-edit.html", locals(), )


def delete_device(request, id):
    device = Device.objects.get(id=id)
    device.delete()
    LogEntry.objects.log_action(
        user_id=request.user.pk,
        content_type_id=ContentType.objects.get_for_model(device).pk,
        object_id=device.pk,
        object_repr=device.name,
        action_flag=DELETION,
        change_message=_('Deleted device'),
    )
    return redirect('/device/list')


@login_required(login_url="/login")
#connect device to mqtt
def connect_device(request, id):
    #if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method=='POST':
    channel_layer = get_channel_layer()
    if request.method=='POST':
        device = Device.objects.get(id=id)

        # build a connection between device using device_id and user_id
        # if the connection is not exist, create a new one
        if not UserDevices.objects.filter(user_detail=request.user, device_name=device).exists():
       
            #initially set device_connection to 
            device_connection = 1
            UserDevices.objects.create(user_detail=request.user, device_name=device, device_connections=device_connection, 
        
            )
            
            #connect to MQTT broker
           #A check if mqtt is on or not
            connect_mqtt()
            msg_ok = "Device connected successfully"
            messages.success(request, msg_ok)
            #create a log device connected
            LogEntry.objects.log_action(
                user_id=request.user.pk,
                content_type_id=ContentType.objects.get_for_model(device).pk,
                object_id=device.pk,
                object_repr=device.name,
                action_flag=ADDITION,
                change_message=_('Connected device' + device.name),
            )
            

            data = {'status':'success'}
            return HttpResponse(data, status=200,)
        else:

            # if the connection is active, do nothing
            if UserDevices.objects.get(user_detail=request.user, device_name=device).active:
                #show the message that the device is already connected
                msg_err = _(u'Attention! The device is already connected!')
                messages.error(request, msg_err)
                return redirect('device_list')
            # if the connection is not active, change the connection status to active
            else:
                #Iif the connection does not exist, update the connection status to active and increase the connection by 1
                device =UserDevices.objects.get(user_detail=request.user, device_name=device)
                device.device_connections += 1
                device.active = True

                #update the connection
                device.save()

                #call method to connect to MQTT broker
                connect_mqtt()
                #if connection is successful, show the message that the device is connected to mqtt
                msg_ok = _(u'Attention! The device is connected to mqtt!')
                messages.success(request, msg_ok)


            

                #create a log device has been reconnected
                LogEntry.objects.log_action(
                    user_id=request.user.pk,
                    content_type_id=ContentType.objects.get_for_model(device).pk,
                    object_id=device.pk,
                    object_repr=device.device_name.name,
                    action_flag=CHANGE,
                    change_message=_('Reconnected device' + device.device_name.name),
                )
        
        msg_ok = "Device connected successfully"
        messages.success(request, msg_ok)


        data = {'status':'success'}
        return JsonResponse(data, status=200)
    
            
    else:
        data = {'status':'cant connect'}
        return JsonResponse(data, status=400)


#disconnect device from mqtt
@login_required(login_url="/login")
def disconnect_device(request, id):
    
    if request.method=='POST':
        channel_layer = get_channel_layer()
        device = Device.objects.get(id=id)
        # print('state')
        # check if the user has the device
        if UserDevices.objects.filter(user_detail=request.user, device_name=device).exists():
            # if the connection is active, deactivate the connection
            if UserDevices.objects.get(user_detail=request.user, device_name=device).active:
                UserDevices.objects.filter(user_detail=request.user, device_name=device).update(active=False)
                
                disconnect_mqtt()
                #create a log for the device disconnected
                LogEntry.objects.log_action(
                    user_id=request.user.pk,
                    content_type_id=ContentType.objects.get_for_model(device).pk,
                    object_id=device.pk,
                    object_repr=device.name,
                    action_flag=CHANGE,
                    change_message=_('Disconnected device'),
                )
                data = {'status':'success'}
                return JsonResponse(data, status=200)
            # if the connection is not active, do nothing
            else:
                return JsonResponse({'status':'error'}, status=400)
        # if the user doesn't have the device, do nothing
        else:
            msg_error = _(u'Attention! The device is not connected!')
            messages.error(request, msg_error)
            pass
    else:
        data = {'status':'cant connect'}
        return JsonResponse(data, status=400)


@login_required(login_url="/login")
@csrf_exempt
#receive ajax request when enable_1, enable_2, enable_3 and enable_4 are changed
def enableState(request, id):
    if request.is_ajax() and request.method == 'POST':
        
        device = Device.objects.get(id=id)
    
        #get the json
        #get enable_1, enable_2, enable_3, enable_4 data from the json
        enable_1 =  json.loads(request.POST.get('checkData[enable_1]'))
        enable_2  = json.loads(request.POST.get('checkData[enable_2]'))
        enable_3  = json.loads(request.POST.get('checkData[enable_3]'))
        enable_4  = json.loads(request.POST.get('checkData[enable_4]'))

        print(enable_1, enable_2, enable_3, enable_4)

        #update the enable_1, enable_2, enable_3 and enable_4 in the database
        Device.objects.filter(id=id).update(enable_1=enable_1, enable_2=enable_2, enable_3=enable_3, enable_4=enable_4)

       #check if enable_1 value is true
        if enable_1:
            #if enable_1 is true, send a message to the mqtt broker
            #send the message to the mqtt broker
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                'receive',
                {
                    'type': 'mqtt_message',
                    'message': '{"device_id":'+ str(id) +', "enable_1":'+ str(enable_1) +'}'
                }
            )
        elif enable_2:
            #if enable_2 is true, send a message to the mqtt broker
            #send the message to the mqtt broker
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                'receive',
                {
                    'type': 'mqtt_message',
                    'message': '{"device_id":'+ str(id) +', "enable_2":'+ str(enable_2) +'}'
                }
            )
        elif enable_3:
            #if enable_3 is true, send a message to the mqtt broker
            #send the message to the mqtt broker
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                'receive',
                {
                    'type': 'mqtt_message',
                    'message': '{"device_id":'+ str(id) +', "enable_3":'+ str(enable_3) +'}'
                }
            )

        elif enable_4:
            #if enable_4 is true, send a message to the mqtt broker
            #send the message to the mqtt broker
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                'receive',
                {
                    'type': 'mqtt_message',
                    'message': '{"device_id":'+ str(id) +', "enable_4":'+ str(enable_4) +'}'
                }
            )


  

 


        # #create a log for the device enable_1, enable_2, enable_3 and enable_4 changed
        LogEntry.objects.log_action(
            user_id=request.user.pk,
            content_type_id=ContentType.objects.get_for_model(device).pk,
            object_id=device.pk,
            object_repr=device.name,
            action_flag=CHANGE,
            change_message=_('An Enable has been changed'),
        )

        data = {'status':'success'}
        return HttpResponse(data, status=200)



    else:
        data = {'status':'error'}
        return HttpResponse(data, status=400)


#connect device to mqtt
topic = 'chat/mqtt'
#an array of topics
#topics = ['chat/mqtt1', 'chat/mqtt2', 'chat/mqtt3', 'chat/mqtt4']
topic_enable = 'chat/enable'
broker = 'broker.emqx.io'
port = 8083
client_id = 'mqttx_07c399d2'
client_conn = mqtt.Client(client_id, transport='websockets')


def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to broker")
            client.subscribe(topic)
        else:
            print("Connection failed", rc)

    client_conn.connect(broker, port, 60)
    client_conn.loop_start()
    return client_conn

def disconnect_mqtt():
    #check if the client is connected
    if client_conn.is_connected():
        client_conn.disconnect()
        print("Disconnected from broker")
        #client_conn.loop_stop()

# subscribe to a topic in topics array
def subscribe_mqtt(topics):
    #check if the client is connected
    if client_conn.is_connected():
        for topic in topics:
            client_conn.subscribe(topic)
            print("Subscribed to topic", topic)
    else:
        print("Client is not connected")
    
# unsubscribe to a topic in topics array
def unsubscribe_mqtt(topics):
    #check if the client is connected
    if client_conn.is_connected():
        for topic in topics:
            client_conn.unsubscribe(topic)
            print("Unsubscribed to topic", topic)
    else:
        print("Client is not connected")


# def connect_mqtt():
#     topic = "chat/device"
#     broker = 'broker.emqx.io'
#     port = 8083
#     topic = "python/mqtt"
#     client_id ="mqttx_0b0b748c"
#     #connect to mqtt broker
#     def on_connect(client, userdata, flags, rc):
#         if rc == 0:
#             print("Connected to MQTT Broker!")
#             client.subscribe(topic)
#         else:
#             print("Failed to connect, return code %d\n", rc)
#     client = mqtt.Client(client_id, transport='websockets')
#     client.on_connect = on_connect
#     client.connect(broker, port, 60)
#     print("Connecting to MQTT Broker")
#     client.loop_start()
#     return client

#disconnect device from mqtt
# def disconnect_mqtt():
#     if client.is_connected():
#         client.disconnect()
#         print("Disconnected from MQTT Broker")







def export(request, model):
    """
    :param request:
    :return:
    """
    model = apps.get_model(app_label=model + 's', model_name=model)

    data = serializers.serialize(request.GET['format'], model.objects.all()[:100])

    return JsonResponse({'response_data': data})

