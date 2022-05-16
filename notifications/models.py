from django.db import models
from django.dispatch import receiver
# from django_celery_beat.models import PeriodicTask,  CrontabSchedule
import json

# Create your models here.
class NotificationChannel(models.Model):
    title = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField()
    sent = models.BooleanField(default=False)
    is_read = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-created_at']

# Signals 
# @receiver(models.signals.post_save, sender=NotificationChannel)
# def send_notification(sender, instance, created, **kwargs):
#     # Dynamic task using celery beat
#     if created:
#         # Send notification to the user
#         schedule, created = CrontabSchedule.objects.get_or_create(
#             minute=instance.created_at.minute,
#             hour=instance.created_at.hour, 
#             day_of_week=instance.created_at.weekday(),
#             day_of_month=instance.created_at.day,
#             month_of_year=instance.created_at.month)
#         task = PeriodicTask.objects.create(
#             crontab=schedule, 
#             name='broadcast-notification-'+str(instance.id), 
#             task='notifications.tasks.send_notification', 
#             args=json.dumps(instance.id),
#             # kwargs=json.dumps({instance.id})
#             )
        
#         instance.sent = True
#         instance.save()
    

