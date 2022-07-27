from django.contrib import admin
from .models import *

# Register your models here.
class HomeWorkAdmin(admin.ModelAdmin):
    list_display= ['subject', 'due']
admin.site.register(Notes)
admin.site.register(HomeWork,HomeWorkAdmin)
admin.site.register(Todo)