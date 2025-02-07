from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator

from ..models import Question


def index(request):
    # GET 방식으로 호출된 url에서 page 값을 가져오고 디폴트 1로 설정
    page = request.GET.get('page', '1')
    question_list = Question.objects.order_by('-create_date')
    
    paginator = Paginator(question_list, 10) # 페이지당 10개씩 보여준다.
    page_obj = paginator.get_page(page)
        
    context = {'question_list' : page_obj}
    # render는 파이썬 데이터를 HTML로 반환
    # question_list.html과 같은 파일을 템플릿이라 부름. 별도의 템플릿 디렉터리에 생성한다.
    # 템플릿을 저장할 기본 디렉터리는 settings.py에 TEMPLATES 항목에 설정한다.
    return render(request, 'gw/question_list.html', context)

def detail(request, question_id):
    # question = Question.objects.get(id=question_id)
    question = get_object_or_404(Question, pk=question_id)
    context = {'question' : question}
    return render(request, 'gw/question_detail.html', context)