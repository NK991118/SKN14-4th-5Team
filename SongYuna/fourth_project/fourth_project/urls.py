from django.contrib import admin
# path와 함께 include 함수를 가져와. include는 다른 URL 설정을 포함시킬 때 사용해.
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.urls')),
]
