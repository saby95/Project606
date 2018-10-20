from django.forms import ModelForm
from .models import ResearchTasks, TaskUserJunction

class AddTaskForm(ModelForm):
    class Meta:
        model = ResearchTasks
        fields = ['task_summary', 'task_desc', 'num_workers']



class AnswerForm(ModelForm):
    class Meta:
        model = TaskUserJunction
        fields = ['answer', 'comment', 'confidence_level']
