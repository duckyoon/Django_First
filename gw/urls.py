from django.urls import path

from . import views

app_name = 'gw'

urlpatterns = [
    path('', views.index, name='index'),
    # 기본적으로 매핑할 때, gw/ url을 매핑하므로 ''를 사용한다.
    
    path('<int:question_id>/', views.detail, name='detail'),
    path('answer/create/<question_id>', views.answer_create, name='answer_create'),
    path('question/create/', views.question_create, name='question_create')
]