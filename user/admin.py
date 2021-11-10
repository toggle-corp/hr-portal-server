from django.contrib import admin
from user.models.user import User
from user.models.department import Department
from user.models.user_department import UserDepartment

# Register your models here.

admin.site.register(User)
admin.site.register(UserDepartment)
admin.site.register(Department)