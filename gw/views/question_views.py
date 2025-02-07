from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from ..models import Question
from ..form import QuestionForm



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