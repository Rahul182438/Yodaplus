
from django.contrib.auth.models import User
from django.db.models import query
from django.db.models.fields import SlugField
from django.http import request
from django.db.models import Count, QuerySet

from rest_framework import serializers, status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework.parsers import JSONParser,ParseError

from dashboard.models import QuestionType, SubjectInfo, AnswerInfo, QuestionInfo, UserProgress
from dashboard.api.serializers import QuestionTypeSerializer, SubjectSerializer, QuestionInfoSerializer, AnswerInfoSerializer, UserProgressSerializer, UserProgressTimeSerializer


class DashboardApiView(ListAPIView):
    
    """
    Permission class will be found common in all the functions as it is required to check
    user login so that to provide access
    
    A ListAPI view is used to return all the subjects available for a quiz test
    
    """
    permission_classes = [IsAuthenticated]
    
    

    queryset = SubjectInfo.objects.all()
    serializer_class = SubjectSerializer



class QuestionApiView(ListAPIView):
    
    permission_classes = [IsAuthenticated]
    serializer_class = QuestionInfoSerializer
    
    def get_queryset(self):

        """
        The selected subject name is retreived from the url.

        This function checks if user has already completed the quiz. 
        
        If Yes it will return and empty question set as url
        If No it will return question remaining for the users to complete. 
        """
        slug = self.kwargs['url_slug']

        user_obj = self.request.user

        subject_info_obj = SubjectInfo.objects.get(url_slug=slug)
        
        try:
            user_progress_obj = UserProgress.objects.filter(user=user_obj,subject=subject_info_obj)
        except:
            user_progress_obj = None
        
        if user_progress_obj:
            queryset_obj = QuestionInfo.objects.filter(subject_id=subject_info_obj.id).exclude(id__in = [obj.question.id if obj.is_complete == True else None for obj in user_progress_obj])
            
        else:
            queryset_obj = QuestionInfo.objects.filter(subject_id=subject_info_obj.id)
        return queryset_obj



class UserProgressApiView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserProgressSerializer



    def create(self,request):


        """
        UserProgress table is updated with user answer and time taken for each question
        """    
        user_obj = self.request.user

        data = request.data

        question = QuestionInfo.objects.get(id=data['question'])
        user_answer = data['user_answer']
        try:
            answer_obj = AnswerInfo.objects.get(answer=user_answer)
        except:
            answer_obj = None
        
        completed = data['complete']
        time = data['time']
        
        
        progress_obj = UserProgress()
        progress_obj.user = user_obj
        progress_obj.question = question
        progress_obj.subject = question.subject
        if answer_obj:
            progress_obj.mcq_answer = answer_obj
        else:
            progress_obj.one_word_answer = user_answer
        progress_obj.is_complete = completed
        progress_obj.time = time
        progress_obj.save()
        
        serializer = UserProgressSerializer(progress_obj)

        return Response(serializer.data)




class AnswersApiView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AnswerInfoSerializer

    """
    To fetch the list of available answers for each question (used for MCQ type)
    """

    def get_queryset(self):
        question_id = self.kwargs['question_id']
        query = AnswerInfo.objects.filter(question__id = question_id)
        return query





class ReportApiView(ListAPIView):
    
    serializer_class = UserProgressSerializer
    
    def get_queryset(self):

        """
        If the user has completed the quiz for a particular subject,
        A report is fetched from the user progress table and displays the 
        user progress report in detail.
        """

        slug = self.kwargs['url_slug']
        
        user_obj = self.request.user

        subject_info_obj = SubjectInfo.objects.get(url_slug=slug)

        try:
            user_progress_obj = UserProgress.objects.filter(user=user_obj,subject=subject_info_obj)
        except:
            user_progress_obj = None
        
        return user_progress_obj




class UserProgressTimeApiView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserProgressTimeSerializer

    def get_queryset(self):

        """
        To retreive the time taken for each question.
        """
        query_obj = UserProgress.objects.filter(user=self.request.user)
                    
        return query_obj