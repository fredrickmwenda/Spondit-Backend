import binascii
from decimal import Decimal
from distutils.command.upload import upload
import os
from django.core.files import File 
from django.db import models
from django.utils.translation import gettext_lazy as _



class Device(models.Model):
    """
    Requests for iot device Gateway
    """
    name = models.CharField(_('Device name'), max_length=60, help_text=_('Enter device name'))
    device_type = models.CharField(max_length=255, blank=True, null=True)
    device_id = models.CharField(max_length=255, blank=True, null=True)
    lane_1 = models.CharField(_('Lane 1'), max_length=20, null=True, blank=True)
    enable_1 = models.BooleanField(_('Activate Lane 1'), default=False, blank=True)
    lane_2 = models.CharField(_('Lane 2'), max_length=20, null=True, blank=True)
    enable_2 = models.BooleanField(_('Activate Lane 2'), default=False, blank=True)
    lane_3 = models.CharField(_('Lane 3'), max_length=20, null=True, blank=True)    
    enable_3 = models.BooleanField(_('Activate Lane 3'), default=False, blank=True)  
    lane_4 = models.CharField(_('lane 4'), max_length=20, null=True, blank=True)
    enable_4 = models.BooleanField(_('Activate Lane 4'), default=False, blank=True)
    lane_5 = models.CharField(_('Lane 5'), max_length=20, null=True, blank=True)
    enable_5 = models.BooleanField(_('Activate Lane 5'), default=False, blank=True)
    lane_6 = models.CharField(_('Lane 6'), max_length=20, null=True, blank=True)
    enable_6 = models.BooleanField(_('Activate Lane 6'), default=False, blank=True)
    lane_7 = models.CharField(_('Lane 7'), max_length=20, null=True, blank=True)   
    enable_7 = models.BooleanField(_('Activate Lane 7'), default=False, blank=True)
    lane_8 = models.CharField(_('Lane 8'), max_length=20, null=True, blank=True)
    enable_8 = models.BooleanField(_('Activate Lane 8'), default=False, blank=True)
    description = models.TextField(_('Description'), blank=True, max_length=255)
    state = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    enable = models.BooleanField(_('Activate'), default=False, blank=True)
    remote_address = models.CharField(_('Ip adresss'), max_length=255,null=True, blank=True)
    pub_date = models.DateTimeField(_('Release date'), auto_now=True)


    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        
     
        super(Device, self).save(*args, **kwargs)

    
class DeviceImages(models.Model):
    device_images = models.ImageField(upload_to= 'static/assets/img',null=True,blank=True)
    feed = models.ForeignKey(Device, on_delete=models.CASCADE)

    # def cache(self):
    #     """Store image locally we just have to  pass URL location"""
    #     if self.device_image:
    #         result = urllib.urlretrieve(self.device_image)
    #         self.photo.save(
    #             os.path.basename(self.device_image),
    #             File(open(result[0], 'rb'))
    #         )
    #         self.save()

    def generate_key(self):
        return binascii.hexlify(os.urandom(12)).decode()
