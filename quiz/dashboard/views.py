from django.db.models import query
from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from django.http import HttpResponse, request
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.edit import FormView
from django.views.generic import ListView, DetailView
from django.db.models import Count, QuerySet


from .models import *


@method_decorator(login_required(login_url='registration:login'),name='dispatch')
class DashboardView(ListView):

    
    template_name ='dashboard/quiz_type.html'
    context_object_name = 'quiz_types'
    

    def get_queryset(self):
        query_set = {'types_obj': QuestionType.objects.all(), 
                    'subjects_obj': SubjectInfo.objects.all(),
                    }
        return query_set

    def post(self, *args, **kwargs):
        postdata = self.request.POST.copy()
        
        subject_id = postdata.get('subject')

        return redirect('dashboard:quiz_questions',pk=subject_id)
    
        

class QuiestionView(DetailView):

    template_name = 'dashboard/questions.html'
    context_object_name = 'quiz'

    def get_object(self, queryset=None):
        complete = True
        max_score, min_score,score_earned = 0, 0, 0
        msg = ""
        subject_obj = SubjectInfo.objects.get(id=self.kwargs.get("pk"))
        max_score = int(subject_obj.max_score)
        min_score = int(subject_obj.min_score)
        total_time = subject_obj.interval
        time_used = 0
        user_progress_obj = UserProgress.objects.filter(user=self.request.user,subject=self.kwargs.get("pk"))
        
        my_answer_list = []
        quest_ids_list = []
        count = 0
        if user_progress_obj:
                
            for progress in user_progress_obj:

                complete = progress.is_complete
                if progress.is_complete == False:
                    quest_ids_list.append(progress.question_id)
                else:
                    count += 1
                time_used = progress.time
                if progress.mcq_answer and progress.mcq_answer.is_correct == True:
                    score_earned += int(progress.question.max_score)
                elif progress.one_word_answer:
                    
                    answers_obj = AnswerInfo.objects.get(question=progress.question,is_correct=True)

                    if answers_obj:
                        if str(answers_obj.answer) == str(progress.one_word_answer):
                            score_earned += int(progress.question.max_score)        
                            
            if score_earned == max_score or score_earned == min_score :
                msg = "You have passed the test with "+str(score_earned)+'/'+str(max_score)+" marks."

            elif score_earned < min_score:
                msg = "You have failed the test. Your Score is "+str(score_earned)+'/'+str(max_score)
            elif score_earned > min_score and score_earned < max_score:
                msg = "You have passed the test. Your Score is "+str(score_earned)+'/'+str(max_score)

        else:
            complete = True

        if quest_ids_list:
            questions_obj = QuestionInfo.objects.filter(subject=self.kwargs.get("pk"),id__in=quest_ids_list)
        else:
            questions_obj = QuestionInfo.objects.filter(subject=self.kwargs.get("pk"))

        query_set = {'questions_obj': questions_obj,
                    'answers_obj': AnswerInfo.objects.all(),
                    'user_progress_obj':user_progress_obj,
                    'complete': complete,
                    'msg': msg,
                    'my_answer_list':my_answer_list,
                    'min_score':min_score,
                    'time_used':time_used,
                    'question_count':count
                    }

        return query_set



def save_user_progress(request,pk):

    postdata = request.POST.copy()
    for data in postdata:
        
        try:
            answers_obj = AnswerInfo.objects.get(question_id=data,answer=postdata[data])
        except:
            answers_obj = None
        try:
            progress_obj = UserProgress.objects.get(user=request.user,question_id=data,subject_id=pk)
        except:
            progress_obj = None            
        if progress_obj:
            if answers_obj:
                progress_obj.mcq_answer_id = answers_obj.id
            else:
                if postdata[data] == 'none':
                    progress_obj.is_complete = True
                else:
                    progress_obj.one_word_answer = postdata[data]

            if postdata[data] == "true":
                complete = True

            progress_obj.save()
        else:
            
            if  data != 'complete' and data != 'time':
                user_progress_obj = UserProgress()
                user_progress_obj.user = request.user
                
                user_progress_obj.question_id = data
                user_progress_obj.subject_id = pk
                if answers_obj:
                    user_progress_obj.mcq_answer_id = answers_obj.id
                else:
                    user_progress_obj.one_word_answer = postdata[data]

                user_progress_obj.save()
            elif data == 'complete':
                if postdata[data] == "true":
                    complete = True
                    user_progress_obj = UserProgress.objects.filter(user=request.user,subject_id=pk)
                    for progress in user_progress_obj:
                        progress.is_complete = complete
                        progress.save()
            elif data == 'time' and postdata[data]:
                user_progress_obj = UserProgress.objects.filter(user=request.user,subject_id=pk)
                for progress in user_progress_obj:
                    progress.time = float(postdata[data])
                    progress.save()                

    return JsonResponse({'success':'True'})





@method_decorator(login_required(login_url='registration:login'),name='dispatch')
class ReportView(ListView):

    
    template_name ='dashboard/reports.html'
    context_object_name = 'reports'
    

    def get_queryset(self):
        
       

        user_tests_obj = (UserProgress.objects.filter(user=self.request.user)
                        .values('subject__subject_name','subject_id','is_complete')
                        .annotate(dcount=Count('subject'))
                    )
        
        
        print(user_tests_obj)
        query_set = {'user_tests': user_tests_obj,
                    'subjects_obj': SubjectInfo.objects.all()
                    }
        
        return query_set

