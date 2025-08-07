from django.shortcuts import render, redirect
from django.urls import reverse
from django.conf import settings
from django.contrib.auth import login, logout
from .forms import CustomAuthenticationForm, CustomUserCreationForm
from django.contrib.auth.decorators import login_required 
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import json

from .config import UNIVERSITY_DATA
from .ocr import process_image_to_text
from .grader import get_essay_grader

from .models import Submission
from .utils import extract_submission_details


def index(request):

    return render(request, 'app/index.html')

def select_question(request):
    
    context = {'schools_data_json': UNIVERSITY_DATA}
    
    return render(request, 'app/01_select_question.html', context)

@login_required(login_url='app:login')
def my_answer(request):
    
    if request.method == 'POST':

        question_id = request.POST.get('question_id')
        answer_image = request.FILES.get('answer_image')
        
        if answer_image:
            extracted_text = process_image_to_text(answer_image)
        else:
            extracted_text = "업로드된 이미지가 없습니다."

        request.session['question_id'] = question_id
        request.session['extracted_text'] = extracted_text
        
        return redirect(reverse('app:run_grading'))
    else:
        context = {'schools_data_json': UNIVERSITY_DATA}
        return render(request, 'app/02_my_answer.html', context)

@login_required 
def run_grading(request):
    
    question_id = request.session.get('question_id', '없음')
    student_answer = request.session.get('extracted_text', '추출된 텍스트가 없습니다.')
    
    ai_comment = "AI 채점을 실행할 수 없습니다."
    if question_id != '없음' and student_answer != '추출된 텍스트가 없습니다.':
        try:
            grader = get_essay_grader() 
            ai_comment = grader.grade_essay(question_id, student_answer)
        except Exception as e:
            ai_comment = f"AI 엔진 로드 중 오류가 발생했습니다: {e}"
        
    if "오류가 발생했습니다" not in ai_comment:
        submission = Submission.objects.create(
            user=request.user,
            question_id=question_id,
            student_answer=student_answer,
            ai_comment=ai_comment
        )
        
        return redirect(reverse('app:submission_detail', kwargs={'submission_id': submission.id}))
    
    else:
        return redirect('app:history')

def submission_detail_view(request, submission_id):
    context = extract_submission_details(submission_id)
    return render(request, 'app/03_ai_result.html', context)

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            
            next_url = request.POST.get('next')
            if next_url:
                return redirect(next_url)
            else:
                return redirect('app:index')
    else:
        form = CustomAuthenticationForm()

    next_url = request.GET.get('next', '')
    return render(request, 'app/login.html', {
        'form': form,
        'next': next_url
    })

def logout_view(request):
    logout(request)
    return redirect('app:index')

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('app:index')
    else:
        form = CustomUserCreationForm()
    return render(request, 'app/signup.html', {'form': form})

@login_required 
def history_view(request):
    submissions = Submission.objects.filter(user=request.user).order_by('-created_at')
    context = {
        'submissions': submissions
    }
    return render(request, 'app/history.html', context)

@csrf_exempt 
def chat_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_question = data.get('message')
            submission_id = data.get('submission_id')

            if not all([user_question, submission_id]):
                return JsonResponse({'error': '필수 데이터(질문 또는 ID)가 누락되었습니다.'}, status=400)
            
            submission = Submission.objects.get(pk=submission_id)

        except json.JSONDecodeError:
            return JsonResponse({'error': '잘못된 JSON 형식입니다.'}, status=400)
        except Submission.DoesNotExist:
            return JsonResponse({'error': '존재하지 않는 첨삭 기록입니다.'}, status=404)

        try:
            grader = get_essay_grader()
            ai_response = grader.mento_chat(
                student_answer=submission.student_answer,
                ai_comment=submission.ai_comment,
                user_question=user_question
            )
            return JsonResponse({'ai_message': ai_response})
            
        except Exception as e:
            return JsonResponse({'error': f'AI 응답 생성 중 오류가 발생했습니다: {e}'}, status=500)

    return JsonResponse({'error': 'POST 요청만 허용됩니다.'}, status=405)