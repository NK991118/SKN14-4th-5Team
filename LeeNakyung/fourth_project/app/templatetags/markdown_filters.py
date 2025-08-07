# c:/Workspaces/Personal_Anything/3rd_to_4th/fourth_project/app/templatetags/markdown_filters.py (새 파일)

from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
import markdown2

# Django 템플릿 라이브러리에 우리 필터를 등록하기 위한 객체를 생성해.
register = template.Library()

@register.filter(name='markdown') # 'markdown'이라는 이름으로 필터를 등록!
@stringfilter # 이 필터에 들어오는 값을 자동으로 문자열로 바꿔주는 편리한 기능.
def markdown_filter(value):
    """
    일반 텍스트(마크다운 형식)를 HTML로 변환하는 필터.
    """
    # markdown2 라이브러리를 사용해서 텍스트를 HTML로 변환해.
    # extras=["fenced-code-blocks", "tables"] 등 다양한 확장 기능을 추가할 수도 있어.
    html = markdown2.markdown(value, extras=["fenced-code-blocks", "cuddled-lists"])
    
    # 변환된 HTML 코드가 안전하다는 표시(mark_safe)를 해서 템플릿에 전달해.
    # 이 표시가 없으면 Django는 보안을 위해 HTML 태그를 그대로 화면에 보여줘버려.
    return mark_safe(html)