from django.contrib import admin

from mainapp import models
from settingsapp.admin import BaseAdminSettings

# Register your models here.

@admin.register(models.News)
class NewsAdmin(BaseAdminSettings):
    list_display = ['pk', 'title', 'intro', 'body_as_markdown', 'created_at', 'deleted']
    list_filter = ['created_at', 'deleted']
    search_fields = ['title', 'intro', 'body']


@admin.register(models.Courses)
class CoursesAdmin(BaseAdminSettings):
    list_display = ['pk', 'name', 'cost', 'description_as_markdown', 'created_at', 'deleted']
    list_filter = ['description_as_markdown', 'created_at', 'deleted']
    search_fields = ['name']
    

@admin.register(models.Lessons)
class LessonsAdmin(BaseAdminSettings):
    list_display = ['pk', 'get_course_name', 'num', 'title', 'description_as_markdown', 'created_at', 'deleted']
    list_filter = ['course', 'created_at', 'deleted']
    search_fields = ['title']
    ordering = ('-course__name', 'num')

    def get_course_name(self, object):
        return object.course.name

    get_course_name.short_description = 'Курс'


@admin.register(models.CourseTeachers)
class CourseTeachersAdmin(BaseAdminSettings):
    list_display = ['pk', 'get_course_name', 'first_name', 'second_name', 'created_at', 'deleted']
    search_fields = ['first_name', 'second_name']

    def get_course_name(self, object):
        return object.course
    
    get_course_name.short_description = 'Курс'


@admin.register(models.Contacts)
class ContactsAdmin(BaseAdminSettings):
    list_display = ['pk', 'city', 'phone', 'email', 'created_at', 'deleted']
    list_filter = ['city', 'created_at', 'deleted']
