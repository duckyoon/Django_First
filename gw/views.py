from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Question, Answer
from .form import QuestionForm, AnswerForm
from django.http import HttpResponseNotAllowed
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
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

@login_required(login_url='common:login') # 로그아웃 상태에서 함수가 호출되면 자동으로 로그인 화면으로 이동시킴
def answer_create(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user # author 속성에 로그인 계정
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect('gw:detail', question_id=question.id)
    else:
        form = QuestionForm()
    context = {'question':question, 'form':form}
    return render(request, 'gw/question_detail.html', context)
    
            
    # # question.answer_set.create(content=request.POST.get('content'), create_date=timezone.now())
    # answer = Answer(question=question, content=request.POST.get('content'), create_date=timezone.now())
    # answer.save()
    # return redirect('gw:detail', question_id=question.id)

@login_required(login_url='common:login') # 로그아웃 상태에서 함수가 호출되면 자동으로 로그인 화면으로 이동시킴
def question_create(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False) # 임시 저장(데이터베이스 업로드x)
            question.author = request.user # author 속성에 로그인 계정 저장
            question.create_date = timezone.now() # 작성일시 저장
            question.save() # 데이터 실제로 저장
            return redirect('gw:index')
    else:
        form = QuestionForm()
    context = {'form' : form}
    return render(request, 'gw/question_form.html', context) 

              
@login_required(login_url='common:login')
def question_modify(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author: # 글쓴이와 수정자 확인
        messages.error(request, '수정 권한 없음!') # message 로 넌필드 오류 발생시킴
        return redirect('gw:detail', question_id=question.id)
    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question) # intance를 기준으로 QuestionForm을 생성하지만 request.POST 값으로 덮어씀
        if form.is_valid():
            question = form.save(commit=False)
            question.modify_date = timezone.now() # 수정일시 저장
            question.save()
            return redirect('gw:detail', question_id=question.id)
    else:
        form = QuestionForm(instance=question) # 수정 시, 기존 값을 항목에 채워넣기 위해 instance 사용
    context = {'form' : form}
    return render(request, 'gw/question_form.html', context)
            
@login_required(login_url='common:login')
def question_delete(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '삭제 권한 없음!')
        return redirect('gw:detail', question_id=question.id)
    question.delete()
    return redirect('gw:index')

@login_required(login_url='common:login')
def answer_modify(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '수정 권한 없음!')
        return redirect('gw:detail', question_id=answer.question.id)
    if request.method == 'POST':
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.modify_date = timezone.now()
            answer.save()
            return redirect('gw:detail', question_id=answer.question.id)
    else:
        form = AnswerForm(instance=answer)
    context = {'form' : form}
    return render(request, 'gw/answer_form.html', context)

@login_required(login_url='common:login')
def answer_delete(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '삭제 권한 없음!')
    else:
        answer.delete()
    return redirect('gw:detail', question_id=answer.question.id)