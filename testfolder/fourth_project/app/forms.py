from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

# Bootstrap 스타일을 적용하기 위한 커스텀 로그인 폼
class CustomAuthenticationForm(AuthenticationForm):
    # __init__ 메서드는 이 폼 클래스의 객체가 처음 만들어질 때 실행되는 특별한 함수야.
    def __init__(self, *args, **kwargs):
        # 일단 부모 클래스(AuthenticationForm)의 __init__을 그대로 실행해서 기본 설정을 가져와.
        super().__init__(*args, **kwargs)
        
        # username 필드에 'form-control' 클래스와 placeholder를 추가해줘.
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': '사용자 아이디를 입력하세요'
        })
        # password 필드에도 똑같이 적용해줘.
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': '비밀번호를 입력하세요'
        })


# Bootstrap 스타일을 적용하기 위한 커스텀 회원가입 폼
class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # UserCreationForm에 있는 모든 필드를 순회하면서
        for field_name, field in self.fields.items():
            # 모든 입력 칸(widget)에 'form-control' 클래스를 추가해.
            field.widget.attrs['class'] = 'form-control'
            # 모든 필드에 placeholder를 추가해서 사용자 경험을 좋게 만들어.
            if 'placeholder' not in field.widget.attrs:
                field.widget.attrs['placeholder'] = field.label