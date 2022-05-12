from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from dashboard.models import Quiz, Answer
from .forms import QuizForm, InviteForm
from django.contrib import messages
from django.utils import timezone
import pandas as pd
import json
import qrcode
import random
import hashlib


# Create your views here.
def index(request):

    # return HttpResponse("Hello, world. You're at the home index.")

    # latest_quiz_list = Quiz.objects.order_by('-created_at')[:5]
    # output = ', '.join([q.name for q in latest_quiz_list])
    # return HttpResponse(output)

    return render(request,"home/index.html",{})



def view_quiz(request,quiz_id):
    # TODO check for cookie in the user browser to know if they take
    # this quiz before
    ip = request.META.get('REMOTE_ADDR')
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    user_agent = request.META['HTTP_USER_AGENT']
    seed_str = str(ip)+str(user_agent)+str(x_forwarded_for)

    # for testing, comment the following, and set any number as seed
   
    seed = hashlib.sha1(seed_str.encode('utf-8')).hexdigest()
    seed = ''.join([s for s in seed if s.isdigit()])
    seed = int(seed[:9])

    print(ip,user_agent,x_forwarded_for) 
    print(seed)

    try:
        quiz = Quiz.objects.get(pk=quiz_id)
    except Quiz.DoesNotExist:
        raise Http404("Quiz does not exist")

    # if quiz exists
    quiz_df = pd.read_json(quiz.quiz, orient='split')
    form = QuizForm(request.POST or None, df=quiz_df, seed=seed)

    if request.method == "GET":
        context = {"form":form,"quiz":quiz, "seed":seed}
        return render(request,"home/quiz.html",context)
    
    if request.method == "POST":
        context = {"form":form,"quiz":quiz, "seed":seed}        
        if form.is_valid():
            student_answers = form.cleaned_data
            questions = [q for q in quiz_df.columns if q.lower() not in ['answers','answer','ans'] and quiz_df[q].iloc[0] not in ['#TEXT#','#NUMBER#']]
            answers = quiz_df['answers']

            # calculate score for student
            score = 0
            total = 0
            for ques,ans in student_answers.items():

                if 'op'in str(ans) and 'q' in ques:                    
                    total +=1
                    question_no = int(ques.split('q')[1])-1
                    choice = int(ans.split('op')[1])

                    if answers[question_no] == choice:
                        score +=1 

            print("scored : "+str(score))

            result = "Success" if score >= total/2  or total == 0 else "Fail"

            student_answers.update({
                "score":score,
                "result":result,
                "total":total
            })

            saved_answer, created = Answer.objects.get_or_create(     
                quiz = quiz,
                answer = json.dumps(student_answers),
                created_at = timezone.now()
            )    

            form = QuizForm(df=quiz_df, seed=seed)

            return redirect('home:result', answer_id=saved_answer.id)

        return render(request,"home/quiz.html",context)

      
   
def view_result(request,answer_id):

    # TODO set cookie in the user browser

    if request.method == "GET" and request.META.get('HTTP_REFERER'):
        try:
            answer = Answer.objects.get(pk=answer_id)
        except Answer.DoesNotExist:
            raise Http404("Answer does not exist")

        messages.success(request, 'Your answers have been submitted.')

        # convert answer json object back to dict
        answer = json.loads(answer.answer)

        context = {"score":answer.get('score'),
                "result":answer.get('result'),
                "total":answer.get('total')
                }
        return render(request,"home/success.html",context)
    return redirect("home:index")

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

            QRs = []

            for index, link in enumerate(links):
                if len(link) > 0:
                    # Encoding data using make() function
                    img = qrcode.make(link)

                    image_file = 'generated/QRcode'+str(index)+".png"

                    # add accessible img URL
                    QRs.append(image_file)
                    
                    # Saving as an image file
                    img.save('staticfiles/'+image_file)

            return render(request,"home/invite.html",{"quiz":quiz,"qr":QRs})
    else:
        return redirect("home:index")

