from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class QuestionType(models.Model):

    """
    A table to store the type of questions available for each quiz
    """

    MCQ = 'MCQ'
    ONE_LINE = 'One Line'
    quiz_choices = (
        (MCQ,'Multiple Choice Questions'),
        (ONE_LINE,'One Answer Questions'),
    )
    type_name = models.CharField(max_length=50, choices=quiz_choices)

    def __str__(self):
        return self.type_name

class SubjectInfo(models.Model):
    """
    A table to store all the subjects its scoring points and level of ease available for the quiz
    """

    Subj_one = 'Maths'
    Subj_two = 'GK'
    
    subject_choices = (
        (Subj_one,'Maths'),
        (Subj_two,'General Knowledge'),
    )

    level_1 = 'Easy'
    level_2 = 'Medium'
    level_3 = 'Hard'
    
    level_choices = (
        (level_1,'Easy'),
        (level_2,'Medium'),
        (level_3,'Hard'),
    )

    url_slug = models.SlugField(max_length=60, blank=False,unique=True)
    subject_name = models.CharField(max_length=50, choices=subject_choices)
    level = models.CharField(max_length=50, choices=level_choices)
    interval = models.IntegerField()
    min_score = models.IntegerField()
    max_score = models.IntegerField()

    def __str__(self):
        return self.subject_name + ' - ' + self.level


class QuestionInfo(models.Model):
    """
    A table to store all the questions for the respective subjects
    """
    type = models.ForeignKey(QuestionType, on_delete=models.CASCADE)
    subject = models.ForeignKey(SubjectInfo, on_delete=models.CASCADE)
    question = models.TextField(blank=True,null= True)
    max_score = models.IntegerField()

    def __str__(self):
        return 'Question' + str(self.id) + ' - ' + str(self.question[:100])
    
class AnswerInfo(models.Model):
    
    """
    A table to store all the mcq and one word answers
    """
    question = models.ForeignKey(QuestionInfo, on_delete=models.CASCADE)
    answer = models.CharField(max_length=50, null=True, blank=True)
    is_correct = models.BooleanField(default=False)



    def __str__(self):
        return str(self.answer)
    

class UserProgress(models.Model):
    """
    A table created for storing user's answers and time taken to complete respective questions
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.ForeignKey(SubjectInfo,on_delete=models.CASCADE)
    question = models.ForeignKey(QuestionInfo,on_delete=models.CASCADE)
    mcq_answer = models.ForeignKey(AnswerInfo, on_delete=models.CASCADE, null=True, blank=True)
    one_word_answer = models.CharField(max_length=50, null=True, blank=True)
    is_complete = models.BooleanField(default=False)
    time = models.DecimalField(max_digits=5, decimal_places=2,default=0)


    def __str__(self):
        if self.mcq_answer:
            return str(self.question) + str(self.mcq_answer)
        elif self.one_word_answer:
            return str(self.question) + str(self.one_word_answer)
        else:
            return str(self.question)


    def report(self):
        """
        A method which checks the whether the  user answers are correct or incorrect.
        Return a detail report on question's answered by user
        """
        try:
            answers_obj = AnswerInfo.objects.get(question=self.question,is_correct=True)
        except:
            answers_obj = None
        
        
        is_correct = False
        
        if self.mcq_answer == None and self.one_word_answer != "":
            if answers_obj:
                
                return str(self.question.question) +'\n Your Answer -> '+str(self.one_word_answer) + '\n Correct Answer -> ' + str(answers_obj.answer),is_correct
                
        elif self.mcq_answer and self.mcq_answer.is_correct == True:
            
            is_correct  = True
            return str(self.question.question) +'\n Correct Answer -> '+str(self.mcq_answer), is_correct
        
        elif self.mcq_answer:
            if answers_obj:
                return str(self.question.question) +'\n Your Answer -> '+str(self.mcq_answer) + '\n Correct Answer -> ' + str(answers_obj.answer), is_correct
        
        else:
            return str(self.question.question) +'\n You have not answered' + '\n Correct Answer -> ' + str(answers_obj.answer), is_correct

    
    def time_calc(self):
        """
        To calculate the total time used by user . - Used in API Section
        """
        time_used = 0
        if self.time:
            time_used += self.time
        return str(time_used)
