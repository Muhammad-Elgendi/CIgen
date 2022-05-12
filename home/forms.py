from django import forms
from django.contrib.auth import get_user_model
import pandas as pd
import random


class QuizForm(forms.Form):

    def __init__(self, *args, **kwargs):
        quiz_df = kwargs.pop('df')        
        random_seed = kwargs.pop('seed')

        super().__init__(*args, **kwargs)
        questions = [q for q in quiz_df.columns if q.lower() not in ['answers','answer','ans','select'] ]
        answers = quiz_df['answers']
        fields_names = []

        # if number of questions to be shown is used
        random_choose = False
        must_show = {}
        if 'select' in quiz_df.columns:
            random_choose = True
            questions_count = int(quiz_df['select'].iloc[0])
            non_required_questions = [col for col in questions if col[0] != '*']
            pool_of_candidate_questions = pd.Series(non_required_questions).sample(n=questions_count, random_state=random_seed, replace=True).unique()


        for num ,question in enumerate(questions):

            if question[0] != '*':       # exclude required questions             
                if question in pool_of_candidate_questions:
                    must_show['q'+str(num+1)] = True
                else:
                    must_show['q'+str(num+1)] = False
            else:
                must_show['q'+str(num+1)] = True

            if not random_choose:
                must_show['q'+str(num+1)] = True
            
            if must_show['q'+str(num+1)]:
                fields_names.append('q'+str(num+1))

            # extract multiple-choice questions
            if quiz_df[question].iloc[0] not in ['#TEXT#','#NUMBER#']:

                choices_for_question = quiz_df[questions[num]].dropna()

                CHOICES = []
                for index ,option in enumerate(choices_for_question):
                    CHOICES.append(("op"+str(index+1),option))

                # apply random shuffling for choices
                random.shuffle(CHOICES)

                if must_show['q'+str(num+1)]:
                    # check if question is required
                    if questions[num][0] == '*':
                        self.fields['q'+str(num+1)] = forms.ChoiceField(required=True,widget=forms.RadioSelect(),choices=CHOICES,label=questions[num]) 
                    else:
                        self.fields['q'+str(num+1)] = forms.ChoiceField(required=False,widget=forms.RadioSelect(),choices=CHOICES,label=questions[num]) 


            # handle text inputs qustions (questions annotated be #TEXT#)
            elif(quiz_df[question].iloc[0] == '#TEXT#'):
                # check if question is required
                if questions[num][0] == '*':
                    self.fields['q'+str(num+1)] = forms.CharField(required=True,label=questions[num],widget=forms.Textarea(attrs={"name":'q'+str(num+1),"class":"form-control","placeholder":"Your Answer","rows":"1"}))
                else:
                    self.fields['q'+str(num+1)] = forms.CharField(required=False,label=questions[num],widget=forms.Textarea(attrs={"name":'q'+str(num+1),"class":"form-control","placeholder":"Your Answer","rows":"1"}))

            
            # handle text inputs qustions (questions annotated be #NUMBER#)
            elif(quiz_df[question].iloc[0] == '#NUMBER#'):
                if questions[num][0] == '*':
                    self.fields['q'+str(num+1)] = forms.IntegerField(required=True,label=questions[num],widget=forms.NumberInput(attrs={"class":"form-control"}))
                else:
                    self.fields['q'+str(num+1)] = forms.IntegerField(required=False,label=questions[num],widget=forms.NumberInput(attrs={"class":"form-control"}))

        # apply random shuffling for questions
        random.shuffle(fields_names)
        self.order_fields(fields_names)


class InviteForm(forms.Form):
    links = forms.CharField(required=True,widget=forms.Textarea(attrs={"id":"links","name":"links","class":"form-control","placeholder":"Enter Your Links (One Link per Line)","rows":"3"}))
