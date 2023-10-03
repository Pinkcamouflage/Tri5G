from django.contrib import admin

# Register your models here.

from .models import Object,BaseStation,Cell,JsonData

admin.site.register(Object)
admin.site.register(BaseStation)
admin.site.register(Cell)
admin.site.register(JsonData)