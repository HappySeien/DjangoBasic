from settingsapp.tests import DefaultTestData
from django.urls import reverse
from django.core import mail as django_mail
from django.conf import settings
from django.test import TestCase

from http import HTTPStatus
import pickle
from unittest import mock

from mainapp import models
from authapp import models as authapp_models
from mainapp import tasks

# Create your tests here.

class StaticPagesSmokeTest(DefaultTestData):
    """
    Тест открытия страниц проекта
    """

    def setUp(self) -> None:
        return super().setUp()

    def test_index_page_open(self):
        path = reverse('mainapp:index')
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_News_detail_page_open(self):
        news_obj = models.News.objects.first()
        path = reverse('mainapp:news_detail', args=[1, news_obj.pk ])
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_contacts_page_open(self):
        path = reverse('mainapp:contacts')
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_docsite_page_open(self):
        path = reverse('mainapp:docsite')
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_log_page_open_deny_access(self):
        path = reverse('mainapp:log_view')
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_log_page_open_admin(self):
        path = reverse('mainapp:log_view')
        response = self.client_with_auth.get(path)
        self.assertEqual(response.status_code, HTTPStatus.OK)


class NewsCRUDtest(DefaultTestData):
    """
    Тесты доступа к CRUD опциям и их работы
    """

    def setUp(self) -> None:
        return super().setUp()
    
    def test_page_open_crete_deny_access(self):
        path = reverse('mainapp:news_create')
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_page_open_crete_by_admin(self):
        path = reverse('mainapp:news_create')
        response = self.client_with_auth.get(path)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_create_in_web(self):
        counter_before = models.News.objects.count()
        path = reverse('mainapp:news_create')
        self.client_with_auth.post(
            path,
            data={
                'title': 'NewTestNews001',
                'intro': 'NewTestNews001',
                'body': 'NewTestNews001',
            },
        )
        self.assertGreater(models.News.objects.count(), counter_before)

    def test_page_open_update_deny_access(self):
        news_obj = models.News.objects.first()
        path = reverse('mainapp:news_update', args=[1, news_obj.pk])
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_page_open_update_by_admin(self):
        news_obj = models.News.objects.first()
        path = reverse('mainapp:news_update', args=[1, news_obj.pk])
        response = self.client_with_auth.get(path)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_update_in_web(self):
        new_title = 'NewTestTitle001'
        news_obj = models.News.objects.first()
        self.assertNotEqual(news_obj.title, new_title)
        path = reverse('mainapp:news_update', args=[1, news_obj.pk])
        response = self.client_with_auth.post(
            path,
            data={
                'title': new_title,
                'intro': news_obj.intro,
                'body': news_obj.body,
            },
            HTTP_REFERER=reverse('mainapp:news', args=[1,])
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        news_obj.refresh_from_db()
        self.assertEqual(news_obj.title, new_title)

    def test_delete_deny_access(self):
        news_obj = models.News.objects.first()
        path = reverse('mainapp:news_delete', args=[1, news_obj.pk])
        result = self.client.post(path)
        self.assertEqual(result.status_code, HTTPStatus.FOUND)

    def test_delete_in_web(self):
        news_obj = models.News.objects.first()
        path = reverse('mainapp:news_delete', args=[1, news_obj.pk])
        self.client_with_auth.post(
            path,
            HTTP_REFERER=reverse('mainapp:news', args=[1,])
        )
        news_obj.refresh_from_db()
        self.assertTrue(news_obj.deleted)

# TODO не работает, разобраться почему
# class TestCachedPageWithMonk(TestCase):
#     """
#     Тестирование кешированных страниц
#     """
#     fixtures = (
#         'mainapp/fixtures/001_news.json',
#         'mainapp/fixtures/002_courses.json',
#         'mainapp/fixtures/003_lessons.json',
#         'mainapp/fixtures/004_teachers.json',
#     )

#     def test_News_list_page_open(self):
#         path = reverse('mainapp:news', args=[1,])
#         with open(
#             settings.BASE_DIR / 'mainapp/fixtures/011_news_list_.bin', 'rb'
#         ) as inpf, mock.patch('django.core.cache.cache.get') as mocked_cache:
#             mocked_cache.return_value = pickle.load(inpf)
#             response = self.client.get(path)
#             self.assertEqual(response.status_code, HTTPStatus.OK)
#             self.assertTrue(mocked_cache.called)
    
#     def test_courses_list_page_open(self):
#         path = reverse('mainapp:courses', args=[1,])
#         with open(
#             settings.BASE_DIR / 'mainapp/fixtures/012_courses_list_.bin', 'rb'
#         ) as inpf, mock.patch('django.core.cache.cache.get') as mocked_cache:
#             mocked_cache.return_value = pickle.load(inpf)
#             response = self.client.get(path)
#             self.assertEqual(response.status_code, HTTPStatus.OK)
#             self.assertTrue(mocked_cache.called)
        
#     def test_courses_detail_page_open(self):
#         course_obj = models.Courses.objects.first()
#         path = reverse('mainapp:courses_detail', args=[1, course_obj.pk])
#         with open(
#             settings.BASE_DIR / 'mainapp/fixtures/013_feedback_list_1.bin', 'rb'
#         ) as inpf, mock.patch('django.core.cache.cache.get') as mocked_cache:
#             mocked_cache.return_value = pickle.load(inpf)
#             response = self.client.get(path)
#             self.assertEqual(response.status_code, HTTPStatus.OK)
#             self.assertTrue(mocked_cache.called)


class TestTaskMailSend(DefaultTestData):
    """
    Тест отложенной задачи по отправке сообщения на email
    """
    
    def test_mail_send(self):
        message_text = 'test_message_text'
        user_obj = authapp_models.User.objects.first()
        tasks.send_feedback_mail(
            {'user_id': user_obj.id, 'message': message_text}
        )
        self.assertEqual(django_mail.outbox[0].body, message_text)