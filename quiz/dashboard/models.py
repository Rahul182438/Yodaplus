from io import open_code
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models.deletion import CASCADE
from django.db.models.expressions import Case
from django.db.models.fields.related import ForeignKey
from django.utils.translation import ugettext_lazy as _


class QuestionType(models.Model):
    quiz_choices = (
        ('MCQ','Multiple Choice Questions'),
        ('One Line','One Answer Questions'),
    )
    type_name = models.CharField(max_length=50, choices=quiz_choices)

    def __str__(self):
        return self.type_name



class SubjectInfo(models.Model):
    subject_choices = (
        ('Maths','Maths'),
        ('GK','General Knowledge'),
    )
    level_choices = (
        ('Easy','Easy'),
        ('Medium','Medium'),
        ('Hard','Hard'),
    )
    interval_choices = (
        ('0.5','30 Minutes'),
        ('1.0','1 Hour'),
    )
    subject_name = models.CharField(max_length=50, choices=subject_choices)
    level = models.CharField(max_length=50, choices=level_choices)
    interval = models.CharField(max_length=50, choices=interval_choices)
    min_score = models.DecimalField(max_digits=5, decimal_places=2)
    max_score = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.subject_name + ' - ' + self.level


class QuestionInfo(models.Model):
    type = models.ForeignKey(QuestionType, on_delete=models.CASCADE)
    subject = models.ForeignKey(SubjectInfo, on_delete=models.CASCADE)
    question = models.TextField(blank=True,null= True)
    max_score = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return 'Question' + str(self.id) + ' - ' + str(self.question[:100])


class AnswerInfo(models.Model):
    
    question = models.ForeignKey(QuestionInfo, on_delete=models.CASCADE)
    answer = models.CharField(max_length=50, null=True, blank=True)
    is_correct = models.BooleanField(default=False)



    def __str__(self):
        return str(self.answer)


class UserProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.ForeignKey(QuestionType,on_delete=models.CASCADE)
    subject = models.ForeignKey(SubjectInfo,on_delete=models.CASCADE)
    question = models.ForeignKey(QuestionInfo,on_delete=models.CASCADE)
    mcq_answer = models.ForeignKey(AnswerInfo, on_delete=models.CASCADE, null=True, blank=True)
    one_word_answer = models.CharField(max_length=50, null=True, blank=True)
    

    def save(self, *args, **kwargs):

        if self.right_choice or self.wrong_choice:
            self.is_complete = True
        else:
            self.is_complete = False
            
        super().save(*args, **kwargs)

