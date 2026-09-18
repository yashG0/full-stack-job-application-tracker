from django.contrib import admin

from applications.models import Application, Contact, StatusHistory

# Register your models here.

admin.site.register(Application)
admin.site.register(StatusHistory)
admin.site.register(Contact)
