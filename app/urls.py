from django.urls import path
from . import views as view
urlpatterns=[
    path('',view.Home,name="home"),     
    path('notes/',view.notes,name="notes"),
    path('delete_notes/<int:pk>',view.delete_note,name="delete_note"),
    path('detail_notes/<int:pk>',view.detail_note,name='detail_note'),
    path('home_work/',view.Homework,name='homework'),
    path('updatehome/<int:pk>',view.updatehomework,name='update_home'),
    path('delete_home/<int:pk>',view.delete_homework,name='delete_home'),
    path('youtube/',view.Youtube,name='youtube'),
    path('todo/',view.todo,name='todo'),
    path('update_todo/<int:pk>',view.update_todo,name='update_todo'),
    path('delete_todo/<int:pk>',view.delete_todo,name='delete_todo'),
    path('books/',view.books,name = 'books'),
    path('dictionary/',view.dictionary,name = "dictionary"),
    path('wiki/',view.wiki,name= "wiki"),
    path('conversion',view.conversion,name = 'conversion'),
   
]