<<<<<<< HEAD
from django.urls import path

from .views import parserview, FilesList, get_duplicates

urlpatterns = [
    path('/add', FilesList.as_view()),
    path('/parse', parserview),
    path('/duplicate', get_duplicates),
]
=======
from django.urls import path


from .views import parserview, FilesList, FilesAdd, check_file, column_sum,search_file #,export

urlpatterns = [
    path('add/', FilesAdd.as_view()),
    path('parse/', parserview),
    path('getall/', FilesList.as_view()),
    path('checkfile/', check_file),
    path('column_sum/', column_sum),
    path('column_sum/', column_sum),
    path('search/', search_file),
]

>>>>>>> 4853b7279337d750fedfae6d32b9839df497ff46
