from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('quiz/<int:quiz_id>', views.view_quiz, name='view_quiz'),
    path('quiz/<int:quiz_id>/submit', views.submit_quiz, name='submit_quiz'),

]