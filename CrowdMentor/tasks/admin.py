from django.contrib import admin

from .models import ResearchTasks,TaskUserJunction, Audit

admin.site.register(ResearchTasks)
admin.site.register(TaskUserJunction)
admin.site.register(Audit)