import json
from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)

from devices.models import Device
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.core.validators import MaxValueValidator
from django.db.models.signals import post_save

from asgiref.sync import async_to_sync,sync_to_async
from channels.layers import get_channel_layer


class UserManager(BaseUserManager): 
    def create_user(self, email, full_name, password=None, is_staff=False, is_admin=False, is_normaluser=False, is_advanceduser=False, is_active=True,):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')
        
        if not password:
            raise ValueError('Users must have a password')

        if not full_name:
            raise ValueError("User must have a full name")

        user_obj = self.model(            
            email=self.normalize_email(email),
            full_name=full_name,          
        )
        
        
        user_obj.set_password(password)
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.normaluser = is_normaluser
        user_obj.advanceduser = is_advanceduser
        user_obj.active = is_active
        user_obj.save(using=self._db)
        return user_obj

    def create_customuser(self, email, full_name, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email,
            full_name,
            password=password,
        )
        user.staff = True
        user.full_name = full_name
        user.save(using=self._db)
        return user

    def create_superuser(self, email,  full_name,  password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            full_name,
            password=password,
        )
        user.full_name = full_name
        user.staff = True
        user.admin = True
        user.active = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    full_name = models.CharField(max_length=255,blank=True, null=True)
    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False) # a admin user; non super-user
    admin = models.BooleanField(default=False) # a superuser
    normal_user = models.BooleanField(default=False)
    advanced_user = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now=True)
 
    # notice the absence of a "Password field", that is built in.
    objects     =   UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name'] # Email & Password are required by default.

    def get_full_name(self):
        # The user is identified by their full_name
        if self.full_name:
            return self.full_name
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email
    
    # def set_avatar(self):
    #     _avatar = self.avatar
    #     if not _avatar:
    #         self.avatar="static/assets/img/avatars/avatar.png"

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True



    @property
    def is_staff(self):
        "Is the user a custom admin?"
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin


    @property
    def is_normaluser(self):
        "Is the user a admin member?"
        return self.normal_user

    @property
    def is_advanceduser(self):
        "Is the user a admin member?"
        return self.advanced_user

    @property
    def token(self):
        """
        Allows us to get a user's token by calling `user.token` instead of
        `user.generate_jwt_token().
        """
        return self._generate_jwt_token()

class AllUsers():
    def all_users(self):
        user = get_user_model()
        user.objects.all()

class UserDevices(models.Model):
    user_detail = models.ForeignKey(settings.AUTH_USER_MODEL, default=False, on_delete=models.CASCADE, related_name='user_detail')   
    device_name = models.ForeignKey(Device, default=False,  on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    issue_date = models.DateTimeField(_('Release date'), auto_now=True)
    device_connections = models.IntegerField(default=0)
    time_connected = models.DateTimeField(_('Time connected'), auto_now=True, null=True, blank=True)
    remote_address = models.CharField(max_length=255, blank=True, null=True)

    #active
    def active_device(self):
        return self.filter(active=True)

    #inactive
    def inactive_device(self):
        return self.filter(active=False)

     #calculate time connected (in minutes)
     #get the time the device was connected
   

     



    #device connections

        #set device connection to  0


    


    



    def __str__(self):
        return self.device_name.name

    





    

    class Meta:
        ordering = ['-issue_date']

    




class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile',default=False)   
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to ='static/assets/img', blank=True, null=True)
    phone_number = models.IntegerField(validators=[MaxValueValidator(12)])
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    zip_code = models.IntegerField(validators=[MaxValueValidator(12)], blank=True, null=True)
    bio = models.TextField(max_length=255, blank=True, null=True)
    facebook = models.CharField(max_length=255, blank=True, null=True)
    twitter = models.CharField(max_length=255, blank=True, null=True)
    google_plus = models.CharField(max_length=255, blank=True, null=True)
    linkedin = models.CharField(max_length=255, blank=True, null=True)
    github = models.CharField(max_length=255, blank=True, null=True)
    instagram = models.CharField(max_length=255, blank=True, null=True)
    youtube = models.CharField(max_length=255, blank=True, null=True)
    vimeo = models.CharField(max_length=255, blank=True, null=True)
    pinterest = models.CharField(max_length=255, blank=True, null=True)
    tumblr = models.CharField(max_length=255, blank=True, null=True)
    dribbble = models.CharField(max_length=255, blank=True, null=True)
    behance = models.CharField(max_length=255, blank=True, null=True)
    reddit = models.CharField(max_length=255, blank=True, null=True)
    flickr = models.CharField(max_length=255, blank=True, null=True)
    website = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return str(self.user.email) + ' Profile'        

    def __unicode__(self):
        return '%s' %(self.user)

    def create_profile(sender, **kwargs):
        if kwargs["created"]:
            user_profile = UserProfile.objects.create(user=kwargs["instance"])
    post_save.connect(create_profile, sender=User)

class NotificationChannel(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField()
    sent = models.BooleanField(default=False)
    is_read = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # if not self.id:
        #     self.created_at = timezone.now()
        print('save called')
        channel_layer = get_channel_layer()
        notification_objs =NotificationChannel.objects.all().count()
        data = {'count': notification_objs, 'current_notification': self.message, 'title': self.title}
        async_to_sync(channel_layer.group_send)('notification', {
            'type': 'notification_send',
            'value': json.dumps(data)
        })
        super(NotificationChannel, self).save(*args, **kwargs)
        # return super(NotificationChannel, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-created_at']


# class msg(models.Model):
#     """ Mqtt message model """
#     time = models.DateTimeField(null=False)
#     sn = models.IntegerField(null=False)
#     imei = models.IntegerField(null=False)
#     eth_mac = models.CharField(max_length=20, null=False)
#     wifi_mac = models.CharField(max_length=20, null=False)
#     temper = models.IntegerField(null=False)
#     adc1 = models.SmallIntegerField(null=False)
#     adc2 = models.SmallIntegerField(null=False)
#     rs485 = models.SmallIntegerField(null=False)
#     lora1 = models.SmallIntegerField(null=False)
#     lora2 = models.SmallIntegerField(null=False)

#     class Meta:
#             ordering = ['time']
