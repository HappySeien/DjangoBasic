from multiprocessing import context
from django.shortcuts import render
from django.views.generic import TemplateView
from django.conf import settings

import json

# Create your views here.


class IndexView(TemplateView):
    """
    Отображение главной страницы
    """
    template_name = 'mainapp/index.html'


class LoginView(TemplateView):
    """
    Отображение страницы входа
    """
    template_name = 'mainapp/login.html'


class NewsView(TemplateView):
    """
    Отображение страницы новостей
    """
    template_name = 'mainapp/news.html'

    def get_context_data(self, page, **kwargs) -> dict():
        context_data = super().get_context_data(**kwargs)
        context_data['page_num'] = page
        json_data = settings.JSON_DATA_MAINAPP
        with open(json_data / 'news.json', 'r', encoding='utf-8') as f:
            context_data['news_list'] = json.load(f)

        return context_data


class NewsPaginatorView(NewsView):
    """
    Пагинация для страницы новостей
    """

    def get_context_data(self, page, **kwargs) -> dict():
        context_data = super().get_context_data(**kwargs)
        
        context_data['page_num'] = page

        return context_data


class ContactsView(TemplateView):
    """
    Отображение страницы контакты
    """
    template_name = 'mainapp/contacts.html'

    def get_context_data(self, **kwargs) -> dict():
        context_data = super().get_context_data(**kwargs)

        context_data['contacts'] = [
            {
                'map': 'https://yandex.ru/map-widget/v1/-/CCUAZHcrhA',
                'city': 'Санкт‑Петербург',
                'phone': '+7-999-11-11111',
                'email': 'geeklab@spb.ru',
                'adress': 'территория Петропавловская крепость, 3Ж',
            }, {
                'map': 'https://yandex.ru/map-widget/v1/-/CCUAZHX3xB',
                'city': 'Казань',
                'phone': '+7-999-22-22222',
                'email': 'geeklab@kz.ru',
                'adress': 'территория Кремль, 11, Казань, Республика Татарстан, Россия',
            }, {
                'map': 'https://yandex.ru/map-widget/v1/-/CCUAZHh9kD',
                'city': 'Москва',
                'phone': '+7-999-33-33333',
                'email': 'geeklab@msk.ru',
                'adress': 'Красная площадь, 7, Москва, Россия',
            },
        ]

        return context_data


class CoursesListView(TemplateView):
    """
    Отображение страницы курсов
    """
    template_name = 'mainapp/courses_list.html'

    def get_context_data(self, page, **kwargs) -> dict():
        context_data = super().get_context_data(**kwargs)
        
        context_data['page_num'] = page

        return context_data


class CoursesPaginatorView(CoursesListView):
    """
    Пагинация для страницы курсов
    """

    def get_context_data(self, page, **kwargs) -> dict():
        context_data = super().get_context_data(**kwargs)
        
        context_data['page_num'] = page

        return context_data



class DocSiteView(TemplateView):
    """
    Отображение страницы Документация по сайту
    """
    template_name = 'mainapp/doc_site.html'
