from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q  # OR조건으로 데이터를 조회하기위해 Q함수를 사용
from ..models import Question


def index(request):
    # GET 방식으로 호출된 url에서 page 값을 가져오고 디폴트 1로 설정
    page = request.GET.get('page', '1')
    kw = request.GET.get('kw', '') # 검색어
    question_list = Question.objects.order_by('-create_date')
    
    # subject__icontains=kw는 제목에 kw 문자열이 포함되는지를 의미, contains 대신 icontains를 사용하면 대소문자를 가리지 않고 찾음
    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw) |  # 제목 검색
            Q(content__icontains=kw) |  # 내용 검색
            Q(answer__content__icontains=kw) |  # 답변 내용 검색
            Q(author__username__icontains=kw) |  # 질문 글쓴이 검색
            Q(answer__author__username__icontains=kw)  # 답변 글쓴이 검색
        ).distinct() # distinct() : 중복 질문 제거
    
    paginator = Paginator(question_list, 10) # 페이지당 10개씩 보여준다.
    page_obj = paginator.get_page(page)
        
    context = {'question_list' : page_obj, 'page':page, 'kw': kw} # 템플릿에 전달하기 위해 page, kw 추가
    # render는 파이썬 데이터를 HTML로 반환
    # question_list.html과 같은 파일을 템플릿이라 부름. 별도의 템플릿 디렉터리에 생성한다.
    # 템플릿을 저장할 기본 디렉터리는 settings.py에 TEMPLATES 항목에 설정한다.
    return render(request, 'gw/question_list.html', context)

def detail(request, question_id):
    # question = Question.objects.get(id=question_id)
    question = get_object_or_404(Question, pk=question_id)
    context = {'question' : question}
    return render(request, 'gw/question_detail.html', context)