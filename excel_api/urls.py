from django.urls import path

from .views import parserview, FilesList, export

urlpatterns = [
    path('/add', FilesList.as_view()),
    path('/parse', parserview),
    path('/export', export),
]
