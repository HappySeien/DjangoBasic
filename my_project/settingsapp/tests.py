from django.test import TestCase, Client
from django.urls import reverse

from mainapp import models
from authapp.models import User

# Create your tests here.

class DefaultTestData(TestCase):
    """
    Настройки по умолчанию set_up для тестов
    """

    def setUp(self) -> None:
        for i in range(10):
            models.News.objects.create(
                title=f'TestNews{i}',
                intro=f'Testintro{i}',
                body=f'TestText{i}'
            )
            models.Courses.objects.create(
                name=f'TestCorsename{i}',
                description=f'TestCorseDescription{i}',
                cost=i * 1000
            )
        User.objects.create_superuser(username='testadmin', password='12345678')
        self.client_with_auth = Client()
        auth_url = reverse('authapp:login')
        self.client_with_auth.post(
            auth_url,
            {'username': 'testadmin', 'password': '12345678'}
        )
