from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from settingsapp.models import BaseModel, NULLABLE, RATING

# Create your models here.


class News(BaseModel):
    """
    Модель таблицы новости
    """

    title = models.CharField(max_length=256, verbose_name=_('Title'))
    intro = models.CharField(max_length=1024, verbose_name=_('Intro'))
    body = models.TextField(**NULLABLE, verbose_name=_('Text'))
    body_as_markdown = models.BooleanField(default=False, verbose_name='as_Markdown')

    def __str__(self) -> str:
        return f'{self.pk} {self.title} {self.created_at}'

    def delete(self, *args) -> None:
        return super().delete(*args)

    class Meta:
        verbose_name = _('News')
        verbose_name_plural = _('News')
        ordering = ('-created_at',)


class Courses(BaseModel):
    """
    Модель таблицы курсы
    """

    name = models.CharField(max_length=256, verbose_name=_('Course name'))
    description = models.TextField(verbose_name=_('Description'), **NULLABLE)
    description_as_markdown = models.BooleanField(default=False, verbose_name = 'as_Markdown')
    cost = models.DecimalField(max_digits=8, decimal_places=2, default=0, verbose_name=_('Cost'))
    cover = models.CharField(max_length=25, default='no_image.svg', verbose_name=_('Cover'))

    def __str__(self) -> str:
        return f'{self.pk} {self.name} {self.created_at}'

    def delete(self, *args) -> None:
        return super().delete(*args)

    class Meta:
        verbose_name = _('Course')
        verbose_name_plural = _('Courses')


class Lessons(BaseModel):
    """
    Модель таблицы занятий к курсам
    """ 

    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    num = models.PositiveIntegerField(verbose_name=_('Lesson number'))
    title = models.CharField(max_length=256, verbose_name=_('Title'))
    description = models.TextField(**NULLABLE, verbose_name=_('Description'))
    description_as_markdown = models.BooleanField(default=False, verbose_name = 'as_Markdown')

    def __str__(self) -> str:
        return f'{self.pk} {self.title} {self.created_at}'

    def delete(self, *args) -> None:
        return super().delete(*args)

    
    class Meta:
        ordering = ('course', 'num')
        verbose_name = _('Lesson')
        verbose_name_plural = _('Lessons')


class CourseTeachers(BaseModel):
    """
    Модель таблицы преподавателей на курсах
    """

    course = models.ManyToManyField(Courses)
    first_name = models.CharField(max_length=128, verbose_name=_('First name'))
    second_name = models.CharField(max_length=128, verbose_name=_('Last name'))
    birth_day = models.DateField(verbose_name=_('Birth day'))

    def __str__(self) -> str:
        return f'{self.pk} {self.second_name} {self.first_name} {self.created_at}'

    def delete(self, *args) -> None:
        return super().delete(*args)

    class Meta:
        verbose_name = _('Teacher')
        verbose_name_plural = _('Teachers')


class CourseFeedback(BaseModel):
    """
    Модель таблицы отзывов
    """
    course = models.ForeignKey(Courses, on_delete=models.CASCADE, verbose_name=_('Course'))
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name=_('User'))
    feedback = models.TextField(default=_('No feedback'), verbose_name=_('Feedback'))
    rating = models.SmallIntegerField(choices=RATING, default=5, verbose_name=_('Rating'))

    def __str__(self):
        return f'{self.course} ({self.user})'

    class Meta:
        verbose_name = 'Course feedback'
        verbose_name_plural = 'Course feedbacks'


class Contacts(BaseModel):
    """
    модель таблицы с контактной информацией
    """

    link_to_map = models.CharField(max_length=1024, verbose_name=_('Link to map'))
    city = models.CharField(max_length=128, verbose_name=_('City'))
    phone = models.BigIntegerField(verbose_name=_('Phone'))
    email = models.CharField(max_length=256, verbose_name=_('Email'))
    adress = models.CharField(max_length=1024, verbose_name=_('Adress'))

    def __str__(self) -> str:
        return f'{self.pk} {self.city} {self.email} {self.created_at}'  

    def delete(self, *args) -> None:
        return super().delete(*args)

    class Meta:
        verbose_name = _('Contact')
        verbose_name_plural = _('Contacts')

    