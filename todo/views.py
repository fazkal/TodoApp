from django.shortcuts import redirect
from django.views.generic.list import ListView
from .models import Task
from accounts.models import Profile
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.edit import (
    CreateView,
    UpdateView,
    DeleteView,
)
from django.views import View
from .forms import TaskUpdateForm

# Create your views here.

class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = "tasks"
    template_name = "todo/task_form.html"

    #def get_queryset(self):
        #return self.model.objects.filter(user=self.request.user)
    
    def get_queryset(self):

         # Get the user's profile
        try:
            user_profile = Profile.objects.get(user=self.request.user)
        except Profile.DoesNotExist:
            # Handle the case where the user doesn't have a profile
            # For example, create a new profile or return an empty queryset
            return Task.objects.none()  # Return an empty queryset

        # Filter tasks by the user's profile
        return self.model.objects.filter(user=user_profile)

class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ["title"]
    success_url = "/"

    def form_valid(self, form):
        #form.instance.user = self.request.user
        form.instance.user = Profile.objects.get(user=self.request.user)
        return super(TaskCreate, self).form_valid(form)
    
class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    success_url = "/"
    form_class = TaskUpdateForm
    template_name = "todo/update_task.html"

class TaskComplete(LoginRequiredMixin, View):
    model = Task
    success_url = reverse_lazy("todo:task_list")

    def get(self, request, *args, **kwargs):
        object = Task.objects.get(id=kwargs.get("pk"))
        object.complete = True
        object.save()
        return redirect(self.success_url)

class DeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = "task"
    success_url = "/"

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def get_queryset(self):
        #return self.model.objects.filter(user=self.request.user)
        user_profile = Profile.objects.get(user=self.request.user)
        return self.model.objects.filter(user=user_profile)