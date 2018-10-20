from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.auth.models import User

@python_2_unicode_compatible  # only if you need to support Python 2
class ResearchTasks(models.Model):
    CONFIDENCE = (
        (1, 'poor'),
        (2, 'below average'),
        (3, 'average'),
        (4, 'above average'),
        (5, 'good')
    )

    task_desc = models.CharField(max_length=500)
    creation_time = models.DateTimeField(auto_now_add=True)
    worker_id = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank = True, null=True)
    claim_time =  models.DateTimeField(blank = True, null=True)
    answer = models.CharField(max_length=500, blank = True, null=True)
    submission_time = models.DateTimeField(blank=True, null=True)
    comment = models.CharField(max_length=500, blank = True, null=True)
    confidence_level = models.IntegerField(choices=CONFIDENCE,blank=True, null=True)

    def __str__(self):
        return self.task_desc

