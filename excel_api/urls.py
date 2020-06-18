from django.urls import path

from .views import parserview, FilesList

urlpatterns = [
    path('/add', FilesList.as_view()),
    path('/parse', parserview),
]
