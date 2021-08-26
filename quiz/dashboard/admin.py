from django.contrib import admin
from django import forms
from django.utils import tree

from .models import QuestionType, SubjectInfo, QuestionInfo, AnswerInfo, UserProgress
# Register your models here.

admin.site.register(QuestionType)
admin.site.register(SubjectInfo)


"""
    Custom Validations
"""

class QuestionForm(forms.ModelForm):
    def clean(self):
        score = self.cleaned_data['max_score']
        max_score  = self.cleaned_data['subject'].max_score
        min_score = self.cleaned_data['subject'].min_score
        
        if score > max_score:
            raise forms.ValidationError({'max_score': "Score should be less than or equal to "+ str(int(max_score))})


@admin.register(QuestionInfo)
class QuestionAdmin(admin.ModelAdmin):
    form = QuestionForm


class AnswerForm(forms.ModelForm):
    """
        Custom Validations
    """
    def clean(self):
        answer = self.cleaned_data['answer']
        if str(answer) == "None":
            raise forms.ValidationError({'option': "Answer or Option Field Required."})


@admin.register(AnswerInfo)
class AnswersAdmin(admin.ModelAdmin):
    form = AnswerForm
    

class UserProgressForm(forms.ModelForm):
    """
        Custom Validations in admin panel for answer columns
    """    
    def clean(self):
        mcq_answer = self.cleaned_data['mcq_answer']
        one_word_answer  = self.cleaned_data['one_word_answer']
        
        if mcq_answer and one_word_answer:
            raise forms.ValidationError({'right_choice': "Cannot have 2 choices for a question"})



@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    form = UserProgressForm
    

