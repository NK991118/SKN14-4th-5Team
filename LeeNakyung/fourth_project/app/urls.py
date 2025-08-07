from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
    path('', views.index, name='index'),
    path('01_select_question', views.select_question, name='01_select_question'),
    path('02_my_answer', views.my_answer, name='02_my_answer'),
    path('run-grading/', views.run_grading, name='run_grading'),

    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
    
    # '나의 첨삭 히스토리' 페이지
    path('history/', views.history_view, name='history'),

    # 채팅 API를 위한 경로
    path('api/chat/', views.chat_api, name='chat_api'),

    # <int:submission_id>는 이 위치에 오는 숫자를 submission_id라는 변수로 받아서 뷰에 넘기라는 뜻이야.
    path('history/<int:submission_id>/', views.submission_detail_view, name='submission_detail'),
]