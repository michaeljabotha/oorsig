from django.contrib import admin

from .models import Monitor, Result

# Register your models here.
class MonitorAdmin(admin.ModelAdmin):
    list_display = ("__str__", "name", "url", "interval")

class ResultAdmin(admin.ModelAdmin):
    list_display = ("__str__", "monitor", "status", "rtt")

admin.site.register(Monitor, MonitorAdmin)
admin.site.register(Result, ResultAdmin)