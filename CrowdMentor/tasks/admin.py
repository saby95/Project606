from django.contrib import admin

from .models import ResearchTasks,TaskUserJunction

admin.site.register(ResearchTasks)
admin.site.register(TaskUserJunction)