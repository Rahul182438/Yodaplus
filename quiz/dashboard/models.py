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

    subject_name = models.CharField(max_length=50, choices=subject_choices)
    level = models.CharField(max_length=50, choices=level_choices)
    interval = models.IntegerField()
    min_score = models.IntegerField()
    max_score = models.IntegerField()

    def __str__(self):
        return self.subject_name + ' - ' + self.level


class QuestionInfo(models.Model):
    type = models.ForeignKey(QuestionType, on_delete=models.CASCADE)
    subject = models.ForeignKey(SubjectInfo, on_delete=models.CASCADE)
    question = models.TextField(blank=True,null= True)
    max_score = models.IntegerField()

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
    subject = models.ForeignKey(SubjectInfo,on_delete=models.CASCADE)
    question = models.ForeignKey(QuestionInfo,on_delete=models.CASCADE)
    mcq_answer = models.ForeignKey(AnswerInfo, on_delete=models.CASCADE, null=True, blank=True)
    one_word_answer = models.CharField(max_length=50, null=True, blank=True)
    is_complete = models.BooleanField(default=False)
    time = models.DecimalField(max_digits=5, decimal_places=2,default=0)


    def __str__(self):
        
        '''
        Filter out the return type according to the user has answered the questions
        '''
        try:
            answers_obj = AnswerInfo.objects.get(question=self.question,is_correct=True)
        except:
            answers_obj = None
        

        if self.mcq_answer == None and self.one_word_answer != "":
            if answers_obj:
                return str(self.question.question) +'\n Your Answer -> '+str(self.one_word_answer) + '\n Correct Answer -> ' + str(answers_obj.answer)
        
        
        elif self.mcq_answer and self.mcq_answer.is_correct == True:
            return str(self.question.question) +'\n Correct Answer -> '+str(self.mcq_answer)
        
        elif self.mcq_answer:
            if answers_obj:
                return str(self.question.question) +'\n Your Answer -> '+str(self.mcq_answer) + '\n Correct Answer -> ' + str(answers_obj.answer)
        
        else:
            return str(self.question.question) +'\n You have not answered' + '\n Correct Answer -> ' + str(answers_obj.answer)
        
