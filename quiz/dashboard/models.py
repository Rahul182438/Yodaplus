from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models.deletion import CASCADE
from django.db.models.expressions import Case
from django.utils.translation import ugettext_lazy as _
# Create your models here.
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
        ('Python','Python'),
        ('Django','Django'),
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

    # def save(self, *args, **kwargs):
    #     if self.max_score > self.subject.max_score:
    #         self.
    #     super().save(*args, **kwargs)


# class Options(models.Model):
#     question = models.ForeignKey(QuestionInfo, on_delete=models.CASCADE)
#     option = models.CharField(max_length=50, null=True, blank=True)

#     def save(self, *args, **kwargs):
#         if str(self.question.type) != 'MCQ':
#             self.option = None
#         super().save(*args, **kwargs)

#     def __str__(self):
#         return str(self.option)

class AnswerInfo(models.Model):
    
    question = models.ForeignKey(QuestionInfo, on_delete=models.CASCADE)
    answer = models.CharField(max_length=50, null=True, blank=True)
    is_correct = models.BooleanField(default=False)



    def __str__(self):
        return str(self.answer)


class UserProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(QuestionInfo,on_delete=models.CASCADE)
    mcq_answer = models.ForeignKey(AnswerInfo, on_delete=models.CASCADE, null=True, blank=True)
    one_word_answer = models.CharField(max_length=50, null=True, blank=True)

    # def __str__(self):
    #     return str(self.user) + " has completed " + str(self.report.question)

    # @property
    # def question_name(self):
    #     print(self.report.question)
    #     return str(self.report.question)


    def save(self, *args, **kwargs):
        print(self.right_choice)
        print(self.wrong_choice)
        if self.right_choice or self.wrong_choice:
            self.is_complete = True
        else:
            self.is_complete = False

        if self.right_choice and self.right_choice.is_right == False:
            self.wrong_choice = self.right_choice
            self.right_choice = None
            
        super().save(*args, **kwargs)


# class Report(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     question = models.ForeignKey(QuestionInfo, on_delete=models.CASCADE)
#     progress = models.ForeignKey(UserProgress, on_delete=models.CASCADE)
#     score = models.DecimalField(max_digits=5, decimal_places=2)
    

#     def __str__(self):
#         return str(self.user) + ' has scored '  + str(self.score) + ' points in ' + str(self.question)


