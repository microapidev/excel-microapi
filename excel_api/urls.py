from django.urls import path

from .views import parserview, FilesList, get_duplicates

urlpatterns = [
    path('/add', FilesList.as_view()),
    path('/parse', parserview),
    path('/duplicate', get_duplicates),
]
