from django.shortcuts import render
from django.http import HttpResponse
from dashboard.models import Quiz
from django.http import Http404

import pandas as pd

from .forms import QuizForm
from django.contrib import messages


# Create your views here.
def index(request):
    # return HttpResponse("Hello, world. You're at the home index.")
    latest_quiz_list = Quiz.objects.order_by('-created_at')[:5]
    output = ', '.join([q.name for q in latest_quiz_list])
    return HttpResponse(output)


def view_quiz(request,quiz_id):
    try:
        quiz = Quiz.objects.get(pk=quiz_id)
    except Quiz.DoesNotExist:
        raise Http404("Quiz does not exist")

    # if quiz exists
    quiz_df = pd.read_json(quiz.quiz, orient='split')
    form = QuizForm(request.POST or None, df=quiz_df)
    context = {"form":form,"quiz":quiz}

    if form.is_valid():
        print(form.cleaned_data)
    return render(request,"home/quiz.html",context)


def submit_quiz(request,quiz_id):
    try:
        quiz = Quiz.objects.get(pk=quiz_id)
    except Quiz.DoesNotExist:
        raise Http404("Quiz does not exist")

    # if quiz exists
    quiz_df = pd.read_json(quiz.quiz, orient='split')
    form = QuizForm(request.POST or None, df=quiz_df)

    if form.is_valid():
        student_answers = form.cleaned_data
        questions = [q for q in quiz_df.columns if q.lower() not in ['answers','answer','ans'] and quiz_df[q].iloc[0] not in ['#TEXT#','#NUMBER#']]
        answers = quiz_df['answers']

        # calculate score for student
        score = 0
        for ques,ans in student_answers.items():

            if 'op'in ans and 'q' in ques:
                question_no = int(ques.split('q')[1])-1
                choice = int(ans.split('op')[1])

                if answers[question_no] == choice:
                    score +=1 

        print("scored : "+str(score))

        messages.success(request, 'Your answers have been submitted.')

        result = "Success" if score >= len(questions)/2 else "Fail"
        
        context = {"score":score,
                   "result":result
                   }

    return render(request,"home/success.html",context)