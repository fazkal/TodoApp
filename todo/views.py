from django.shortcuts import render
from django.views.generic.list import ListView
from .models import Task
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import (
    CreateView,
    UpdateView,
    DeleteView,
)

# Create your views here.

class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = "tasks"
    template_name = "todo/list_task.html"

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)
    
class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ["title"]
    success_url = reverse_lazy("task_list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)