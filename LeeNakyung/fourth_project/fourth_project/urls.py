"""
URL configuration for fourth_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
# path와 함께 include 함수를 가져와. include는 다른 URL 설정을 포함시킬 때 사용해.
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # '' (빈 경로, 즉 웹사이트의 가장 기본 주소)로 들어오는 모든 요청을
    # 'app.urls' 파일에서 처리하도록 넘겨주는 설정이야.
    path('', include('app.urls')),
]
