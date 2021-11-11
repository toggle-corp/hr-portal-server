from django.contrib import admin
from apps.user.models import User, UserDepartment, Department

# Register your models here.

admin.site.register(User)
admin.site.register(UserDepartment)
admin.site.register(Department)
