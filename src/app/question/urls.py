from django.urls import path
from . import views

app_name = 'question'

urlpatterns = [
    path('home/', views.QuestionHome.as_view(), name='home'),
    path('question_collection_update/<int:pk>/', views.QuestionCollectionUpdate.as_view(),
         name='question_collection_update'),
    path('question_update/<int:pk>/', views.QuestionUpdate.as_view(), name='question_update'),
    path('question_delete/<int:pk>/', views.QuestionDelete.as_view(), name='question_delete'),
    path('about/<int:pk>/', views.QuestionAbout.as_view(), name='about'),
    path('question_list/<int:collection_id>/', views.question_list, name='question_list'),
    path('question/<int:collection_id>/', views.question, name='question'),
    path('answer/', views.answer, name='answer'),
    path('create_question_collection/', views.CreateQuestionCollection.as_view(), name='create_question_collection'),
    path('create_question/<int:question_collection_id>/', views.create_question, name='create_question'),
    path('aggregation/<str:username>/', views.aggregation, name='aggregation'),
    path('plot/<str:username>/<str:collection>/', views.plot, name='plot'),
]

