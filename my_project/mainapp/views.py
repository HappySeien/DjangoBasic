from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, ListView

from mainapp import models

# Create your views here.


class IndexView(TemplateView):
    """
    Отображение главной страницы
    """
    template_name = 'mainapp/index.html'


class NewsView(ListView):
    """
    Отображение страницы новостей
    """
    template_name = 'mainapp/news.html'
    paginate_by: int = 5
    model = models.News
    queryset = model.non_delete_objects.all()

    def get_context_data(self, **kwargs) -> dict():
        context_data = super().get_context_data(**kwargs)

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

        context_data['contacts'] = models.Contacts.non_delete_objects.all()

        return context_data


class CoursesListView(ListView):
    """
    Отображение страницы курсов
    """
    template_name = 'mainapp/courses_list.html'

    paginate_by: int = 5
    model = models.Courses
    queryset = model.non_delete_objects.values_list('pk', 'cover', 'name')

    def get_context_data(self, **kwargs) -> dict():
        context_data = super().get_context_data(**kwargs)

        return context_data


class CoursesDetailView(TemplateView):
    """
    Отображение подробной информации о курсе
    """

    template_name = "mainapp/courses_detail.html"
    
    def get_context_data(self, pk=None, **kwargs) -> dict():
        context_data = super().get_context_data(**kwargs)

        context_data["course_object"] = get_object_or_404(models.Courses, pk=pk)
        context_data["lessons"] = models.Lessons.non_delete_objects.filter(course=context_data["course_object"])
        context_data["teachers"] = models.CourseTeachers.non_delete_objects.filter(course=context_data["course_object"])
        
        return context_data


class DocSiteView(TemplateView):
    """
    Отображение страницы Документация по сайту
    """
    template_name = 'mainapp/doc_site.html'
