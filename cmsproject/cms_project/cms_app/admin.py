from django.contrib import admin
from .models import  Like ,Post , AccoutUser
# Register your models here.

admin.site.register(Post)
admin.site.register(AccoutUser)
admin.site.register(Like)
