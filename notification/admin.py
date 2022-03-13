from django.contrib import admin

# Register your models here.
from notification.models import Notification, EmailNotification

admin.site.register(EmailNotification)