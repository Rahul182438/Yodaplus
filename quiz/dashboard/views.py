from django.db.models import query
from django.shortcuts import render, redirect
from django.http import HttpResponse, request
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.edit import FormView
from django.views.generic import ListView, DetailView
from .models import *



@method_decorator(login_required(login_url='registration:login'),name='dispatch')
class DashboardView(ListView):

    
    template_name ='dashboard/test.html'
    context_object_name = 'quiz_types'
    

    def get_queryset(self):
        query_set = {'types_obj': QuestionType.objects.all(), 
                    'subjects_obj': SubjectInfo.objects.all()}
        return query_set

    def post(self, *args, **kwargs):
        postdata = self.request.POST.copy()
        
        subject_id = postdata.get('subject')
        type_id = postdata.get('type')
        # subject_info = SubjectInfo.objects.get(id=subject_id)
        # questions_info = QuestionInfo.objects.get(subject_id=subject_info.id)
        return redirect('dashboard:quiz_questions',pk=subject_id,type_id=type_id)
    
        

class QuiestionView(DetailView):

    template_name = 'dashboard/questions.html'
    context_object_name = 'quiz'

    def get_object(self, queryset=None):

        query_set = {'questions_obj': QuestionInfo.objects.filter(subject=self.kwargs.get("pk"),type=self.kwargs.get("type_id")),
                    'answers_obj': AnswerInfo.objects.all()}

        return query_set
    

