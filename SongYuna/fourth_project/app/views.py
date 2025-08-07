from django.shortcuts import render, redirect
from django.urls import reverse
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .forms import CustomAuthenticationForm, CustomUserCreationForm
from django.contrib.auth.decorators import login_required 
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import os
import json

from .config import UNIVERSITY_DATA
from .ocr import process_image_to_text
from .grader import get_essay_grader
from .models import Submission

import re
import difflib
import markdown2

# index
def index(request):
    return render(request, 'app/index.html')


# 01_select_question 문항 선택
def select_question(request):
    """config.py 파일을 받아 pdf로 전달 """
    context = {'schools_data_json': UNIVERSITY_DATA}
    return render(request, 'app/01_select_question.html', context)


# 02_my_answer 나의 답안 입력
def my_answer(request):
    """question_id 전달 & 답안 이미지 업로드"""
    if request.method == 'POST':
        question_id = request.POST.get('question_id')
        # request.POST 대신 request.FILES !
        answer_image = request.FILES.get('answer_image')
        extracted_text = "업로드된 이미지가 없습니다."
        if answer_image:
            # ocr.py - def process_image_to_text
            extracted_text = process_image_to_text(answer_image)
       # session 저장 (question_id, answer_image->extracted_text)
        request.session['question_id'] = question_id
        request.session['extracted_text'] = extracted_text
        return redirect(reverse('app:run_grading'))
        
    else:
        # 이 페이지에도 대학-연도-문항 선택 드롭다운이 필요하므로 데이터를 템플릿에 전달해야 해.
        context = {'schools_data_json': UNIVERSITY_DATA}
        return render(request, 'app/02_my_answer.html', context)


# [4-1] AI 첨삭 실행 및 DB 저장 뷰 (기존 ai_result의 역할)
@login_required # 이제 DB 저장이 핵심이므로, 로그인은 필수!
def run_grading(request):
    """
    세션에서 데이터를 받아 AI 채점을 실행하고, 결과를 DB에 저장한 뒤, 
    상세 결과 페이지로 리다이렉트시키는 역할만 전담.
    """
    print("\n--- [run_grading] 뷰 함수 시작 ---")
    
    # 1. 세션에서 데이터 가져오기
    question_id = request.session.get('question_id', '없음')
    student_answer = request.session.get('extracted_text', '추출된 텍스트가 없습니다.')
    
    # 2. AI 첨삭 실행
    ai_comment = "AI 채점을 실행할 수 없습니다."
    if question_id != '없음' and student_answer != '추출된 텍스트가 없습니다.':
        try:
            grader = get_essay_grader() 
            ai_comment = grader.grade_essay(question_id, student_answer)
            print("  [CCTV-6] AI 첨삭 실행 성공!")
        except Exception as e:
            print(f"  [CRITICAL ERROR] AI 엔진 호출 중 오류 발생: {e}")
            ai_comment = f"AI 엔진 로드 중 오류가 발생했습니다: {e}"
        
    # 3. DB에 저장하기
    if "오류가 발생했습니다" not in ai_comment:
        submission = Submission.objects.create(
            user=request.user,
            question_id=question_id,
            student_answer=student_answer,
            ai_comment=ai_comment
        )
        print(f"✅ '{request.user.username}' 사용자의 첨삭 결과 (ID: {submission.id})가 DB에 저장되었습니다.")
        
        # 4. ★★★ 핵심! ★★★
        #    결과를 직접 보여주지 않고, 방금 생성된 제출물의 상세 페이지로 이동시켜버려!
        return redirect(reverse('app:submission_detail', kwargs={'submission_id': submission.id}))
    else:
        # 만약 AI 채점 자체를 실패했다면, 에러 메시지를 들고 히스토리 페이지로 보낸다.
        # (이 부분은 나중에 더 예쁜 에러 페이지로 만들 수도 있어)
        return redirect('app:history')


