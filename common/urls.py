from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


app_name = 'common'

urlpatterns = [
    # 로그인 뷰는 django.contrib.auth 앱의 LoginView를 사용하도록 설정
    # LoginView는 registration 템플릿 디렉터리에서 login.html 파일을 찾는데,
    # common 디렉터리의 login.html 파일을 참조할 수 있도록 설정 -> as_view(template_name='common/login.html')
    path('login/', auth_views.LoginView.as_view(template_name='common/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup, name='signup')
] 