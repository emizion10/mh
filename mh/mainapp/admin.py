from django.contrib import admin
from mainapp.models import Hostel,Student,Warden,Notifications,Fees

# Register your models here.

admin.site.register(Hostel);
admin.site.register(Warden);
admin.site.register(Student);
admin.site.register(Notifications);
admin.site.register(Fees);
