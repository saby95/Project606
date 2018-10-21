from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.auth.models import User

#Creating the table for Tasks
@python_2_unicode_compatible  # only if you need to support Python 2
class ResearchTasks(models.Model):
    task_type = models.CharField(max_length=10, blank = True, null=True)
    task_summary = models.CharField(max_length=500, default = 'Enter a single line summary')
    task_desc = models.TextField(default = 'Describe the task')
    creator_id = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True)
    creation_time = models.DateTimeField(auto_now_add=True)
    num_workers = models.PositiveIntegerField(default=1)


    def __str__(self):
        return self.task_summary

#Creating the table for TasksUser junction
@python_2_unicode_compatible
class TaskUserJunction(models.Model):
    CONFIDENCE = (
        (1, 'poor'),
        (2, 'below average'),
        (3, 'average'),
        (4, 'above average'),
        (5, 'good')
    )
    task_id = models.ForeignKey(ResearchTasks, on_delete=models.DO_NOTHING)
    worker_id = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    claim_time = models.DateTimeField(auto_now_add=True)
    answer = models.CharField(max_length=500, blank=True, null=True)
    submission_time = models.DateTimeField(blank=True, null=True)
    comment = models.CharField(max_length=500, blank=True, null=True)
    confidence_level = models.IntegerField(choices=CONFIDENCE, blank=True, null=True)

    def __str__(self):
        return 'TUJ Instance'
