from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from dashboard.models import Quiz, Answer
from .forms import QuizForm, InviteForm
from django.contrib import messages
from django.utils import timezone
import pandas as pd
import json

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

    if request.method == "GET":
        context = {"form":form,"quiz":quiz}
        return render(request,"home/quiz.html",context)
    
    if request.method == "POST":
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

            result = "Success" if score >= len(questions)/2 else "Fail"

            student_answers.update({
                "score":score,
                "result":result
            })

            saved_answer, created = Answer.objects.get_or_create(     
                quiz = quiz,
                answer = json.dumps(student_answers),
                created_at = timezone.now()
            )    

            form = QuizForm(df=quiz_df)

            return redirect('result', answer_id=saved_answer.id)

        return redirect('/')
      
   
def view_result(request,answer_id):

    if request.method == "GET" and request.META.get('HTTP_REFERER'):
        try:
            answer = Answer.objects.get(pk=answer_id)
        except Answer.DoesNotExist:
            raise Http404("Answer does not exist")

        messages.success(request, 'Your answers have been submitted.')

        # convert answer json object back to dict
        answer = json.loads(answer.answer)

        context = {"score":answer.get('score'),
                "result":answer.get('result')
                }
        return render(request,"home/success.html",context)
    return redirect("/")

def invite_to_quiz(request,quiz_id):
    try:
        quiz = Quiz.objects.get(pk=quiz_id)
    except Quiz.DoesNotExist:
        raise Http404("Quiz does not exist")

    if request.method == 'GET':
        form = InviteForm()
        return render(request,"home/invite.html",{"quiz":quiz,"form":form})
    elif request.method == 'POST':
        form = InviteForm(request.POST or None)
        if form.is_valid():
            links = form.cleaned_data.get('links')
            ips_with_quizes = links.replace('quiz','quiz/'+str(quiz.id))
            links = [link.strip() for link in ips_with_quizes.split('\r\n')]
            print(links)
            return render(request,"home/invite.html",{"quiz":quiz,"qr":""})
    else:
        return redirect("/")

