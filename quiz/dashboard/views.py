from django.http.response import JsonResponse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView
from django.db.models import Count, QuerySet

from .models import SubjectInfo, UserProgress, AnswerInfo, QuestionInfo

'''
login required decorator is used to check whether the user is authenticated before displaying the dashboard pages
'''
@method_decorator(login_required(login_url='registration:login'),name='dispatch')
class DashboardView(ListView):

    '''
    template path is assigned.
    context_object_name refers to the object name to be used in the corresponding html pages.
    '''
    
    template_name ='dashboard/quiz_type.html'
    context_object_name = 'quiz_types'
    

    '''
    When the dashboard page is loaded below given query set is fetched and retuned
    '''
    def get_queryset(self):
        query_set = SubjectInfo.objects.all()
        return query_set


    '''
    Subject selected by user is selected and redirected to the quiz questions pages
    '''
    def post(self, *args, **kwargs):

        subject_id = self.request.POST.get('subject')

        return redirect('dashboard:quiz_questions',subject_name=subject_id)
    
        

'''
All questions are fetched for the particular subject selected and displayed
'''
class QuiestionView(DetailView):

    template_name = 'dashboard/questions.html'
    context_object_name = 'quiz'

    ''''''
    def get_object(self):
        complete = True
        max_score, min_score,score_earned = 0, 0, 0
        msg = ""
        subject_obj = SubjectInfo.objects.get(url_slug=self.kwargs.get("subject_name"))
        
        max_score = int(subject_obj.max_score)
        min_score = int(subject_obj.min_score)
        time_used = 0
        user_progress_obj = UserProgress.objects.filter(user=self.request.user,subject=subject_obj)
        
        my_answer_list = []
        quest_ids_list = []
        count = 0

        '''
        checks if user progress is found
        '''
        if user_progress_obj:
                
            for progress in user_progress_obj:
                '''
                For each progress found it stores the complete value.
                '''
                complete = progress.is_complete
                if progress.is_complete == False:
                    '''
                    If the respecive question is false a list is created to store the respective question ids.
                    '''
                    quest_ids_list.append(progress.question_id)
                else:
                    count += 1

                '''
                Time used by user is stored
                '''
                time_used = progress.time

                '''
                If user has a correct mcq answer or one word answer score is incremented
                '''
                if progress.mcq_answer and progress.mcq_answer.is_correct == True:
                    score_earned += int(progress.question.max_score)
                elif progress.one_word_answer:
                    
                    answers_obj = AnswerInfo.objects.get(question=progress.question,is_correct=True)

                    if answers_obj:
                        if str(answers_obj.answer) == str(progress.one_word_answer):
                            score_earned += int(progress.question.max_score)        
                            
            '''
            A text message to be displayed in the frontend according to score earned by the user.
            '''
            if score_earned == max_score or score_earned == min_score :
                msg = "You have passed the test with "+str(score_earned)+'/'+str(max_score)+" marks."

            elif score_earned < min_score:
                msg = "You have failed the test. Your Score is "+str(score_earned)+'/'+str(max_score)
            elif score_earned > min_score and score_earned < max_score:
                msg = "You have passed the test. Your Score is "+str(score_earned)+'/'+str(max_score)

        else:
            complete = True


        '''
        If quest_ids_list is not empty it will filter out the question that are not completed by user
        Else it will display all the questions 
        '''
        if quest_ids_list:
            questions_obj = QuestionInfo.objects.filter(subject=subject_obj,id__in=quest_ids_list)
        else:
            questions_obj = QuestionInfo.objects.filter(subject=subject_obj)



        
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





'''
On each next button user clicks in the question this function is called via ajax 
'''
def save_user_progress(request,subject_name):

    postdata = request.POST.copy()

    subject_obj = SubjectInfo.objects.get(url_slug=subject_name)

    '''
    Looping through all the data submitted
    '''    
    for data in postdata:


        '''
        checks answer retrieved from user is available in the answers table
        '''
        try:
            answers_obj = AnswerInfo.objects.get(question_id=data,answer=postdata[data])
        except:
            answers_obj = None

        '''
        checks if user's progress for the selected quiz questions
        '''
        try:
            progress_obj = UserProgress.objects.get(user=request.user,question_id=data,subject=subject_obj)
        except:
            progress_obj = None            
    

        '''
        Checks if progress of user and answers given is available from above and stores the respective id
        '''
        if progress_obj:
            if answers_obj:
                progress_obj.mcq_answer_id = answers_obj.id
            else:
                if postdata[data] == 'none':
                    progress_obj.is_complete = True
                else:
                    '''
                    if answer is not available in db stores the user input answer
                    '''
                    progress_obj.one_word_answer = postdata[data]
            'if complete is retrieved as true the question is completed'
            if postdata[data] == "true":
                complete = True

            progress_obj.save()
        else:
            '''
            If no user progress is found will create a new user progress
            '''

            '''
            Removes the complete and time data retrieved from database so as to match the rest of ids with question id in db
            '''
            if data != 'complete' and data != 'time':
                user_progress_obj = UserProgress()
                user_progress_obj.user = request.user
                
                user_progress_obj.question_id = data
                user_progress_obj.subject = subject_obj
                if answers_obj:
                    user_progress_obj.mcq_answer_id = answers_obj.id
                else:
                    user_progress_obj.one_word_answer = postdata[data]

                user_progress_obj.save()


            elif data == 'complete':
                '''
                Satisies the data retrieved for complete 
                '''
                if postdata[data] == "true":
                    complete = True
                    user_progress_obj = UserProgress.objects.filter(user=request.user,subject=subject_obj)
                    for progress in user_progress_obj:
                        progress.is_complete = complete
                        progress.save()
            elif data == 'time' and postdata[data]:
                '''
                stores the time taken for each question by user
                '''
                user_progress_obj = UserProgress.objects.filter(user=request.user,subject=subject_obj)
                for progress in user_progress_obj:
                    progress.time = float(postdata[data])
                    progress.save()                

    return JsonResponse({'success':'True'})






'''
Login is required for the report page to be displayed
'''

@method_decorator(login_required(login_url='registration:login'),name='dispatch')
class ReportView(ListView):
    
    template_name ='dashboard/reports.html'


    '''
    A GET method is requested
    
    A checks whether user has attempted any quiz 
    '''
    def get_queryset(self):
        
        query_set = (UserProgress.objects.filter(user=self.request.user)
                    .values('subject__subject_name','subject_id','is_complete','subject__url_slug')
                    .annotate(dcount=Count('subject'))
                    )
        return query_set

