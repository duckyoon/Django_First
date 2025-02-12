from django.shortcuts import render, get_object_or_404, redirect, resolve_url
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
            # return redirect('gw:detail', question_id=question.id)
            # HTML을 호출하는 URL 뒤에 #page를 붙여주면 해당 페이지가 호출되면서 해당 앵커로 스크롤이 이동
            # resolve_url은 실제 호출되는 url 문자열을 리턴하는 장고의 함수
            return redirect('{}#answer_{}'.format(
                resolve_url('gw:detail', question_id=question.id), answer.id
            ))
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
            # return redirect('gw:detail', question_id=answer.question.id)
            return redirect('{}#answer_{}'.format(
                resolve_url('gw:detail', question_id=answer.question.id), answer.id
            ))
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

@login_required(login_url='common:login')
def answer_vote(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user == answer.author:
        messages.error(request, '본인이 작성한 글은 추천할 수 없음')
    else:
        answer.voter.add(request.user)
    # return redirect('gw:detail', question_id=answer.question.id)
    return redirect('{}#answer_{}'.format(
            resolve_url('gw:detail', question_id=answer.question.id), answer.id
    ))
