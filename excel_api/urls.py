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

