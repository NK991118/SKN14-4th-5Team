import re, markdown2, difflib, os, json

from django.conf import settings
from django.shortcuts import get_object_or_404
from .models import Submission

def extract_submission_details(submission_id):
    submission = get_object_or_404(Submission, pk=submission_id)

    try:
        pattern = re.compile(r"(.*?)(\*\*\[이렇게 바꿔보세요.*?)(\*\*\[예상 점수 및 다음 학습 팁.*)", re.DOTALL)
        match = pattern.search(submission.ai_comment)
        if match:
            main_comment_md, suggestion_part, final_comment_md = match.group(1).strip(), match.group(2).strip(), match.group(3).strip()
        else:
            main_comment_md, suggestion_part, final_comment_md = submission.ai_comment, "", ""

        def add_line_breaks_to_markdown(md_text):
            return re.sub(r'(\*\*.*?\]\*\*)\n', r'\1\n\n', md_text)

        main_comment_html = markdown2.markdown(add_line_breaks_to_markdown(main_comment_md))
        final_comment_html = markdown2.markdown(add_line_breaks_to_markdown(final_comment_md))

        suggestion_pattern = r"- 학생 원문:\s*(.*?)\s*- 수정 제안:\s*(.*?)(?=\n- 학생 원문:|\Z)"
        raw_suggestions = re.findall(suggestion_pattern, suggestion_part, re.DOTALL)
        suggestions = []
        d = difflib.Differ()
        for original_raw, suggestion_raw in raw_suggestions:
            original, suggestion = original_raw.strip(), suggestion_raw.strip()

            def preprocess_for_diff(text):
                return re.sub(r'([.,!?"\'])', r' \1 ', text)

            original_words, suggestion_words = preprocess_for_diff(original).split(), preprocess_for_diff(suggestion).split()
            diff = d.compare(original_words, suggestion_words)
            diff_html_parts = []
            for word in diff:
                if word.startswith('+ '):
                    diff_html_parts.append(f'<span class="diff-added">{word[2:]}</span>')
                elif word.startswith('- '):
                    diff_html_parts.append(f'<span class="diff-removed">{word[2:]}</span>')
                elif word.startswith('? '):
                    continue
                else:
                    diff_html_parts.append(word[2:])
            diff_html = ' '.join(diff_html_parts)
            diff_html = re.sub(r'\s+([.,!?"\'])', r'\1', diff_html)
            suggestions.append({'original': original, 'suggestion': suggestion, 'diff_html': diff_html})

    except Exception as e:
        main_comment_html = markdown2.markdown(submission.ai_comment)
        suggestions, final_comment_html = [], ""

    model_answer = "모범 답안을 찾을 수 없습니다."
    json_path = os.path.join(settings.BASE_DIR, 'data', 'json', f"{submission.question_id}.json")
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        model_answer = data.get('sample_answer', 'JSON 파일에 모범 답안이 없습니다.')
    except Exception as e:
        model_answer = f"모범 답안 로딩 중 오류 발생: {e}"

    return {
        'question_id': submission.question_id,
        'student_answer': submission.student_answer,
        'model_answer': model_answer,
        'main_comment_html': main_comment_html,
        'suggestions': suggestions,
        'final_comment_html': final_comment_html,
        'submission': submission,
    }
