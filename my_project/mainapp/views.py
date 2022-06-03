from django.shortcuts import get_object_or_404 
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from django.http import FileResponse, JsonResponse
from django.http.response import HttpResponseRedirect
from django.template.loader import render_to_string
from django.views import View
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView, DetailView
from django.core.cache import cache
import logging

from mainapp import models, forms
from django.conf import settings
from mainapp import tasks

# Create your views here.

logger = logging.getLogger(__name__)


class LogView(TemplateView):
    """
    Отображение страницы логирования на сайте
    """
    template_name: str = 'mainapp/log_view.html'

    def get_context_data(self, **kwargs) -> dict():
        context_data = super().get_context_data(**kwargs)
        log_slice = []
        with open(settings.LOG_FILE, 'r') as f:
            for i, line in enumerate(f):
                if i == 1000:
                    break
                log_slice.insert(0, line)
            context_data['log'] = ''.join(log_slice)
        return context_data


class LogDownloadView(UserPassesTestMixin, View):
    """
    Загрузка логов
    """

    def test_func(self):
        return self.request.user.is_superuser

    def get(self, *args, **kwargs):
        return FileResponse(open(settings.LOG_FILE, 'rb'))


class IndexView(TemplateView):
    """
    Отображение главной страницы
    """
    template_name = 'mainapp/index.html'


class NewsView(ListView):
    """
    Отображение страницы новостей
    """
    paginate_by: int = 5
    model = models.News
    queryset = model.non_delete_objects.all()

    def get_context_data(self, **kwargs) -> dict():
        context_data = super().get_context_data(**kwargs)

        return context_data

class NewsCreateView(PermissionRequiredMixin, CreateView):
    """
    CRUD создание новости
    """
    model = models.News
    fields = '__all__'
    permission_required = ('mainapp.add_news',)

    def get_success_url(self):
        return reverse_lazy('mainapp:news', args=[1,])


class NewsUpdateView(PermissionRequiredMixin, UpdateView):
    """
    CRUD редактирование новости
    """
    model = models.News
    fields = '__all__'
    permission_required = ('mainapp.change_news',)

    def get_success_url(self):
        previos_url = '/'.join(self.request.META.get('HTTP_REFERER').split('/')[:-2]) 
        return previos_url


class NewsDeleteView(PermissionRequiredMixin, DeleteView):
    """
    CRUD удаление новости
    """
    model = models.News
    permission_required = ('mainapp.delete_news',)

    def get_success_url(self):
        previos_url = '/'.join(self.request.META.get('HTTP_REFERER').split('/')[:-2]) 
        return previos_url


class NewsDetailView(DetailView):
    """
    Отображение тела новости
    """
    model = models.News
    
    


class ContactsView(TemplateView):
    """
    Отображение страницы контакты
    """
    template_name = 'mainapp/contacts.html'

    def get_context_data(self, **kwargs) -> dict():
        context_data = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context_data['form'] = forms.MailFeedbackForm(user=self.request.user)
        context_data['contacts'] = models.Contacts.non_delete_objects.all()

        return context_data

    def post(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            cache_lock_flag = cache.get(f'mail_feedback_lock_{self.request.user.pk}')
            if not cache_lock_flag:
                cache.set(f'mail_feedback_lock_{self.request.user.pk}', 'lock', timeout=300)
                messages.add_message(self.request, messages.INFO, _('Message sended'))
                tasks.send_feedback_mail.delay(
                    {
                        'user_id': self.request.POST.get('user_id'),
                        'message': self.request.POST.get('message')
                    }
                )
            else:
                messages.add_message(self.request, messages.WARNING, _("You can send only one message per 5 minutes"))
        return HttpResponseRedirect(reverse_lazy('mainapp:contacts'))


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
        if not self.request.user.is_anonymous:
            if not models.CourseFeedback.objects.filter(
                course = context_data['course_object'], user=self.request.user
            ).count():
                context_data['feedback_form'] = forms.CourseFeedbackForm(
                    course=context_data['course_object'], user=self.request.user
                )
        cached_feedback = cache.get(f'feedback_list_{pk}')
        if not cached_feedback:
            context_data['feedback_list'] = models.CourseFeedback.objects.filter(
                course=context_data['course_object']
            ).order_by('-created_at', '-rating')[:5].select_related()
            cache.set(f'feedback_list_{pk}', context_data["feedback_list"], timeout=300)
        else:
            context_data["feedback_list"] = cached_feedback
        
        return context_data


class CourseFeedbackFormProcessView(LoginRequiredMixin, CreateView):
    """
    Отображение формы отзыв
    """
    model = models.CourseFeedback
    form_class = forms.CourseFeedbackForm

    def form_valid(self, form):
        self.object = form.save()
        rendered_card = render_to_string('mainapp/includes/inc_feedback_card.html', context={"item": self.object})
        return JsonResponse({'card': rendered_card})


class DocSiteView(TemplateView):
    """
    Отображение страницы Документация по сайту
    """
    template_name = 'mainapp/doc_site.html'
