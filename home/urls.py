from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('invite/<int:quiz_id>', views.invite_to_quiz, name='invite'),
    path('quiz/<int:quiz_id>', views.view_quiz, name='quiz'),
    path('result/<int:answer_id>', views.view_result, name='result'),
]