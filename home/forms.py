from django import forms
from django.contrib.auth import get_user_model
import pandas as pd
import random


class QuizForm(forms.Form):

    def __init__(self, *args, **kwargs):
        quiz_df = kwargs.pop('df')
        super().__init__(*args, **kwargs)
        questions = [q for q in quiz_df.columns if q.lower() not in ['answers','answer','ans'] ]

        # apply random shuffling for questions
        # random.shuffle(questions)

        answers = quiz_df['answers']
        for num ,question in enumerate(questions):

            # extract multiple-choice questions
            if quiz_df[question].iloc[0] not in ['#TEXT#','#NUMBER#']:

                choices_for_question = quiz_df[questions[num]].dropna()

                # apply random shuffling for choices
                # random.shuffle(choices_for_question)

                CHOICES = []
                for index ,option in enumerate(choices_for_question):
                    CHOICES.append(("op"+str(index+1),option))
                self.fields['q'+str(num+1)] = forms.ChoiceField(widget=forms.RadioSelect,choices=CHOICES,label=questions[num]) 

            # handle text inputs qustions (questions annotated be #TEXT#)
            elif(quiz_df[question].iloc[0] == '#TEXT#'):
                self.fields['q'+str(num+1)] = forms.CharField(label=questions[num],widget=forms.Textarea(attrs={"name":'q'+str(num+1),"class":"form-control","placeholder":"Your Answer","rows":"1"}))
            
            # handle text inputs qustions (questions annotated be #NUMBER#)
            elif(quiz_df[question].iloc[0] == '#NUMBER#'):
                self.fields['q'+str(num+1)] = forms.IntegerField(label=questions[num],widget=forms.NumberInput)

    # def clean(self):
    #     data = self.cleaned_data
    #     password = self.cleaned_data.get('password')
    #     password2 = self.cleaned_data.get('password2')
    #     if password != password2:
    #         raise forms.ValidationError("Passwords mush match.")
    #     return data

    # def clean_username(self):
    #     username = self.cleaned_data.get('username')
    #     User = get_user_model()
    #     qs = User.objects.filter(username=username)
    #     if qs.exists():
    #         raise forms.ValidationError("User name is taken")      
    #     return username

    # def clean_email(self):
    #     email = self.cleaned_data.get('email')
    #     User = get_user_model()
    #     qs = User.objects.filter(email=email)
    #     if qs.exists():
    #         raise forms.ValidationError("This email is already registered")      
    #     return email