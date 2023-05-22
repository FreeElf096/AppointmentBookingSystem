from django.contrib import admin
from app.models import *
# Register your models here.

admin.site.register(myCustomUser)
admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Appointment)
