from settingsapp.tests import DefaultTestData
from django.urls import reverse

from http import HTTPStatus
from mainapp import models

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

    def test_News_list_page_open(self):
        path = reverse('mainapp:news', args=[1,])
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_News_detail_page_open(self):
        news_obj = models.News.objects.first()
        path = reverse('mainapp:news_detail', args=[1, news_obj.pk ])
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_courses_list_page_open(self):
        path = reverse('mainapp:courses', args=[1,])
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_courses_detail_page_open(self):
        course_obj = models.Courses.objects.first()
        path = reverse('mainapp:courses_detail', args=[1, course_obj.pk])
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

    def test_log_page_open(self):
        path = reverse('mainapp:log_view')
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.OK)
