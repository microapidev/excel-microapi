from django.urls import path

from .views import parserview, FilesList, FilesAdd

urlpatterns = [
    path('add/', FilesAdd.as_view()),
    path('parse/', parserview),
    path('getall/',FilesList.as_view()),
]
