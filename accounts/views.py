from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
# Create your views here.

'''If use FormView for register user:

class RegisterPage(FormView):
    template_name = "accounts/register.html"
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy("task_list")

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect("task_list")
        return super(RegisterPage, self).get(*args, **kwargs)
'''


def indexView(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect("/")
    else:
        return render(request, "accounts/login.html")