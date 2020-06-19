from django.urls import path

from .views import parserview, FilesList, FilesAdd, check_file, column_sum


urlpatterns = [
    path('add/', FilesAdd.as_view()),
    path('parser/', parserview),
    path('parser/files', FilesList.as_view()),
    path('checkfile/', check_file),
    path('column_sum/', column_sum),

]
