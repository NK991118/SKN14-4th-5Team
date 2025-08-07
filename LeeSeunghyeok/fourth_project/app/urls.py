from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
    path('', views.index, name='index'),
    path('select-question/', views.select_question, name='01_select_question'),
    path('my-answer/', views.my_answer, name='02_my_answer'),
    path('run-grading/', views.run_grading, name='run_grading'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('history/', views.history_view, name='history'),
    path('api/chat/', views.chat_api, name='chat_api'),
    path('history/<int:submission_id>/', views.submission_detail_view, name='submission_detail'),
]