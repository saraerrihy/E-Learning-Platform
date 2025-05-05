from django.urls import path
from . import views

app_name = 'quiz'

urlpatterns = [
    path('create/<int:course_id>/', views.quiz_create, name='quiz_create'),
    path('edit/<int:quiz_id>/', views.quiz_edit, name='quiz_edit'),
    path('delete/<int:quiz_id>/', views.quiz_delete, name='quiz_delete'),
    path('question/create/<int:quiz_id>/', views.question_create, name='question_create'),
    path('question/edit/<int:question_id>/', views.question_edit, name='question_edit'),
    path('question/delete/<int:question_id>/', views.question_delete, name='question_delete'),
    path('take/<int:quiz_id>/', views.take_quiz, name='take_quiz'),
    path('results/<int:attempt_id>/', views.quiz_results, name='quiz_results'),
    path('my-quizzes/', views.my_quizzes, name='my_quizzes'),
] 