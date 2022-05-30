from django.urls import path
from mainapp import views
from mainapp.apps import MainappConfig
from django.views.generic import RedirectView


app_name = MainappConfig.name

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('news/<int:page>', views.NewsView.as_view(), name='news'),
    path('news/<int:page>/detail/<int:pk>', views.NewsDetailView.as_view(), name='news_detail'),
    path('news/create/', views.NewsCreateView.as_view(), name='news_create'),
    path('news/<int:pk>/update', views.NewsUpdateView.as_view(), name='news_update'),
    path('news/<int:pk>/delete', views.NewsDeleteView.as_view(), name='news_delete'),

    path('newssearch/', RedirectView.as_view(url='https://yandex.ru/search/', query_string=True), name='news_search'),
    path('contacts/', views.ContactsView.as_view(), name='contacts'),
    path('courses/<int:page>', views.CoursesListView.as_view(), name='courses'),
    path('courses/<int:page>/detail/<int:pk>', views.CoursesDetailView.as_view(), name='courses_detail'),
    path('docsite/', views.DocSiteView.as_view(), name='docsite'),
    
]
