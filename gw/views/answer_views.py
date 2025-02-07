from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from ..models import Question, Answer
from ..form import QuestionForm, AnswerForm



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