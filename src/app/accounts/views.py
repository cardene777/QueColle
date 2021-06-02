from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic

from . import forms
from question.models import QuestionCollection


class MyLoginView(LoginView):
    form_class = forms.LoginForm
    template_name = "accounts/login.html"


class MyLogoutView(LoginRequiredMixin, LogoutView):
    template_name = "accounts/logout.html"


class SignUpView(generic.CreateView):
    form_class = forms.SignUpForm
    template_name = "accounts/signup.html"
    success_url = reverse_lazy("accounts:login")


class ProfileView(generic.TemplateView):
    template_name = "accounts/profile.html"
    model = QuestionCollection()
    context_object_name: str = "question_collection"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
