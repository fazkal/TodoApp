from django.shortcuts import render
from django.views.generic.list import ListView
from .models import Task
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = "tasks"
    template_name = "todo/list_task.html"

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)