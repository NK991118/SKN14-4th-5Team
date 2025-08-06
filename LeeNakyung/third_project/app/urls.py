from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
    path('', views.index, name='index'),
    path('01_select_question', views.select_question, name='01_select_question'),
    path('02_my_answer', views.my_answer, name='02_my_answer'),
    path('03_ai_result', views.ai_result, name='03_ai_result'),
]