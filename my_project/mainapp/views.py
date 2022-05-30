from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView, DetailView

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

class NewsCreateView(PermissionRequiredMixin, CreateView):
    model = models.News
    fields = '__all__'
    success_url = reverse_lazy('mainapp:news')
    permission_required = ('mainapp.add_news',)


class NewsUpdateView(PermissionRequiredMixin, UpdateView):
    model = models.News
    fields = '__all__'
    success_url = reverse_lazy('mainapp:news')
    permission_required = ('mainapp.change_news',)


class NewsDeleteView(PermissionRequiredMixin, DeleteView):
    model = models.News
    success_url = reverse_lazy('mainapp:news')
    permission_required = ('mainapp.delete_news',)



class NewsDetailView(DetailView):
    """
    Отображение тела новости
    """

    template_name = "mainapp/news_detail.html"
    model = models.News
    
    


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
