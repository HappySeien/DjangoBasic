from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, UsernameField
from django.core.exceptions import ValidationError

import os


class CustomUserCreationFrom(UserCreationForm):
    """
    Форма регистрации пользователя
    """

    class Meta:
        model = get_user_model()
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'age',
            'avatar'
        )
        field_classes = {'username': UsernameField}
    
    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age < 10 or age > 150:
            raise ValidationError('Укажите реальный возраст')
        return age


class CustomUserChangeFrom(UserChangeForm):
    """
    Форма регистрации пользователя
    """

    class Meta:
        model = get_user_model()
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'age',
            'avatar'
        )
        field_classes = {'username': UsernameField}
    
    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age < 10 or age > 150:
            raise ValidationError('Укажите реальный возраст')
        return age

    def clean_avatar(self):
        arg_ = 'avatar'
        if arg_ in self.changed_data and self.instance.avatar:
            if os.path.exists(self.instance.avatar.path):
                os.remove(self.instance.avatar.path)
        return self.cleaned_data.get(arg_)
        