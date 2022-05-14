from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from dashboard.models import Quiz, Answer
from .forms import QuizForm, InviteForm
from django.contrib import messages
from django.utils import timezone
from dateutil.parser import parse
from datetime import timedelta
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
    user_agent = request.META.get('HTTP_USER_AGENT')
    cookie = request.COOKIES.get('CIgen_VQ')

    seed_str = str(ip)+str(user_agent)+str(x_forwarded_for)+str(cookie)

    # for testing, comment the following, and set any number as seed
    seed = hashlib.sha1(seed_str.encode('utf-8')).hexdigest()
    seed = ''.join([s for s in seed if s.isdigit()])
    seed = int(seed[:9])

    print(ip, user_agent, cookie, x_forwarded_for) 
    print("seed:",seed)

    try:
        quiz = Quiz.objects.get(pk=quiz_id)
    except Quiz.DoesNotExist:
        raise Http404("Quiz does not exist")

    # if quiz exists
    quiz_df = pd.read_json(quiz.quiz, orient='split')

    if request.method == "GET":
        form = QuizForm(request.POST or None, df=quiz_df, seed=seed, initial={'start': str(timezone.now())})
        context = {"form":form,"quiz":quiz, "seed":seed}
        response = render(request,"home/quiz.html",context)
        # check if this is the first visit to the CIgen's quiz
        if cookie:
            print("cookie",cookie)
            cookie = int(cookie)+1            
            response.set_cookie(key='CIgen_VQ', value=cookie)  
        else:
            cookie = 2           
            response.set_cookie(key='CIgen_VQ', value=cookie) 
        return response
    
    if request.method == "POST":
        form = QuizForm(request.POST or None, df=quiz_df, seed=seed)
        context = {"form":form,"quiz":quiz, "seed":seed}        
        if form.is_valid():
            submit_time = str(timezone.now())
            student_answers = form.cleaned_data
            time_taked = parse(submit_time) - parse(student_answers.get('start'))

            # to get the "total minutes"
            time_taked = time_taked / timedelta(minutes=1)
            time_taked = round(time_taked,2)

            questions = [q for q in quiz_df.columns if q.lower() not in ['answers','answer','ans'] and quiz_df[q].iloc[0] not in ['#TEXT#','#NUMBER#']]
            
            score = None
            total = None          

            # if quiz type not an attendace
            if 'answers' in quiz_df.columns:

                # calculate score for student
                score = 0
                total = 0

                answers = quiz_df['answers']
                for ques,ans in student_answers.items():
                    if 'op'in str(ans) and 'q' in ques:                    
                        total +=1
                        question_no = int(ques.split('q')[1])-1
                        choice = int(ans.split('op')[1])

                        if answers[question_no] == choice:
                            score +=1 

                print("scored : ",str(score)+"/"+str(total),"percent : ", str(round(score/total*100,2))+"%")

            result = "Success" if score == None or score >= total/2  or total == 0 else "Fail"

            # if timed-quiz type
            if 'time' in quiz_df.columns:
                accepted_time = int(quiz_df['time'].iloc[0])
                answer_status = "In time" if time_taked <= accepted_time else "Late"
                student_answers.update({ 'answer status' : answer_status })

            student_answers.update({
                "score":score,
                "result":result,
                "total":total,
                "finish":submit_time,
                "answer time (minutes)": time_taked,
            })

            saved_answer, created = Answer.objects.get_or_create(     
                quiz = quiz,
                answer = json.dumps(student_answers),
                created_at = timezone.now()
            )    

            form = QuizForm(df=quiz_df, seed=seed)

            return redirect('home:result', answer_id=saved_answer.id)

        response = render(request,"home/quiz.html",context)
        # check if this is the first visit to the CIgen's quiz
        if cookie:
            print("cookie",cookie)
            cookie = int(cookie)+1            
            response.set_cookie(key='CIgen_VQ', value=cookie)  
        else:
            cookie = 2           
            response.set_cookie(key='CIgen_VQ', value=cookie) 
        return response

      
   
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
        mylist = None
        if form.is_valid():
            links = form.cleaned_data.get('links')
            ips_with_quizes = links.replace('quiz','quiz/'+str(quiz.id))
            links = [link.strip() for link in ips_with_quizes.split('\r\n')]

            QRs = []

            for index, link in enumerate(links):
                if len(link) > 0:

                    qr = qrcode.QRCode(                  
                        box_size=10,
                        border=1,
                    )

                    qr.add_data(link)

                    # QR in color are not compatible with all readers
                    # img = qr.make_image(fill_color="white", back_color=(95, 207, 128))

                    img = qr.make_image()

                    image_file = 'generated/QRcode'+str(index)+".png"

                    # add accessible img URL
                    QRs.append(image_file)
                    
                    # Saving as an image file
                    img.save('staticfiles/'+image_file)

            mylist = zip(links , QRs)
        return render(request,"home/invite.html",{"form":form, "quiz":quiz, "qr": mylist })
    else:
        return redirect("home:index")

