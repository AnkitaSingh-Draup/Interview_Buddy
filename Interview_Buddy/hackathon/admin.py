from django.contrib import admin
from .models import JobRole
# Register your models here.


class AuthorAdmin(admin.ModelAdmin):
    pass


admin.site.register(JobRole, AuthorAdmin)
