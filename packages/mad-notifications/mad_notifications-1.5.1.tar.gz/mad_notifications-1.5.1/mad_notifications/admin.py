from mad_notifications.models import get_device_admin_class, get_device_model, get_email_template_admin_class, get_email_template_model, get_notification_admin_class, get_notification_model, get_user_notification_config_admin_class, get_user_notification_config_model
from django.contrib import admin

# Register your models here.


class UserNotificationConfigAdmin(admin.ModelAdmin):
    list_display = [field.name for field in get_user_notification_config_model()._meta.get_fields()]
    list_filter = ('created_at',)
    ordering = ('-created_at',)


class EmailTemplateAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'slug', 'created_at']
    list_filter = ('created_at',)
    ordering = ('-created_at',)

class DeviceAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'created_at']
    list_filter = ('created_at',)
    ordering = ('-created_at',)
    raw_id_fields = ('user',)

class NotificationAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'title', 'is_read', 'created_at']
    list_filter = ('created_at',)
    ordering = ('-created_at',)
    raw_id_fields = ('user', 'template')


#show admin
userConfig_model = get_user_notification_config_model()
emailTemplate_model = get_email_template_model()
device_model = get_device_model()
notification_model = get_notification_model()

userConfig_admin_class = get_user_notification_config_admin_class()
emailTemplate_admin_class = get_email_template_admin_class()
device_admin_class = get_device_admin_class()
notification_admin_class = get_notification_admin_class()

admin.site.register(userConfig_model, userConfig_admin_class)
admin.site.register(emailTemplate_model, emailTemplate_admin_class)
admin.site.register(device_model, device_admin_class)
admin.site.register(notification_model, notification_admin_class)
