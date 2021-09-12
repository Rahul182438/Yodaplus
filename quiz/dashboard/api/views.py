
from django.contrib.auth.models import User
from django.db.models import query
from django.db.models.fields import SlugField
from django.http import request
from django.db.models import Count, QuerySet

from rest_framework import serializers, status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView, ListCreateAPIView


from dashboard.models import QuestionType, SubjectInfo, AnswerInfo, QuestionInfo, UserProgress
from dashboard.api.serializers import QuestionTypeSerializer, SubjectSerializer, QuestionInfoSerializer, AnswerInfoSerializer, UserProgressSerializer


class DashboardApiView(ListAPIView):
    permission_classes = [IsAuthenticated]
    
    queryset = SubjectInfo.objects.all()
    serializer_class = SubjectSerializer



class QuestionApiView(ListAPIView):
    
    serializer_class = QuestionInfoSerializer
    
    def get_queryset(self):
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

    def get_queryset(self):

        query_obj = (UserProgress.objects.filter(user=self.request.user)
                    .values('subject__subject_name','subject_id','is_complete','subject__url_slug')
                    .annotate(dcount=Count('subject'))
                    )
    

    def create(self):
        user_obj = self.request.user

        data = self.request.data
        question = QuestionInfo.objects.get(id=data['question'])
        user_answer = data['user_answer']
        answer_obj = AnswerInfo.objects.get(answer=user_answer)
        completed = data['complete']
        time = data['time']
        progress_obj = UserProgress()
        progress_obj.question = question
        if answer_obj:
            progress_obj.mcq_answer = user_answer
        else:
            progress_obj.one_word_answer = user_answer
        progress_obj.is_complete = completed
        progress_obj.time = time
        progress_obj.save()
        serializer = UserProgressSerializer(progress_obj)
        return Response(serializer.data)