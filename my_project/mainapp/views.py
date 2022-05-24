from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from mainapp import models

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
        context_data['news_list'] = models.News.objects.all()

        return context_data


class NewsPaginatorView(NewsView):
    """
    Пагинация для страницы новостей
    """

    def get_context_data(self, page, **kwargs) -> dict():
        context_data = super().get_context_data(**kwargs)
        
        context_data['page_num'] = page

        return context_data


class NewsDetailView(TemplateView):
    """
    Отображение тела новости
    """

    template_name = "mainapp/news_detail.html"
    
    def get_context_data(self, page, pk=None, **kwargs) -> dict():
        context_data = super().get_context_data(pk=pk, **kwargs)
        context_data["news_object"] = get_object_or_404(models.News, pk=pk)
        context_data['page_num'] = page

        return context_data



class ContactsView(TemplateView):
    """
    Отображение страницы контакты
    """
    template_name = 'mainapp/contacts.html'

    def get_context_data(self, **kwargs) -> dict():
        context_data = super().get_context_data(**kwargs)

        context_data['contacts'] = models.Contacts.objects.all()

        return context_data


class CoursesListView(TemplateView):
    """
    Отображение страницы курсов
    """
    template_name = 'mainapp/courses_list.html'

    def get_context_data(self, page, **kwargs) -> dict():
        context_data = super().get_context_data(**kwargs)

        context_data['courses_list'] = models.Courses.objects.values_list('pk', 'cover', 'name')
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


class CoursesDetailView(TemplateView):
    """
    Отображение подробной информации о курсе
    """

    template_name = "mainapp/courses_detail.html"
    
    def get_context_data(self, pk=None, **kwargs) -> dict():
        context_data = super().get_context_data(**kwargs)

        context_data["course_object"] = get_object_or_404(models.Courses, pk=pk)
        context_data["lessons"] = models.Lessons.objects.filter(course=context_data["course_object"])
        context_data["teachers"] = models.CourseTeachers.objects.filter(course=context_data["course_object"])
        
        return context_data


class DocSiteView(TemplateView):
    """
    Отображение страницы Документация по сайту
    """
    template_name = 'mainapp/doc_site.html'
