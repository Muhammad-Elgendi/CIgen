from django.contrib import admin, messages
from django.urls import path, reverse
from django.shortcuts import render, redirect
from django import forms
from .models import Quiz, Answer
import pandas as pd
import json
from django.utils.safestring import mark_safe
from django.http import FileResponse, HttpResponse
from io import BytesIO
import zipfile
from pathlib import Path
import os
import shutil



class UploadForm(forms.Form):
    file_to_upload = forms.FileField()
    images_to_upload = forms.FileField(required=False)


class QuizAdmin(admin.ModelAdmin):
    list_display = ['name', 'get_view_link', 'get_invite_link', 'created_at']
    list_display_links = ['name']

    def get_view_link(self, obj):
        return mark_safe('<a href="%s">Take Quiz</a>' % reverse('home:quiz', kwargs={'quiz_id':obj.id }))
    get_view_link.allow_tags = True
    get_view_link.admin_order_field  = 'quiz'  #Allows column order sorting
    get_view_link.short_description = 'View'  #Renames column head

    def get_invite_link(self, obj):
        return mark_safe('<a href="%s">Invite Participants</a>' % reverse('home:invite', kwargs={'quiz_id':obj.id }))
    get_invite_link.allow_tags = True
    get_invite_link.admin_order_field  = 'quiz'  #Allows column order sorting
    get_invite_link.short_description = 'Invitation'  #Renames column head

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [
            path('upload-quiz/',self.upload_quiz),
            path('<int:quiz_id>/export/',self.export_answers),
            ]
        return new_urls + urls

    def export_answers(self,request,quiz_id):
        quiz = Quiz.objects.get(id=quiz_id)
        quiz_df = pd.read_json(quiz.quiz, orient='split')
        answers = quiz.answer_set.all()
        if not answers:
            return redirect('home:quiz',quiz_id=quiz_id)
        df = pd.DataFrame(json.loads(answers[0].answer), index=[0])
        for idx, answer in enumerate(answers):
            if idx != 0:
                temp = pd.DataFrame(json.loads(answer.answer), index=[0])
                df = pd.concat([df, temp],axis=0,ignore_index=True)

        # render questions as columns
       
        new_columns = {}
        for num,col in enumerate(df.columns):
            if 'q' in df.columns[num]:
                new_columns.update(
                    {   
                        df.columns[num] : quiz_df.columns[int(df.columns[num].split('q')[1])-1]
                    }
                )

                # render answers not the indexes

                # get choices
                choices = df[col].unique()
                for choice in choices:
                    if 'op' in str(choice):
                        index_of_choice = int(choice.split('op')[1])-1
                        col_in_quiz = quiz_df.columns[int(col.split('q')[1])-1]

                        df[col].replace(
                            { choice : quiz_df[col_in_quiz].iloc[index_of_choice] },
                            inplace=True
                            )

        # apply new columns names
        df.rename(columns = new_columns, inplace = True)

        # add percent column to dataframe if quiz type
        if 'total' in df.columns:
            df['percent'] = round(df['score'] / df['total'] * 100, 2) if df['total'].any() else 0

        # download answers dataframe
        with BytesIO() as b:
            # Use the StringIO object as the filehandle.
            writer = pd.ExcelWriter(b, engine='openpyxl')
            df.to_excel(writer, sheet_name=quiz.name + ' answers')
            writer.save()
            # Set up the Http response.
            filename = quiz.name+" answers.xlsx"
            response = HttpResponse(
                b.getvalue(),
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            response['Content-Disposition'] = 'attachment; filename=%s' % filename
            return response

    def get_filenames(self,path_to_zip):
            """ return list of filenames inside of the zip folder """
            with zipfile.ZipFile(path_to_zip, 'r') as zip:
                return zip.namelist()

    def upload_quiz(self,request):
        df = None
        if request.method == "POST":
            quiz_file = request.FILES["file_to_upload"]
            if 'images_to_upload' in request.FILES:
                images_file = request.FILES["images_to_upload"]
                current_user = request.user
                images_path = "public/media_root/images/"+quiz_file.name.split(".")[0].replace(" ","_")+"/"


                # remove old images for this quiz if any
                if os.path.exists(images_path) and os.path.isdir(images_path):
                    shutil.rmtree(images_path)

                # create quiz images folder if not existed
                Path(images_path).mkdir(parents=True, exist_ok=True)

                # decompress images file
                with zipfile.ZipFile(images_file, 'r') as zip_ref:
                    zip_ref.extractall(images_path)
                    
                    # extract images
                    # for img in zip_ref.namelist():
                    #     zip_ref.extract(img, images_path)
                
                # get images names from compressed file
                img_names = self.get_filenames(images_file)
            
            try:
                df = pd.read_excel(quiz_file, dtype=str)

                if 'images_to_upload' in request.FILES:
                    Quiz.objects.update_or_create(
                        name = quiz_file.name.split(".")[0],
                        quiz = df.to_json(orient='split'),
                        images = json.dumps(img_names)
                    )
                else:
                    Quiz.objects.update_or_create(
                        name = quiz_file.name.split(".")[0],
                        quiz = df.to_json(orient='split')
                    )
            except Exception as e:
                messages.warning(request, 'Your File Is Invaild.')                
                print(e)

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
    list_display = ['get_quiz', 'get_score', 'get_total', 'get_percent', 'created_at']

    def get_quiz(self, obj):
        return obj.quiz.name + " Answer"
    get_quiz.admin_order_field  = 'quiz'  #Allows column order sorting
    get_quiz.short_description = 'Answers'  #Renames column head

    def get_score(self, obj):
        return json.loads(obj.answer).get('score')
    get_score.admin_order_field  = 'answer'  #Allows column order sorting 
    get_score.short_description = 'Score'  #Renames column head

    def get_total(self, obj):
        return json.loads(obj.answer).get('total')
    get_total.admin_order_field  = 'answer'  #Allows column order sorting 
    get_total.short_description = 'Total'  #Renames column head

    def get_percent(self, obj):
        # score/total*100
        answer = json.loads(obj.answer)
        if answer.get('score') and answer.get('total'):
            return round( int(answer.get('score')) / int(answer.get('total')) * 100 , 2)
    get_percent.admin_order_field  = 'answer'  #Allows column order sorting 
    get_percent.short_description = 'percent'  #Renames column head


# Register your models here.
admin.site.register(Answer, AnswerAdmin)