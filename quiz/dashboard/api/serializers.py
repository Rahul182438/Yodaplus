from django.contrib.auth.models import User

from rest_framework import serializers
from dashboard.models import QuestionType, SubjectInfo, QuestionInfo, AnswerInfo, UserProgress


class QuestionTypeSerializer(serializers.ModelSerializer):

    """
    A Question Type Serializer to fetch all the type of questions available
    """
    class Meta:
        model = QuestionType
        fields = '__all__'

class SubjectSerializer(serializers.ModelSerializer):

    """
    A Subject Serializer to fetch all the subjects available
    """
    class Meta:
        model = SubjectInfo
        fields = '__all__'


class QuestionInfoSerializer(serializers.ModelSerializer):
    """
    A Serializer to fetch all the questions available

    To fetch some attributes of subject field subject is also passed to created a nested serializer response
    """
    subject = SubjectSerializer(read_only=True)
    class Meta:
        model = QuestionInfo
        fields = '__all__'

class AnswerInfoSerializer(serializers.ModelSerializer):
    """
    A Serializer to fetch all the answers available
    """
    class Meta:
        model = AnswerInfo
        fields = '__all__'

class UserProgressSerializer(serializers.ModelSerializer):
    
    """
    A Serializer to fetch user's progress
    """
    
    class Meta:
        model = UserProgress
        

        fields = ['report',]

    def report(self, instance):
        """
        This will return a function named report created in models section.
        """

        return instance.report()



class UserProgressTimeSerializer(serializers.ModelSerializer):

    """
    A Serializer to fetch user's progress
    """
    
    class Meta:
        model = UserProgress
        
        fields = ['time_calc']

    def time_calc(self, instance):
        """
        This will return a function named time_calc created in models section.
        """

        return instance.time_calc()


