from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from django import forms
from django.contrib import messages

from .models import Quiz
from .models import Answer

import pandas as pd

class UploadForm(forms.Form):
    file_to_upload = forms.FileField()

class QuizAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [path('upload-quiz/',self.upload_quiz)]
        return new_urls + urls

    def upload_quiz(self,request):
        if request.method == "POST":
            quiz_file = request.FILES["file_to_upload"]
            
            print(quiz_file.read())

            quiz_df = pd.read_excel(quiz_file)

            # quiz format
            # {'q1':{'question':'test question?','choices':[{'a':'right answer'}]},'answers':{'q1':'a'}}
            # answer format
            # {	"name": "fdgdfgfdgfdg",	"phone": "0101424242",	"q1": "a"}

            Quiz.objects.update_or_create(
                name='test2',
                quiz = {'test':'test'}
            )

        form = UploadForm()
        data = {"form":form}
        return render(request,"admin/dashboard/quiz/upload.html",data)

admin.site.register(Quiz, QuizAdmin)



class AnswerAdmin(admin.ModelAdmin):
    list_display = ['get_quiz', 'created_at']

    def get_quiz(self, obj):
        return obj.quiz.name
    get_quiz.admin_order_field  = 'quiz'  #Allows column order sorting
    get_quiz.short_description = 'Quiz'  #Renames column head

# Register your models here.
admin.site.register(Answer, AnswerAdmin)


