from django.db import models
from django.utils.encoding import python_2_unicode_compatible

@python_2_unicode_compatible  # only if you need to support Python 2
class ResearchTasks(models.Model):
    task_desc = models.CharField(max_length=500)
    creation_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.task_desc

