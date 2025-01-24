from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Question, Answer
from .form import QuestionForm, AnswerForm
from django.http import HttpResponseNotAllowed
from django.core.paginator import Paginator
# Create your views here.

# from django.http import HttpResponse

# def index(request):
#     return HttpResponse("gw 페이지입니다.")

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

def answer_create(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect('gw:detail', question_id=question.id)
    else:
        return HttpResponseNotAllowed('Only POST is possible.')
    context = {'question':question, 'form':form}
    return render(request, 'gw/question_detail.html', context)
    
            
    # # question.answer_set.create(content=request.POST.get('content'), create_date=timezone.now())
    # answer = Answer(question=question, content=request.POST.get('content'), create_date=timezone.now())
    # answer.save()
    # return redirect('gw:detail', question_id=question.id)

def question_create(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False) # 임시 저장(데이터페이스 업로드x)
            question.create_date = timezone.now() # 작성일시 저장
            question.save() # 데이터 실제로 저장
            return redirect('gw:index')
    else:
        form = QuestionForm()
    context = {'form' : form}
    return render(request, 'gw/question_form.html', context) 

              
    