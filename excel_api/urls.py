from django.urls import path

from .views import parserview, FilesList

urlpatterns = [
    path('/parser/files/all', FilesList.as_view()),
    path('/parse', parserview),
]
