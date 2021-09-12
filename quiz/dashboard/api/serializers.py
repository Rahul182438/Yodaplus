from django.contrib.auth.models import User

from rest_framework import serializers
from dashboard.models import QuestionType, SubjectInfo, QuestionInfo, AnswerInfo, UserProgress


class QuestionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionType
        fields = '__all__'

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubjectInfo
        fields = '__all__'


class QuestionInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionInfo
        fields = '__all__'

class AnswerInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerInfo
        fields = '__all__'

class UserProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProgress
        fields = '__all__'
