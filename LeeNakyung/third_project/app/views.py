from django.shortcuts import render
from datetime import datetime

def index(request):
    return render(request, 'app/index.html')

def select_question(request):
    return render(request, 'app/01_select_question.html')

def my_answer(request):
    return render(request, 'app/02_my_answer.html')

def ai_result(request):
    return render(request, 'app/03_ai_result.html')


