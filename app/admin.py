from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Person)
admin.site.register(Channel)
admin.site.register(DirectMessage)
