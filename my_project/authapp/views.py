from django.views.generic import CreateView, UpdateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe
from django.urls import reverse_lazy

from authapp import models
from authapp import forms

# Create your views here.

class CustomLoginView(LoginView):
    """
    Отображение страницы входа
    """
    template_name: str = 'authapp/login.html'

    def form_valid(self, form):
        ret = super().form_valid(form)
        message = _('Login success!<br>Hi, %(username)s') % {
            'username': self.request.user.get_full_name()
            if self.request.user.get_full_name()
            else self.request.user.get_username()
            }
        messages.add_message(self.request, messages.INFO, mark_safe(message))
        return ret

    def form_invalid(self, form):
        for _unused, msg in form.error_messages.items():
            messages.add_message(
                self.request,
                messages.WARNING,
                mark_safe(_(f'Something goes worng:<br>{msg}')),
            )
        return self.render_to_response(self.get_context_data(form=form))


class RegisterView(CreateView):
    """
    Отображение страницы регистрация
    """
    template_name: str = 'authapp/register.html'
    model = get_user_model()
    form_class = forms.CustomUserCreationFrom
    success_url = reverse_lazy('authapp:login')
        

class LogoutView(LogoutView):
    """
    Отображение сообщения при выходе пользователя
    """

    def dispatch(self, request, *args, **kwargs):
        messages.add_message(self.request, messages.INFO, _('See you later!'))
        return super().dispatch(request, *args, **kwargs)


class EditProfileView(UpdateView):
    """
    Отображение страницы редактирования профиля пользователя
    """
    template_name: str = 'authapp/profile_edit.html'
    model = models.User
    form_class = forms.CustomUserChangeFrom

    def get_object(self, queryset=None):
        return self.request.user
    
    def get_success_url(self):
        return reverse_lazy('authapp:profile_edit', args=[self.request.user.pk])

    
