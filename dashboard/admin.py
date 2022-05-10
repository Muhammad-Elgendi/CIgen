from django.contrib import admin
from django.urls import path
from django.shortcuts import render, redirect
from django import forms
from django.contrib import messages
from django.urls import reverse
from .models import Quiz
from .models import Answer
import pandas as pd
import json
from django.utils.safestring import mark_safe


class UploadForm(forms.Form):
    file_to_upload = forms.FileField()

class QuizAdmin(admin.ModelAdmin):
    list_display = ['name', 'get_view_link', 'get_invite_link', 'created_at']
    list_display_links = ['name']

    def get_view_link(self, obj):
        return mark_safe('<a href="%s">Take Quiz</a>' % reverse('quiz', kwargs={'quiz_id':obj.id }))
    get_view_link.allow_tags = True
    get_view_link.admin_order_field  = 'quiz'  #Allows column order sorting
    get_view_link.short_description = 'View'  #Renames column head

    def get_invite_link(self, obj):
        return mark_safe('<a href="%s">Invite Participants</a>' % reverse('invite', kwargs={'quiz_id':obj.id }))
    get_invite_link.allow_tags = True
    get_invite_link.admin_order_field  = 'quiz'  #Allows column order sorting
    get_invite_link.short_description = 'Invitation'  #Renames column head

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [path('upload-quiz/',self.upload_quiz)]
        return new_urls + urls

    def upload_quiz(self,request):
        df = None
        if request.method == "POST":
            quiz_file = request.FILES["file_to_upload"]
            
            try:
                df = pd.read_excel(quiz_file)

                Quiz.objects.update_or_create(
                    name = quiz_file.name.split(".")[0],
                    quiz = df.to_json(orient='split')
                )
            except:
                messages.warning(request, 'Your File Is Invaild.')                

        form = UploadForm()
        data = {"form":form,
                "df":"Upload Your File To Preview It Here"
                }

        if isinstance(df, pd.DataFrame):
            data.update( { "df": df.to_html() })
            messages.success(request, 'Your File Has Been Uploaded Successfully.')


            
        if request.user.is_active and request.user.is_superuser:
            return render(request,"admin/dashboard/quiz/upload.html",data)
        else:
            return redirect('admin:index')


admin.site.register(Quiz, QuizAdmin)



class AnswerAdmin(admin.ModelAdmin):
    list_display = ['get_quiz', 'get_score', 'created_at']

    def get_quiz(self, obj):
        return obj.quiz.name + " Answer"
    get_quiz.admin_order_field  = 'quiz'  #Allows column order sorting
    get_quiz.short_description = 'Answers'  #Renames column head

    def get_score(self, obj):
        return json.loads(obj.answer).get('score')
    get_score.admin_order_field  = 'answer'  #Allows column order sorting 
    get_score.short_description = 'Score'  #Renames column head

# Register your models here.
admin.site.register(Answer, AnswerAdmin)