# [4-2] 첨삭 결과 상세 페이지 뷰 (화면에 그리는 역할)
def submission_detail_view(request, submission_id):
    """
    DB에서 특정 ID의 첨삭 결과를 가져와서, 파싱하고, 
    '03_ai_result.html' 템플릿을 그려주는 역할.
    """
    print(f"\n--- [submission_detail_view] 뷰 함수 시작 (ID: {submission_id}) ---")
    
    # 1. DB에서 데이터 가져오기
    # get_object_or_404는 데이터가 있으면 가져오고, 없으면 404 에러 페이지를 보여주는 편리한 함수야.
    from django.shortcuts import get_object_or_404
    submission = get_object_or_404(Submission, pk=submission_id)

    # 2. 프론트엔드 표시를 위한 데이터 가공 (기존 ai_result의 파싱 로직 그대로)
    try:
        # (파싱 로직은 길어서 생략... 기존 ai_result에 있던 파싱 코드 전체를 여기에 복붙하면 돼)
        pattern = re.compile(r"(.*?)(\*\*\[이렇게 바꿔보세요.*?)(\*\*\[예상 점수 및 다음 학습 팁.*)", re.DOTALL)
        match = pattern.search(submission.ai_comment)
        if match:
            main_comment_md, suggestion_part, final_comment_md = match.group(1).strip(), match.group(2).strip(), match.group(3).strip()
        else:
            main_comment_md, suggestion_part, final_comment_md = submission.ai_comment, "", ""
        
        def add_line_breaks_to_markdown(md_text): return re.sub(r'(\*\*.*?\]\*\*)\n', r'\1\n\n', md_text)
        main_comment_html = markdown2.markdown(add_line_breaks_to_markdown(main_comment_md))
        final_comment_html = markdown2.markdown(add_line_breaks_to_markdown(final_comment_md))
        
        suggestion_pattern = r"- 학생 원문:\s*(.*?)\s*- 수정 제안:\s*(.*?)(?=\n- 학생 원문:|\Z)"
        raw_suggestions = re.findall(suggestion_pattern, suggestion_part, re.DOTALL)
        suggestions = []
        d = difflib.Differ()
        for original_raw, suggestion_raw in raw_suggestions:
            original, suggestion = original_raw.strip(), suggestion_raw.strip()
            def preprocess_for_diff(text): return re.sub(r'([.,!?"\'])', r' \1 ', text)
            original_words, suggestion_words = preprocess_for_diff(original).split(), preprocess_for_diff(suggestion).split()
            diff = d.compare(original_words, suggestion_words)
            diff_html_parts = []
            for word in diff:
                if word.startswith('+ '): diff_html_parts.append(f'<span class="diff-added">{word[2:]}</span>')
                elif word.startswith('- '): diff_html_parts.append(f'<span class="diff-removed">{word[2:]}</span>')
                elif word.startswith('? '): continue
                else: diff_html_parts.append(word[2:])
            diff_html = ' '.join(diff_html_parts)
            diff_html = re.sub(r'\s+([.,!?"\'])', r'\1', diff_html)
            suggestions.append({'original': original, 'suggestion': suggestion, 'diff_html': diff_html})

    except Exception as e:
        print(f"[파싱 에러] AI 코멘트 파싱 실패: {e}. 원본 텍스트를 표시합니다.")
        main_comment_html = markdown2.markdown(submission.ai_comment)
        suggestions, final_comment_html = [], ""

    # 3. 모범 답안 로딩 (이것도 기존 로직 그대로)
    model_answer = "모범 답안을 찾을 수 없습니다."
    json_path = os.path.join(settings.BASE_DIR, 'data', 'json', f"{submission.question_id}.json")
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        model_answer = data.get('sample_answer', 'JSON 파일에 모범 답안이 없습니다.')
    except Exception as e:
        model_answer = f"모범 답안 로딩 중 오류 발생: {e}"

    # 4. 최종 데이터를 템플릿에 전달
    context = {
        'question_id': submission.question_id,
        'student_answer': submission.student_answer,
        'model_answer': model_answer,
        'main_comment_html': main_comment_html, 
        'suggestions': suggestions,
        'final_comment_html': final_comment_html,
        'submission': submission,
    }
    return render(request, 'app/03_ai_result.html', context)


# ✨✨✨ [5] 로그인 뷰 함수 (위치를 바로잡았어!) ✨✨✨
def login_view(request):
    """사용자 로그인을 처리하는 뷰입니다."""
    if request.method == 'POST':
        # 사용자가 제출한 아이디/비밀번호로 인증 폼을 생성합니다.
        form = CustomAuthenticationForm(request, data=request.POST)
        # 폼 데이터가 유효한지 검사합니다.
        if form.is_valid():
            # 폼에서 검증된 사용자 객체를 가져옵니다.
            user = form.get_user()
            # 사용자를 로그인 상태로 만듭니다.
            login(request, user)
            # 로그인이 성공하면 메인 페이지로 보냅니다.
            return redirect('app:index')
    else:
        # GET 요청일 경우, 그냥 비어있는 로그인 폼을 생성합니다.
        form = CustomAuthenticationForm()
    # 템플릿에 폼을 전달하여 로그인 페이지를 보여줍니다.
    return render(request, 'app/login.html', {'form': form})


