from django.db import models

# Create your models here.


class BaseModel(models.Model):
    """
    Базовая модель
    """

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создана', editable=False)
    updated_at =models.DateTimeField(auto_now=True, verbose_name='Обновлена', editable=False)
    deleted = models.BooleanField(default=False)

    def delete(self, *args) -> None:
        self.deleted = True
        self.save()


    class Meta:
        abstract = True


class News(BaseModel):
    """
    Модель таблицы новости
    """

    title = models.CharField(max_length=256, verbose_name='Заголовок')
    intro = models.CharField(max_length=1024, verbose_name='Вступление')
    body = models.TextField(blank=True, null=True, verbose_name='Текст')
    body_as_markdown = models.BooleanField(default=False, verbose_name='Markdown')

    def __str__(self) -> str:
        return f'{self.pk} {self.title} {self.created_at}'

    def delete(self, *args) -> None:
        return super().delete(*args)


class Courses(BaseModel):
    """
    Модель таблицы курсы
    """

    name = models.CharField(max_length=256, verbose_name='Название')
    description = models.TextField(verbose_name='Описание', blank=True, null=True)
    description_as_markdown = models.BooleanField(default=False, verbose_name = 'Markdown')
    cost = models.DecimalField(max_digits=8, decimal_places=2, default=0, verbose_name='Цена')
    cover = models.CharField(max_length=25, default='no_image.svg', verbose_name='Изображение')

    def __str__(self) -> str:
        return f'{self.pk} {self.name} {self.created_at}'

    def delete(self, *args) -> None:
        return super().delete(*args)


class Lessons(BaseModel):
    """
    Модель таблицы занятий к курсам
    """ 

    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    num = models.PositiveIntegerField(verbose_name='Номер лекции')
    title = models.CharField(max_length=256, verbose_name='Тема лекции')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    description_as_markdown = models.BooleanField(default=False, verbose_name = 'Markdown')

    def __str__(self) -> str:
        return f'{self.pk} {self.title} {self.created_at}'

    def delete(self, *args) -> None:
        return super().delete(*args)

    
    class Meta:
        ordering = ('course', 'num')


class CourseTeachers(BaseModel):
    """
    Модель таблицы преподавателей на курсах
    """

    course = models.ManyToManyField(Courses)
    first_name = models.CharField(max_length=128, verbose_name='Имя')
    second_name = models.CharField(max_length=128, verbose_name='Фамилия')
    birth_day = models.DateField(verbose_name='Дата рождения')

    def __str__(self) -> str:
        return f'{self.pk} {self.second_name} {self.first_name} {self.created_at}'

    def delete(self, *args) -> None:
        return super().delete(*args)


class Contacts(BaseModel):
    """
    модель таблицы с контактной информацией
    """

    link_to_map = models.CharField(max_length=1024, verbose_name='Ссылка на карту')
    city = models.CharField(max_length=128, verbose_name='Город')
    phone = models.BigIntegerField(verbose_name='Телефон')
    email = models.CharField(max_length=256, verbose_name='email')
    adress = models.CharField(max_length=1024, verbose_name='Адрес')

    def __str__(self) -> str:
        return f'{self.pk} {self.city} {self.email} {self.created_at}'  

    def delete(self, *args) -> None:
        return super().delete(*args)

    