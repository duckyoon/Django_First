from django.shortcuts import render
from .models import Question
# Create your views here.

# from django.http import HttpResponse

# def index(request):
#     return HttpResponse("gw 페이지입니다.")

def index(request):
    question_list = Question.objects.order_by('-create_date')
    context = {'question_list' : question_list}
    # render는 파이썬 데이터를 HTML로 반환
    # question_list.html과 같은 파일을 템플릿이라 부름. 별도의 템플릿 디렉터리에 생성한다.
    # 템플릿을 저장할 디렉터리는 settings.py에 TEMPLATES 항목에 설정한다.
    return render(request, 'gw/question_list.html', context)