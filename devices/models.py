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
    lane1_name = models.CharField(_('Lane 1 Name'), max_length=20, null=True, blank=True)
    enable_1 = models.BooleanField(_('Activate Lane 1'), default=False, blank=True)
    lane_2 = models.CharField(_('Lane 2'), max_length=20, null=True, blank=True)
    lane2_name = models.CharField(_('Lane 2 Name'), max_length=20, null=True, blank=True)
    enable_2 = models.BooleanField(_('Activate Lane 2'), default=False, blank=True)
    lane_3 = models.CharField(_('Lane 3'), max_length=20, null=True, blank=True)
    lane3_name = models.CharField(_('Lane 3 Name'), max_length=20, null=True, blank=True)
    enable_3 = models.BooleanField(_('Activate Lane 3'), default=False, blank=True)  
    lane_4 = models.CharField(_('lane 4'), max_length=20, null=True, blank=True)
    lane4_name = models.CharField(_('Lane 4 Name'), max_length=20, null=True, blank=True)
    enable_4 = models.BooleanField(_('Activate Lane 4'), default=False, blank=True)
    lane_5 = models.CharField(_('Lane 5'), max_length=20, null=True, blank=True)
    lane5_name = models.CharField(_('Lane 5 Name'), max_length=20, null=True, blank=True)
    enable_5 = models.BooleanField(_('Activate Lane 5'), default=False, blank=True)
    lane_6 = models.CharField(_('Lane 6'), max_length=20, null=True, blank=True)
    lane6_name = models.CharField(_('Lane 6 Name'), max_length=20, null=True, blank=True)
    enable_6 = models.BooleanField(_('Activate Lane 6'), default=False, blank=True)
    lane_7 = models.CharField(_('Lane 7'), max_length=20, null=True, blank=True) 
    lane7_name = models.CharField(_('Lane 7 Name'), max_length=20, null=True, blank=True)
    enable_7 = models.BooleanField(_('Activate Lane 7'), default=False, blank=True)
    lane_8 = models.CharField(_('Lane 8'), max_length=20, null=True, blank=True)
    lane8_name = models.CharField(_('Lane 8 Name'), max_length=20, null=True, blank=True)
    enable_8 = models.BooleanField(_('Activate Lane 8'), default=False, blank=True)
    description = models.TextField(_('Description'), blank=True, max_length=255)
    #latitude and longitude
    lat = models.DecimalField(max_digits=22, decimal_places=16, null=True, blank=True)
    lng = models.DecimalField(max_digits=22, decimal_places=16, null=True, blank=True)

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

    @property
    def has_lane5(self):
        return self.lane_5 is not None and self.lane_5 != ''

    @property
    def has_lane6(self):
        return self.lane_6 is not None and self.lane_6 != ''
    
    @property
    def has_lane7(self):
        return self.lane_7 is not None and self.lane_7 != ''

    @property
    def has_lane8(self):
        return self.lane_8 is not None and self.lane_8 != ''


    
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
