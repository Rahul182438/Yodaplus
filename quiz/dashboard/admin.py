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
    

class AnswerInline(admin.TabularInline):
    model = AnswerInfo
    extra = 4

class AnswerQuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]

admin.site.register(QuestionInfo,AnswerQuestionAdmin)

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
    

