from django.contrib import admin

from config.config import Config
from .models import *


class TaskManager(admin.ModelAdmin):
    fields = ('title', 'summary', 'level', 'group_id', 'location_id', 'status', 'price', 'cycle', "begin_time", "finish_time", 'cycle_unit')
    list_display = ('title', 'summary', 'price')
    search_fields = ('title', "summary")
    list_per_page = 20


class TaskGroupManager(admin.ModelAdmin):
    fields = ('title', 'description',)
    list_display = ('title', 'description',)
    search_fields = ('title', 'description',)
    list_per_page = 20


class TaskAppointManager(admin.ModelAdmin):
    fields = ('task', 'user', 'is_attend', 'leave_reason')
    list_display = ('id', 'task', 'user')
    list_per_page = 20


admin.site.register(Task, TaskManager)
admin.site.register(TaskGroup, TaskGroupManager)
admin.site.register(TaskAppoint, TaskAppointManager)

# admin.site.site_header = Config.getIns().get('main', 'app_name')
# admin.site.site_title = Config.getIns().get('main', 'app_name')
