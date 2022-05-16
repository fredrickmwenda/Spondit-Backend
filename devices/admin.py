from django.contrib import admin
from devices.models import Device

class DeviceAdmin(admin.ModelAdmin):
    """
    """
    list_display = ('id', 'name',  'enable', 'remote_address')


admin.site.register(Device, DeviceAdmin)
