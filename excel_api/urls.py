from django.urls import path


from .views import parserview, FilesList, FilesAdd, check_file, column_sum, search_file, modify_file, process_duplicates, print_duplicate, doc

urlpatterns = [
    path('add/', FilesAdd.as_view()),
    path('parse/', parserview),
    path('getall/', FilesList.as_view()),
    path('checkfile/', check_file),
    path('column_sum/', column_sum),
    path('search/', search_file),
    path('add_row/', modify_file),
    path('duplicates/',process_duplicates),
    path('printduplicates/', print_duplicate),
    path('', doc),
]