# ✨✨✨ [6] 로그아웃 뷰 함수 (위치를 바로잡았어!) ✨✨✨
def logout_view(request):
    """사용자 로그아웃을 처리하는 뷰입니다."""
    # 사용자를 로그아웃시킵니다.
    logout(request)
    # 로그아웃 후 메인 페이지로 보냅니다.
    return redirect('app:index')

# ✨✨✨ [7] 회원가입 뷰 함수 (새로 추가!) ✨✨✨
def signup_view(request):
    """사용자 회원가입을 처리하는 뷰입니다."""
    # 사용자가 폼에 데이터를 채워서 '제출'했을 때 (POST 방식)
    if request.method == 'POST':
        # 사용자가 제출한 데이터로 회원가입 폼을 생성합니다.
        form = CustomUserCreationForm(request.POST)
        # 폼에 담긴 데이터가 유효한지 (비밀번호가 일치하는지 등) 검사합니다.
        if form.is_valid():
            # 폼 데이터가 유효하다면, form.save()를 통해 새 사용자를 데이터베이스에 저장합니다.
            user = form.save()
            # 회원가입이 성공하면, 그 사용자를 바로 로그인 상태로 만들어 줍니다. (사용자 경험 향상!)
            login(request, user)
            # 모든 처리가 끝나면 메인 페이지로 이동시킵니다.
            return redirect('app:index')
        # 폼 데이터가 유효하지 않다면, 오류 메시지를 포함한 폼을 가지고 다시 회원가입 페이지를 보여줍니다.
    
    # 사용자가 그냥 '/signup' 페이지에 처음 '접속'했을 때 (GET 방식)
    else:
        # 그냥 비어있는 깨끗한 회원가입 폼을 생성합니다.
        form = CustomUserCreationForm()
        
    # 템플릿에 폼을 전달하여 회원가입 페이지를 보여줍니다.
    return render(request, 'app/signup.html', {'form': form})

# ✨✨✨ [8] 나의 첨삭 히스토리 뷰 함수 (드디어 완성!) ✨✨✨
@login_required # 로그인한 사용자만 접근 가능!
def history_view(request):
    """로그인한 사용자의 첨삭 히스토리 목록을 보여주는 뷰입니다."""
    
    # 1. 데이터베이스에서 데이터 가져오기 (ORM의 마법!)
    # Submission.objects는 우리 데이터베이스의 Submission 테이블에 접근하는 창구야.
    # .filter(user=request.user)는 "모든 Submission 기록 중에서, user 필드가
    # 현재 로그인한 사용자(request.user)와 일치하는 것만 골라줘!" 라는 강력한 필터링 기능이야.
    # .order_by('-created_at')는 결과를 '만들어진 시간(created_at)'을 기준으로 정렬하는데,
    # 앞에 붙은 '-'는 '내림차순(descending)', 즉 최신 기록이 맨 위로 오게 하라는 뜻이야.
    submissions = Submission.objects.filter(user=request.user).order_by('-created_at')
    
    # 2. 가져온 데이터를 'context' 보따리에 담기
    # 'submissions'라는 이름표를 붙여서, 우리가 방금 가져온 기록 목록을 담아줘.
    context = {
        'submissions': submissions
    }
    
    # 3. 데이터 보따리를 가지고 템플릿을 그려서 사용자에게 보여주기
    return render(request, 'app/history.html', context)

# ✨✨✨ [9] 채팅 API 뷰 함수 (이 함수가 누락된 거야!) ✨✨✨

# c:/Workspaces/Personal_Anything/3rd_to_4th/fourth_project/app/views.py

# c:/Workspaces/Personal_Anything/3rd_to_4th/fourth_project/app/views.py

@csrf_exempt 
def chat_api(request):
    """채팅 메시지를 받아 AI의 응답을 JSON으로 반환하는 API 뷰입니다."""
    
    if request.method == 'POST':
        print(f"[Chat-API-DEBUG] Received request body: {request.body}") # 디버깅 로그 추가
        try:
            data = json.loads(request.body)
            user_question = data.get('message')
            submission_id = data.get('submission_id')

            # ★★★ 여기서 submission_id가 비어있거나 None이면 에러가 발생! ★★★
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
            print(f"[Chat-API-ERROR] 챗봇 응답 생성 중 오류 발생: {e}")
            return JsonResponse({'error': f'AI 응답 생성 중 오류가 발생했습니다: {e}'}, status=500)

    return JsonResponse({'error': 'POST 요청만 허용됩니다.'}, status=405)