from django.urls import path
from . import views

app_name = 'question'

urlpatterns = [
    path('home/', views.QuestionHome.as_view(), name='home'),
    path('about/<int:pk>', views.QuestionAbout.as_view(), name='about'),
    path('question/<int:collection_id>', views.question, name='question'),
    path('answer/', views.answer, name='answer')
]

