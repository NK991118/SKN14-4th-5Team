from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
    path('', views.index, name='index'),
    
    # 문항 선택
    path('select-question/', views.select_question, name='01_select_question'),
    # 나의 답안 입력
    path('my-answer/', views.my_answer, name='02_my_answer'),
    # AI 첨삭
    path('run-grading/', views.run_grading, name='run_grading'),

    # login/logout
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    # singup
    path('signup/', views.signup_view, name='signup'),
    
    # history
    path('history/', views.history_view, name='history'),

    # api for chatting
    path('api/chat/', views.chat_api, name='chat_api'),

    # <int:submission_id>는 이 위치에 오는 숫자를 submission_id라는 변수로 받아서 뷰에 넘기라는 뜻이야.
    path('history/<int:submission_id>/', views.submission_detail_view, name='submission_detail'),
]